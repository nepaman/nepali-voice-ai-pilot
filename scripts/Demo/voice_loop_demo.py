"""
Nepali Voice AI - voice_loop_demo.py (Gradio 6.x)
Complete voice loop: Speak → Transcribe → Respond → Speak back
"""

import gradio as gr
import whisper
from gtts import gTTS
import os
from pathlib import Path

# --------------------------------------------------
# 1. Paths and models
# --------------------------------------------------

SCRIPT_DIR   = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
RESPONSE_DIR = SCRIPT_DIR / "response_audio"

print("Loading Whisper model...")
model = whisper.load_model("small")
print("✓ Whisper 'small' loaded")

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
    """
    Detect Whisper looping: same word repeated more than 5 times.
    e.g. "अग्टाए अग्टाए अग्टाए..." or "तो तो तो तो..."
    """
    words = text.split()
    if len(words) < 4:
        return False
    for word in set(words):
        if words.count(word) > 5:
            print(f"  ⚠️ Hallucination: '{word}' repeated {words.count(word)}x — rejected")
            return True
    return False


# --------------------------------------------------
# 3. Response logic — real phonetic variants from YOUR logs
# --------------------------------------------------

def generate_smart_response(user_text: str):
    """
    Every variant below was actually seen in Whisper output from your test logs.
    We match on what Whisper ACTUALLY produces, not what we expect it to produce.
    """
    t = user_text

    # ── GREETING: नमस्ते / नमस्कार ──────────────────────────────────────
    # Seen: नमस्ते ✓, नवास्ते, नवस्तें, नमस्
    if any(k in t for k in [
        "नमस्ते", "नमस्कार", "नमस्",
        "नवास्ते", "नवस्ते", "नवस्तें", "नवास्"
    ]):
        return "नमस्कार! तपाईंलाई भेटेर खुशी लाग्यो। म नेपाली भ्वाइस एआई हुँ।", "greeting"

    # ── GOOD MORNING: शुभ प्रभात ─────────────────────────────────────────
    # Seen: सूबो प्रवाद, सूब प्रबात, सुबब्रबाद, शुबःप्रबाद
    if any(k in t for k in [
        "प्रभात", "प्रबात", "प्रवाद", "प्रबाद",
        "बिहानी", "सुबब्र", "सूबो", "शुबः",
        "सुप्र", "शुभप्र"
    ]):
        return "शुभ प्रभात! आज तपाईंको दिन शुभ रहोस्।", "morning"

    # ── THANK YOU: धन्यवाद ───────────────────────────────────────────────
    # Seen: तन्ये बाद, तान्धे बाद, तभन्ने बाद
    # Pattern: Whisper loses the "ध" and writes त instead
    #          and converts "न्यवाद" → "न्ये बाद" / "न्धे बाद" / "भन्ने बाद"
    # Match on: any "बाद" or "वाद" that follows a short word (2-4 chars)
    if any(k in t for k in [
        "धन्यवाद", "धन्यबाद", "धन्य",
        "तन्ये", "तान्धे", "तभन्ने",
        "थ्यान्क", "थान्क", "धन्"
    ]):
        return "तपाईंलाई पनि धन्यवाद! सधैं खुशी छु सहयोग गर्न।", "thanks"

    # Extra: catch "X बाद" pattern where X is 2-5 chars (धन्यवाद variants)
    words = t.split()
    for i, word in enumerate(words):
        if word in ["बाद", "वाद"] and i > 0 and len(words[i-1]) <= 5:
            print(f"  → Caught धन्यवाद via बाद/वाद pattern: '{t}'")
            return "तपाईंलाई पनि धन्यवाद! सधैं खुशी छु सहयोग गर्न।", "thanks"

    # ── GOOD NIGHT: शुभ रात्रि ───────────────────────────────────────────
    # Seen: सुबरात्री ✓ (already working well)
    if any(k in t for k in [
        "रात्रि", "रात्री", "राति", "रात्",
        "सुबरात", "शुभरात"
    ]):
        return "शुभ रात्रि! राम्रोसँग सुत्नुहोस्।", "goodnight"

    # ── HOW ARE YOU: कस्तो छ ─────────────────────────────────────────────
    # Seen: ख़ाँ तो था, ख़्ष्टो चा, ख़ाँ तो चाँ
    # Pattern: Whisper writes ख़ (kha with nukta) instead of क
    #          "स्तो" → "ाँ तो" or "्ष्टो"
    #          "छ" → "था" / "चा" / "चाँ"
    if any(k in t for k in [
        "कस्तो", "कस्तै", "कस्",
        "ख़ाँ", "ख़्ष्", "ख़्ट",       # Whisper's ख़ variants
        "काँ तो", "खाँ तो",            # space variants
        "छ", "चा", "था"                 # "छ" endings — broad catch
    ]):
        # Avoid false positives on "छ" alone — needs context
        if "कस्" in t or "ख़" in t or "काँ" in t or "खाँ" in t:
            return "म ठीक छु, धन्यवाद! तपाईं कस्तो हुनुहुन्छ?", "howru"
        # If just "छ" matched, check it's not part of another phrase
        if "छ" in t and not any(k in t for k in ["प्रभात", "रात्र", "नमस्", "धन्"]):
            return "म ठीक छु, धन्यवाद! तपाईं कस्तो हुनुहुन्छ?", "howru"

    # ── DEFAULT ───────────────────────────────────────────────────────────
    return f"तपाईंले भन्नुभयो: {user_text}। म अझै सिक्दैछु!", "default"


# --------------------------------------------------
# 4. Core function: STT → smart reply → play your voice
# --------------------------------------------------

def transcribe_and_respond(audio_path):
    if audio_path is None:
        return "⚠️ No audio received. Please record first.", "", None

    try:
        result = model.transcribe(
            audio_path,
            language="ne",
            fp16=False,
            temperature=0.0,
            no_speech_threshold=0.6,
            compression_ratio_threshold=2.0,
            condition_on_previous_text=False,
        )
        user_text = result["text"].strip()
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
# 5. Gradio UI
# --------------------------------------------------

with gr.Blocks(title="Nepali Voice AI Demo") as demo:
    gr.Markdown("""
    # 🇳🇵 Nepali Voice AI — Phase 2 Demo
    **नेपाली भ्वाइस एआई - प्रदर्शन**

    Speak in Nepali → see transcript → hear response in your own voice!

    **Try saying:** नमस्ते · शुभ प्रभात · धन्यवाद · शुभ रात्रि · कस्तो छ
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

    gr.Markdown("---\n**Phase 2 Demo** | Whisper STT + Your recorded voice | March 2026")


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("Starting Nepali Voice AI — voice_loop_demo.py")
    print("Open: http://127.0.0.1:7860")
    print("=" * 70)
    demo.launch(
        share=False,
        server_name="127.0.0.1",
        server_port=7860,
        show_error=True
    )