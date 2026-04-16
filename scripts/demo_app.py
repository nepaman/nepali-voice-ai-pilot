import gradio as gr
import torch
import librosa
import numpy as np
from transformers import WhisperForConditionalGeneration, WhisperProcessor
from pathlib import Path

MODEL_PATH = Path("models/whisper-nepali")
DEVICE = "mps" if torch.backends.mps.is_available() else "cpu"

print(f"Loading model on {DEVICE}...")
processor = WhisperProcessor.from_pretrained(MODEL_PATH)
model = WhisperForConditionalGeneration.from_pretrained(MODEL_PATH).to(DEVICE)
model.eval()
print("✅ Model ready!")

def transcribe(audio):
    if audio is None:
        return "Please record audio first."
    sr, data = audio
    if data.dtype != np.float32:
        data = data.astype(np.float32) / np.iinfo(data.dtype).max
    if len(data.shape) > 1:
        data = data.mean(axis=1)
    if sr != 16000:
        data = librosa.resample(data, orig_sr=sr, target_sr=16000)
    inputs = processor(data, sampling_rate=16000, return_tensors="pt")
    input_features = inputs.input_features.to(DEVICE)
    with torch.no_grad():
        predicted_ids = model.generate(
            input_features,
            language="nepali",
            task="transcribe"
        )
    transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
    return transcription

demo = gr.Interface(
    fn=transcribe,
    inputs=gr.Audio(sources=["microphone"], label="🎙️ Speak in Nepali"),
    outputs=gr.Textbox(label="📝 Transcription"),
    title="🇳🇵 Nepali Voice AI — Phase 4",
    description="Fine-tuned Whisper model trained on 256 Nepali recordings.\nSpeak clearly into your microphone.",
    theme=gr.themes.Soft()
)

demo.launch(share=True)
