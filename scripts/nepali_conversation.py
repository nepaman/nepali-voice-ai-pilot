import os
import torch
import librosa
import numpy as np
import anthropic
import gradio as gr
import tempfile
import asyncio
import edge_tts
from gtts import gTTS
from pathlib import Path
from transformers import WhisperForConditionalGeneration, WhisperProcessor
from dotenv import load_dotenv
import re

load_dotenv()

MODEL_PATH  = Path("models/whisper-nepali")
DEVICE      = "mps" if torch.backends.mps.is_available() else "cpu"
SAMPLE_RATE = 16000

VOICES = {
    "Sagar (Male)": "ne-NP-SagarNeural",
    "Hemkala (Female)": "ne-NP-HemkalaNeural"
}

print(f"Device: {DEVICE}")
print("Loading Whisper STT...")
processor = WhisperProcessor.from_pretrained(MODEL_PATH)
whisper   = WhisperForConditionalGeneration.from_pretrained(MODEL_PATH).to(DEVICE)
whisper.eval()
print("Whisper loaded")

client  = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
history = []

PROJECT_CONTEXT = """
tapain Nepali samudayako lagi banaeko Nepali Voice AI ko sahayak hunuhunchha.
Yo pehilo community-owned, open-source Nepali Voice AI ho.
256 Nepali recording sangalana gariyeko chha.
Lakshya 500 bhandha badi recording sangalana garnu ho.
Yo pariyojana Nepali samudayako lagi nihshulka chha.

Sadhai Nepali lipima matra jawaf dinuhos — romanized va English ma kahilyai nadinus.
Afno jawaf sadhai 1-2 wakyama matra dinuhos — kabhi pani lamo jawaf nadinus.
Pura wakya ma jawaf dinuhos — adha wakyama kabhi naroknus.
Kunai pani markdown formatting, star (**), dash (-), bullet points prayog nagarnuhos.
"""

def clean_text(text):
    text = re.sub(r"\*+", "", text)
    text = re.sub(r"#+\s*", "", text)
    text = re.sub(r"[-]+", "", text)
    text = re.sub(r"\n+", " ", text)
    return re.sub(r"\s+", " ", text).strip()

def get_claude_response(user_text):
    history.append({"role": "user", "content": user_text})
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=600,
        system=PROJECT_CONTEXT,
        messages=history
    )
    reply = clean_text(response.content[0].text.strip())
    history.append({"role": "assistant", "content": reply})
    return reply

async def speak_async(text, voice_key):
    voice = VOICES[voice_key]
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
        output_path = f.name
    try:
        await edge_tts.Communicate(text, voice=voice).save(output_path)
    except Exception:
        gTTS(text=text, lang="ne").save(output_path)
    return output_path

def speak_nepali(text, voice_key):
    return asyncio.run(speak_async(text, voice_key))

def transcribe_audio(audio):
    if audio is None:
        return ""
    sr, data = audio
    if data.dtype != np.float32:
        data = data.astype(np.float32) / np.iinfo(data.dtype).max
    if len(data.shape) > 1:
        data = data.mean(axis=1)
    if sr != SAMPLE_RATE:
        data = librosa.resample(data, orig_sr=sr, target_sr=SAMPLE_RATE)
    inputs = processor(data, sampling_rate=SAMPLE_RATE, return_tensors="pt")
    input_features = inputs.input_features.to(DEVICE)
    with torch.no_grad():
        predicted_ids = whisper.generate(
            input_features,
            language="nepali",
            task="transcribe"
        )
    return processor.batch_decode(predicted_ids, skip_special_tokens=True)[0].strip()

def get_chat_display():
    return [(h["content"], None) if h["role"] == "user"
            else (None, h["content"]) for h in history]

def voice_conversation(audio, voice_key):
    user_text = transcribe_audio(audio)
    if not user_text:
        return "Sunna sakiena — feri koshish garnuhos", None, None, get_chat_display()
    ai_text = get_claude_response(user_text)
    return user_text, speak_nepali(ai_text, voice_key), None, get_chat_display()

def text_conversation(text, voice_key):
    if not text or not text.strip():
        return "", None, "", get_chat_display()
    ai_text = get_claude_response(text.strip())
    return ai_text, speak_nepali(ai_text, voice_key), "", get_chat_display()

def reset_conversation():
    global history
    history = []
    return None, "", None, None, []

with gr.Blocks(theme=gr.themes.Soft(), title="Nepali Voice AI") as demo:

    gr.Markdown("""
    # Nepali Voice AI
    Community-owned open-source Nepali Voice AI
    Speak or type in Nepali — AI responds in Nepali voice
    """)

    gr.Markdown("""
    ---
    HOW TO USE / KASARI PRAYOG GARNE:

    VOICE (Awaj bata): Select the Speak Nepali tab. Click the microphone button to start recording. Speak clearly in Nepali. Click the microphone button again to stop. Click Submit. When the AI Response audio appears, press the Play button to hear the answer.

    TEXT (Lekhera): Select the Type Nepali tab. Type any Nepali sentence or question. Press Enter or click Submit. When the AI Response audio appears, press the Play button to hear the answer.

    VOICE SELECTOR: Choose Sagar for male voice or Hemkala for female voice.

    NEW CONVERSATION: Click Start New Conversation to clear history and begin fresh.

    NOTE: After AI responds, press the Play button to hear the voice. Microphone resets automatically after each submission.
    ---
    """)

    voice_selector = gr.Radio(
        choices=list(VOICES.keys()),
        value="Sagar (Male)",
        label="Select Voice / Awaj Chunuhos",
        interactive=True
    )

    with gr.Tabs():
        with gr.Tab("Speak Nepali / Bolnuhos"):
            gr.Markdown("Click microphone to start, speak Nepali clearly, click again to stop, then click Submit.")
            voice_input = gr.Audio(
                source="microphone",
                type="numpy",
                label="Microphone — Click to start recording"
            )
            voice_btn = gr.Button("Submit", variant="primary", size="lg")
            voice_out_text  = gr.Textbox(label="What you said / Tapain bhannu bhayo", interactive=False)
            voice_out_audio = gr.Audio(label="AI Response — Press Play to hear", autoplay=False)

        with gr.Tab("Type Nepali / Lekhnus"):
            gr.Markdown("Type any Nepali sentence below and press Enter or click Submit.")
            text_input = gr.Textbox(
                placeholder="Type Nepali here...",
                label="Type Nepali / Nepali ma lekhnus",
                lines=2
            )
            text_btn = gr.Button("Submit", variant="primary", size="lg")
            text_out_response = gr.Textbox(label="AI Response (text)", interactive=False)
            text_out_audio    = gr.Audio(label="AI Response — Press Play to hear", autoplay=False)

    chatbot   = gr.Chatbot(label="Conversation History / Kurakani Itihas", height=300)
    reset_btn = gr.Button("Start New Conversation / Naya Kurakani Suru Garnuhos")

    gr.Markdown("---")
    gr.Markdown("Ask anything about Nepal, this project, or any topic in Nepali.")

    voice_btn.click(
        fn=voice_conversation,
        inputs=[voice_input, voice_selector],
        outputs=[voice_out_text, voice_out_audio, voice_input, chatbot]
    )
    text_btn.click(
        fn=text_conversation,
        inputs=[text_input, voice_selector],
        outputs=[text_out_response, text_out_audio, text_input, chatbot]
    )
    text_input.submit(
        fn=text_conversation,
        inputs=[text_input, voice_selector],
        outputs=[text_out_response, text_out_audio, text_input, chatbot]
    )
    reset_btn.click(
        fn=reset_conversation,
        outputs=[voice_input, text_input, text_out_audio, voice_out_audio, chatbot]
    )

demo.launch(share=True)
