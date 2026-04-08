"""
Nepali Voice AI - voice_loop_demo.py (Gradio 6.x)
Complete voice loop: Speak → Transcribe → Respond → Speak back
Now using fine-tuned Whisper model (Phase 3)
"""

import gradio as gr
import torch
import librosa
from gtts import gTTS
import os
from pathlib import Path
from transformers import WhisperForConditionalGeneration, WhisperProcessor

# --------------------------------------------------
# 1. Paths and models
# --------------------------------------------------

SCRIPT_DIR   = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
RESPONSE_DIR = SCRIPT_DIR / "response_audio"
MODEL_DIR    = PROJECT_ROOT / "models" / "whisper-nepali"

DEVICE = "mps" if torch.backends.mps.is_available() else "cpu"

# Load fine-tuned Whisper model
print("Loading fine-tuned Whisper model...")
if MODEL_DIR.exists():
    ft_processor = WhisperProcessor.from_pretrained(str(MODEL_DIR))
    ft_model     = WhisperForConditionalGeneration.from_pretrained(str(MODEL_DIR))
    ft_model     = ft_model.to(DEVICE)
    ft_model.eval()
    USE_FINETUNED = True
    print(f"✓ Fine-tuned Whisper loaded from {MODEL_DIR}")
else:
    import whisper
    ft_model     = whisper.load_model("small")
    ft_processor = None
    USE_FINETUNED = False
    print("⚠️  Fine-tuned model not found — using baseline whisper-small")

print(f"→ Project root : {PROJECT_ROOT}")
print(f"→ Response dir : {RESPONSE_DIR}")
print(f"→ Dir exists   : {RESPONSE_DIR.exists()}")

RESPONSE_AUDIO = {
    "greeting":  RESPONSE_DIR / "greeting_response.wav",
    "morning":   RESPONSE_DIR / "morning_response.wav",
    "thanks":    RESPONSE_DIR / "thanks_response.wav",
    "goodnight": RESPONSE_DIR / "goodnight_response.wav",
    "howru":     RESPONSE_DIR / "howru_response.wav",
    "default":   RESPONSE_DIR / "default_response.wav",
}

for key, path in RESPONSE_AUDIO.items():
    status = "✓" if path.exists() else "✗ MISSING"
    print(f"  {status} {key}: {path.name}")


# --------------------------------------------------
# 2. Hallucination detection
# --------------------------------------------------

def is_hallucination(text: str) -> bool:
    words = text.split()
    if len(words) < 4:
        return False
    for word in set(words):
        if words.count(word) > 5:
            print(f"  ⚠️ Hallucination: '{word}' repeated {words.count(word)}x — rejected")
            return True
    return False


# --------------------------------------------------
# 3. Response logic
# --------------------------------------------------

def generate_smart_response(user_text: str):
    t = user_text

    if any(k in t for k in ["नमस्ते", "नमस्कार", "नमस्", "नवास्ते", "नवस्ते", "आपस्कार"]):
        return "नमस्कार! तपाईंलाई भेटेर खुशी लाग्यो। म नेपाली भ्वाइस एआई हुँ।", "greeting"

    if any(k in t for k in ["प्रभात", "प्रबात", "प्रवाद", "प्रबाद", "बिहानी", "सुबब्र", "सूबो"]):
        return "शुभ प्रभात! आज तपाईंको दिन शुभ रहोस्।", "morning"

    if any(k in t for k in ["धन्यवाद", "धन्यबाद", "धन्य", "तन्ये", "तान्धे", "तभन्ने"]):
        return "तपाईंलाई पनि धन्यवाद! सधैं खुशी छु सहयोग गर्न।", "thanks"

    words = t.split()
    for i, word in enumerate(words):
        if word in ["बाद", "वाद"] and i > 0 and len(words[i-1]) <= 5:
            return "तपाईंलाई पनि धन्यवाद! सधैं खुशी छु सहयोग गर्न।", "thanks"

    if any(k in t for k in ["रात्रि", "रात्री", "राति", "सुबरात", "शुभरात"]):
        return "शुभ रात्रि! राम्रोसँग सुत्नुहोस्।", "goodnight"

    if any(k in t for k in ["कस्तो", "कस्तै", "ख़ाँ", "ख़्ष्", "काँ तो"]):
        if any(k in t for k in ["कस्", "ख़", "काँ", "खाँ"]):
            return "म ठीक छु, धन्यवाद! तपाईं कस्तो हुनुहुन्छ?", "howru"

    return f"तपाईंले भन्नुभयो: {user_text}। म अझै सिक्दैछु!", "default"


# --------------------------------------------------
# 4. Transcribe using fine-tuned model
# --------------------------------------------------

def transcribe_audio(audio_path: str) -> str:
    if USE_FINETUNED:
        audio_array, _ = librosa.load(audio_path, sr=16000)
        inputs = ft_processor(
            audio_array,
            sampling_rate=16000,
            return_tensors="pt"
        ).input_features.to(DEVICE)
        with torch.no_grad():
            predicted_ids = ft_model.generate(inputs)
        return ft_processor.batch_decode(
            predicted_ids, skip_special_tokens=True
        )[0].strip()
    else:
        result = ft_model.transcribe(
            audio_path,
            language="ne",
            fp16=False,
            temperature=0.0,
            condition_on_previous_text=False,
        )
        return result["text"].strip()


# --------------------------------------------------
# 5. Core function: STT → smart reply → play your voice
# --------------------------------------------------

def transcribe_and_respond(audio_path):
    if audio_path is None:
        return "⚠️ No audio received. Please record first.", "", None

    try:
        user_text = transcribe_audio(audio_path)
    except Exception as e:
        return f"❌ Transcription error: {e}", "", None

    if not user_text:
        return "⚠️ Could not understand. Please speak clearly.", "", None

    if is_hallucination(user_text):
        return "⚠️ Audio unclear — please speak a full phrase slowly.", "", None

    print(f"Whisper heard: {user_text}")

    response_text, response_type = generate_smart_response(user_text)
    print(f"Matched type : {response_type}")

    audio_file = RESPONSE_AUDIO.get(response_type, RESPONSE_AUDIO["default"])

    if audio_file.exists():
        output_audio = str(audio_file)
        print(f"✓ Playing YOUR voice: {audio_file.name}")
    else:
        print("✗ WAV missing — falling back to gTTS")
        output_audio = str(PROJECT_ROOT / "temp_response.mp3")
        try:
            tts = gTTS(text=response_text, lang='ne')
            tts.save(output_audio)
        except Exception as e:
            return user_text, f"(TTS error: {e}) {response_text}", None

    return user_text, response_text, output_audio


# --------------------------------------------------
# 6. Gradio UI
# --------------------------------------------------

model_label = "Fine-tuned Whisper" if USE_FINETUNED else "Baseline Whisper"

with gr.Blocks(title="Nepali Voice AI Demo") as demo:
    gr.Markdown(f"""
    # 🇳🇵 Nepali Voice AI — Phase 3 Demo
    **नेपाली भ्वाइस एआई - प्रदर्शन**

    Speak in Nepali → see transcript → hear response in your own voice!

    **STT Model:** {model_label} · **Try saying:** नमस्ते · शुभ प्रभात · धन्यवाद · शुभ रात्रि · कस्तो छ
    """)

    with gr.Row():
        with gr.Column(scale=1):
            audio_input = gr.Audio(
                sources=["microphone"],
                type="filepath",
                label="🎤 Speak Nepali — click mic to start"
            )
            submit_btn = gr.Button("▶ Process Recording", variant="primary")

        with gr.Column(scale=1):
            transcription = gr.Textbox(
                label="📝 What Whisper heard",
                lines=2,
                interactive=False
            )
            response_out = gr.Textbox(
                label="💬 AI Response",
                lines=2,
                interactive=False
            )
            audio_output = gr.Audio(
                label="🔊 Hear Response (your voice)",
                autoplay=True,
                interactive=False
            )

    process_inputs  = [audio_input]
    process_outputs = [transcription, response_out, audio_output]

    submit_btn.click(
        fn=transcribe_and_respond,
        inputs=process_inputs,
        outputs=process_outputs
    )

    audio_input.stop_recording(
        fn=transcribe_and_respond,
        inputs=process_inputs,
        outputs=process_outputs
    )

    gr.Markdown("---\n**Phase 3 Demo** | Fine-tuned Whisper STT + Your recorded voice | April 2026")


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("Starting Nepali Voice AI — Phase 3 Demo")
    print("Open: http://127.0.0.1:7860")
    print("=" * 70)
    demo.launch(
        share=False,
        server_name="127.0.0.1",
        server_port=7860,
        show_error=True
    )