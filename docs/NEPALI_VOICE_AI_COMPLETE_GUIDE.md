# Nepali Voice AI — Complete Project Guide
# Phase 1 to Phase 5

For the Nepali community, by the Nepali community.
Last updated: April 2026

---

## What This Project Is

A community-owned, open-source Nepali Voice AI that:
- Listens to you speak Nepali (Speech to Text)
- Understands your question using Claude AI
- Responds in Nepali voice (Text to Speech)
- Runs locally on your Mac or in a browser

---

## System Workflow

```
You speak Nepali into microphone
            |
            v
Whisper STT (your fine-tuned model)
Converts your Nepali speech into Nepali text
            |
            v
Claude AI (claude-opus-4-5)
Reads the Nepali text
Thinks of an intelligent Nepali response
            |
            v
Edge-TTS (Microsoft Nepali voices)
Converts the response text into spoken audio
Male voice: Sagar (ne-NP-SagarNeural)
Female voice: Hemkala (ne-NP-HemkalaNeural)
            |
            v
You hear the Nepali response
Press Play button to listen
```

---

## Project Structure

```
nepali-voice-ai-pilot/
|
|-- data/
|   |-- audio/                    256 WAV recordings (NP_001 to NP_256)
|   |-- metadata_all.csv          Master list of all recordings
|   |-- datasets/                 Train and test splits for Whisper
|   |-- _archive/                 Old files kept for reference
|
|-- models/
|   |-- whisper-nepali/           Your fine-tuned Whisper model
|       |-- model.safetensors     The trained model weights
|       |-- config.json
|       |-- vocab.json
|       |-- tokenizer.json
|       |-- test_results.json     WER results
|
|-- scripts/
|   |-- prepare_dataset.py        Step 1: Prepare data for training
|   |-- finetune_whisper.py       Step 2: Train the Whisper model
|   |-- test_finetuned.py         Step 3: Test accuracy
|   |-- nepali_conversation.py    Phase 5: The conversation app
|   |-- record_batch.py           Helper to record new audio
|   |-- demo_app.py               Simple STT-only demo
|
|-- hf_space/                     HuggingFace Spaces deployment files
|   |-- app.py
|   |-- requirements.txt
|   |-- README.md
|
|-- docs/
|   |-- TECHNICAL_DOCUMENTATION.md
|   |-- NEPALI_VOICE_AI_COMPLETE_GUIDE.md  (this file)
|
|-- .env                          Your API keys (never commit this)
|-- .gitignore
|-- README.md
```

---

## Phase History

### Phase 1 and 2 — Setup and First Recordings (Early 2026)

What was done:
- Created the project folder structure
- Set up Python 3.10 virtual environment
- Bought RODE NT1 5th Gen microphone
- Recorded first 50 Nepali audio samples using Audacity
- Created metadata CSV format (filename, transcript, romanized)
- Set up GitHub repository: https://github.com/nepaman/nepali-voice-ai-pilot

Key files created:
- data/audio/NP_001.wav to NP_050.wav
- data/metadata.csv (first version)

---

### Phase 3 — Whisper Fine-tuning with 151 Samples

What was done:
- Recorded 151 clean Nepali WAV files using Audacity and RODE NT1
- Created prepare_dataset.py to split data 80/20 train/test
- Created finetune_whisper.py to train Whisper on Nepali
- Trained openai/whisper-tiny on Apple M1 Mac using MPS (Metal GPU)
- Pushed model to HuggingFace Hub: nepaman/whisper-nepali-tiny
- Baseline WER (before training): 211.5%
- WER after Phase 3: approximately 90%

How to run Phase 3 training:
```bash
cd ~/Documents/nepali-voice-ai-pilot
source venv/bin/activate

python scripts/prepare_dataset.py
python scripts/finetune_whisper.py
python scripts/test_finetuned.py
```

---

### Phase 4 — More Data and Retrain (256 Samples)

What was done:
- Deleted Phase 3 recordings that had background hum noise
- Re-recorded NP_151 to NP_256 using Audacity and RODE NT1
- Fixed metadata_all.csv to correctly match all 256 audio files
- Archived old metadata files and old audio folders
- Retrained Whisper on all 256 samples
- Final WER: 78.6% (improvement of 132.8% over baseline)
- Pushed updated model to HuggingFace Hub

Recording categories used:
- Numbers: एक, दुई, तीन up to एक हजार
- Greetings: नमस्ते, शुभ प्रभात, शुभ रात्रि
- Daily phrases: खाना खानु भयो, कस्तो छ, धन्यवाद
- Commands: बन्द गर्नुहोस्, सुन्नुहोस्, सुरु गर्नुहोस्
- Days and time: सोमबार, बिहान, साँझ, रात
- Family: आमा, बुवा, दाइ, दिदी, भाइ, बहिनी
- Places: काठमाडौं, पोखरा, हिमालय, नेपाल
- Food: दाल भात, रोटी, चिया, पानी
- Full sentences: conversational Nepali

Audio format requirements:
- Format: WAV
- Sample rate: 16000 Hz (16kHz)
- Channels: Mono
- Software: Audacity
- Microphone: RODE NT1 5th Gen (device 0)

Check microphone device number:
```bash
python3 -c "import sounddevice as sd; print(sd.query_devices())"
```

---

### Phase 5 — Voice Conversation App

What was done:
- Built the full conversation pipeline
- Integrated Claude AI for intelligent Nepali responses
- Added Edge-TTS for natural Nepali voice output
- Built Gradio web interface with two tabs
- Added voice selector for male (Sagar) and female (Hemkala)
- Conversation history display
- Auto-clears microphone and text after each submission
- Runs locally with shareable public link

How to run the conversation app:
```bash
cd ~/Documents/nepali-voice-ai-pilot
source venv/bin/activate
python scripts/nepali_conversation.py
```

The terminal will show a link like:
https://abc123.gradio.live

Share this link with anyone. It works for 72 hours then expires.
Run the script again to get a new link.

---

## The Full Conversation Script (nepali_conversation.py)

```python
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

processor = WhisperProcessor.from_pretrained(MODEL_PATH)
whisper   = WhisperForConditionalGeneration.from_pretrained(MODEL_PATH).to(DEVICE)
whisper.eval()

client  = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
history = []

PROJECT_CONTEXT = """
tapain Nepali samudayako lagi banaeko Nepali Voice AI ko sahayak hunuhunchha.
Yo pehilo community-owned, open-source Nepali Voice AI ho.
256 Nepali recording sangalana gariyeko chha.
Lakshya 500 bhandha badi recording sangalana garnu ho.

Sadhai Nepali lipima matra jawaf dinuhos.
Afno jawaf sadhai 1-2 wakyama matra dinuhos.
Pura wakya ma jawaf dinuhos.
Kunai pani markdown formatting prayog nagarnuhos.
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
            input_features, language="nepali", task="transcribe"
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

# Gradio interface built with two tabs:
# Tab 1: Speak Nepali (voice input)
# Tab 2: Type Nepali (text input)
# Voice selector: Sagar (Male) or Hemkala (Female)
# Conversation history displayed below

demo.launch(share=True)
```

---

## Training Pipeline Explained

### Step 1: prepare_dataset.py

What it does:
1. Reads data/metadata_all.csv
2. Loads each WAV file from data/audio/
3. Resamples audio to 16kHz if needed
4. Splits into 80% train and 20% test
5. Saves to data/datasets/whisper_finetune/

### Step 2: finetune_whisper.py

What it does:
1. Loads openai/whisper-tiny as the base model
2. Uses Apple M1 GPU (MPS) for faster training
3. Trains for 20 epochs
4. Batch size 4 (effective 8 with gradient accumulation)
5. Prints WER score every 100 steps
6. Saves best model to models/whisper-nepali/

Training results from Phase 4:
- Step 100: WER 100.76%
- Step 200: WER 87.02%
- Step 300: WER 83.97%
- Step 400: WER 82.44%
- Step 500: WER 78.63%
- Final: WER 78.63%

### Step 3: test_finetuned.py

What it does:
1. Loads your fine-tuned model
2. Loads baseline whisper-small for comparison
3. Tests on 51 test samples
4. Shows side-by-side comparison
5. Saves results to models/whisper-nepali/test_results.json

Final results:
- Baseline WER: 211.5%
- Fine-tuned WER: 78.6%
- Improvement: 132.8%

---

## Push Model to HuggingFace Hub

Run this when you want to update the model online:

```python
from transformers import WhisperForConditionalGeneration, WhisperProcessor

model = WhisperForConditionalGeneration.from_pretrained("models/whisper-nepali")
processor = WhisperProcessor.from_pretrained("models/whisper-nepali")
model.push_to_hub("nepaman/whisper-nepali-tiny")
processor.push_to_hub("nepaman/whisper-nepali-tiny")
```

---

## Environment Setup

### .env file (local only, never commit to GitHub)

```
ANTHROPIC_API_KEY=sk-ant-your-key-here
HF_TOKEN=hf_your-token-here
```

Get Anthropic key: https://console.anthropic.com
Get HuggingFace token: https://huggingface.co/settings/tokens

### Install all dependencies

```bash
cd ~/Documents/nepali-voice-ai-pilot
source venv/bin/activate

pip install torch==2.4.0 torchaudio==2.4.0 torchvision==0.19.0
pip install transformers==4.45.0
pip install gradio==3.50.2 gradio-client==0.6.1
pip install anthropic edge-tts gtts librosa soundfile
pip install python-dotenv huggingface_hub
```

---

## Useful Commands

Listen to a recording:
```bash
afplay data/audio/NP_001.wav
```

Check audio and metadata match:
```bash
ls data/audio/NP_*.wav | wc -l
tail -n +2 data/metadata_all.csv | wc -l
```

Push to GitHub:
```bash
git add .
git commit -m "your message"
git push origin main
```

Run the conversation app:
```bash
cd ~/Documents/nepali-voice-ai-pilot
source venv/bin/activate
python scripts/nepali_conversation.py
```

---

## Model Performance Summary

| Phase | Samples | WER     | Notes                          |
|-------|---------|---------|--------------------------------|
| Base  | 0       | 211.5%  | No fine-tuning                 |
| 3     | 151     | ~90%    | First fine-tune                |
| 4     | 256     | 78.6%   | Re-recorded with RODE NT1      |
| 6 goal| 500+   | Below 50%| Phase 6 target               |

WER = Word Error Rate. Lower is better. 0% means perfect.

---

## Key Decisions Made

Why Whisper Tiny?
- Small enough to run on Mac M1 without GPU
- Fast enough for real-time conversation
- Good base for fine-tuning with limited data

Why Claude AI?
- Best understanding of Nepali context
- Maintains full conversation history
- Customizable with system prompts

Why Edge-TTS?
- Free, no API key needed
- Has real Nepali voices (Sagar and Hemkala)
- Natural sounding, not robotic
- No complex installation

Why NOT HuggingFace Spaces?
- Gradio version conflicts with Docker mode
- jinja2 template errors across all tested versions
- Gradio SDK mode also had issues
- Current solution: run locally and share with gradio.live link

---

## Known Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| WER 78.6% still high | Only 256 training samples | Record 500+ samples |
| Gradio link expires after 72 hours | Free gradio.live limitation | Run script again for new link |
| HF Spaces not working | Gradio version conflicts | To be fixed in Phase 6 |
| Whisper sometimes mishears | Short or silent recording | Speak clearly for 2+ seconds |

---

## Phase 6 Plan (Next Steps)

### Phase 6A — Record More Data
- Target: 500+ recordings (need 250 more)
- Record using Audacity and RODE NT1
- Same format: 16kHz mono WAV
- Update metadata_all.csv after recording
- Push to GitHub after each session
- Retrain Whisper — expect WER below 50%

### Phase 6B — Train Your Own Voice (VITS)
- Need 30+ minutes of clean audio (currently about 20 minutes)
- Use Google Colab for free GPU
- Train Coqui VITS model on your Nepali recordings
- Your actual voice will speak the AI responses

### Phase 6C — Fix HuggingFace Spaces
- Find stable Gradio version that works on HF Spaces
- Get permanent public URL that never expires
- No more restarting the script every 72 hours

### Phase 6D — Community Features
- Multi-dialect support (Newari, Maithili, Tamang)
- Mobile-optimized interface
- Offline mode (no internet required)
- Open dataset release for other researchers

---

## Project Links

- GitHub: https://github.com/nepaman/nepali-voice-ai-pilot
- HuggingFace Model: https://huggingface.co/nepaman/whisper-nepali-tiny
- HuggingFace Spaces: https://huggingface.co/spaces/nepaman/nepali-voice-ai (under repair)
- Anthropic Console: https://console.anthropic.com
- HuggingFace Profile: https://huggingface.co/nepaman

---

## How to Share the Demo with Friends and Family

Step 1: Start the app
```bash
cd ~/Documents/nepali-voice-ai-pilot
source venv/bin/activate
python scripts/nepali_conversation.py
```

Step 2: Look for this line in the terminal:
Running on public URL: https://xxxxxxxx.gradio.live

Step 3: Copy that link and share it via WhatsApp or iMessage.

Step 4: Your friends open it in their browser on any device.

Step 5: They can type Nepali or click microphone to speak Nepali.
After clicking Submit they press the Play button to hear the response.

Note: The link works for 72 hours. After that run the script again for a new link.

---

For the Nepali language, for the Nepali community.
Nepali bhasako lagi, Nepali samudayako lagi.