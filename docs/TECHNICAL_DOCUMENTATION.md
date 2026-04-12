# Nepali Voice AI — Complete Technical Documentation

## Project Overview

This project builds a community-owned, open-source Nepali Voice AI system.
It combines speech recognition, AI conversation, and text-to-speech into one pipeline.

---

## System Architecture

```
User speaks/types Nepali
        |
        v
Whisper STT (Speech-to-Text)
- Fine-tuned on 256 Nepali recordings
- Converts Nepali audio to Nepali text
        |
        v
Claude AI (Anthropic)
- Understands the Nepali text
- Generates intelligent Nepali response
- Knows about the project and Nepal
        |
        v
Edge-TTS (Text-to-Speech)
- Converts Nepali text to spoken audio
- Male voice: ne-NP-SagarNeural
- Female voice: ne-NP-HemkalaNeural
        |
        v
User hears Nepali response
```

---

## Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Speech Recognition | OpenAI Whisper (fine-tuned) | Convert Nepali speech to text |
| AI Brain | Anthropic Claude claude-opus-4-5 | Understand and respond in Nepali |
| Text to Speech | Microsoft Edge-TTS | Speak Nepali responses |
| Web Interface | Gradio | User interface |
| Audio Processing | librosa, soundfile | Process WAV audio files |
| Training Framework | HuggingFace Transformers | Fine-tune Whisper model |

---

## Phase History

### Phase 1 — Project Setup
- Created project structure
- Set up Python virtual environment
- Installed dependencies
- Bought RODE NT1 5th Gen microphone

### Phase 2 — First Recordings
- Recorded first 50 Nepali audio samples
- Created metadata CSV format
- Tested basic STT pipeline

### Phase 3 — Whisper Fine-tuning (151 samples)
- Recorded 151 clean Nepali WAV files
- Prepared HuggingFace dataset format (80/20 train/test split)
- Fine-tuned openai/whisper-tiny on Nepali
- Pushed model to HuggingFace Hub: nepaman/whisper-nepali-tiny
- Baseline WER: 211.5% (before fine-tuning)
- Fine-tuned WER: ~90% (after Phase 3)

### Phase 4 — More Data + Retrain (256 samples)
- Deleted bad recordings (hum noise from Phase 3)
- Re-recorded NP_151 to NP_256 using Audacity + RODE NT1
- Fixed metadata_all.csv to match 256 audio files
- Archived old metadata files (metadata.csv, metadata_v2.csv, metadata_curated.csv)
- Archived old audio folders (audio_cleaned, audio_normalized)
- Retrained Whisper on 256 samples
- Final WER: 78.6% (improvement: 132.8% over baseline)
- Pushed updated model to HuggingFace Hub

### Phase 5 — Voice Conversation App
- Built full conversation pipeline
- Integrated Claude AI for intelligent Nepali responses
- Added Edge-TTS for natural Nepali voice output
- Two tabs: voice input and text input
- Male and female voice selector
- Conversation history display
- Deployed locally with Gradio share=True (72hr public link)
- Deployed permanently on HuggingFace Spaces

---

## File Structure

```
nepali-voice-ai-pilot/
|
|-- data/
|   |-- audio/                    # Master audio folder (256 WAV files)
|   |   |-- NP_001.wav to NP_256.wav
|   |
|   |-- metadata_all.csv          # Master metadata (filename, transcript, romanized)
|   |-- datasets/                 # HuggingFace format train/test splits
|   |-- _archive/                 # Old files kept for reference
|   |-- transcripts/              # Transcript files
|
|-- models/
|   |-- whisper-nepali/           # Fine-tuned Whisper model
|       |-- model.safetensors     # Model weights
|       |-- config.json           # Model config
|       |-- vocab.json            # Tokenizer vocabulary
|       |-- tokenizer.json        # Tokenizer
|       |-- generation_config.json
|       |-- test_results.json     # WER test results
|
|-- scripts/
|   |-- prepare_dataset.py        # Step 1: Prepare data for training
|   |-- finetune_whisper.py       # Step 2: Fine-tune Whisper model
|   |-- test_finetuned.py         # Step 3: Test and compare models
|   |-- nepali_conversation.py    # Phase 5: Full conversation app
|   |-- record_batch.py           # Recording helper script
|
|-- hf_space/                     # HuggingFace Spaces deployment
|   |-- app.py                    # Spaces app (server version)
|   |-- requirements.txt          # Pinned dependencies
|   |-- Dockerfile                # Docker container config
|   |-- README.md                 # Spaces README
|
|-- docs/                         # Phase documentation
|-- .env                          # API keys (NEVER commit this)
|-- .gitignore                    # Excludes .env, models, venv
|-- README.md                     # Project README
```

---

## Data Format

### Audio Files
- Format: WAV (16-bit)
- Sample Rate: 16000 Hz (16kHz)
- Channels: Mono
- Naming: NP_001.wav to NP_256.wav
- Recorded with: RODE NT1 5th Gen microphone
- Software: Audacity

### Metadata CSV (data/metadata_all.csv)
```
filename,transcript,romanized
NP_001.wav,नमस्कार,Namaskar
NP_002.wav,नमस्ते,Namaste
...
```

### Recording Categories
- Numbers: एक, दुई, तीन... (1 to 1000)
- Greetings: नमस्ते, शुभ प्रभात...
- Daily phrases: खाना खानु भयो?, कस्तो छ?...
- Commands: बन्द गर्नुहोस्, सुन्नुहोस्...
- Days and Time: सोमबार, बिहान, साँझ...
- Family: आमा, बुवा, दाइ, दिदी...
- Places: काठमाडौं, पोखरा, हिमालय...
- Food: दाल भात, रोटी, चिया...
- Full sentences: conversational Nepali

---

## Training Pipeline

### Step 1: Prepare Dataset
```bash
python scripts/prepare_dataset.py
```
What it does:
- Reads metadata_all.csv
- Loads each WAV file
- Resamples to 16kHz if needed
- Splits 80% train / 20% test
- Saves to data/datasets/whisper_finetune/

### Step 2: Fine-tune Whisper
```bash
python scripts/finetune_whisper.py
```
What it does:
- Loads openai/whisper-tiny as base model
- Uses Apple M1 GPU (MPS) for acceleration
- Trains for 20 epochs
- Batch size: 4 (effective 8 with gradient accumulation)
- Evaluates WER every 100 steps
- Saves best model to models/whisper-nepali/

### Step 3: Test Results
```bash
python scripts/test_finetuned.py
```
What it does:
- Loads fine-tuned model
- Loads baseline whisper-small for comparison
- Tests on 51 test samples
- Calculates WER for both models
- Shows side-by-side comparison
- Saves results to models/whisper-nepali/test_results.json

### Step 4: Push to HuggingFace Hub
```python
from transformers import WhisperForConditionalGeneration, WhisperProcessor
model = WhisperForConditionalGeneration.from_pretrained("models/whisper-nepali")
processor = WhisperProcessor.from_pretrained("models/whisper-nepali")
model.push_to_hub("nepaman/whisper-nepali-tiny")
processor.push_to_hub("nepaman/whisper-nepali-tiny")
```

---

## Conversation App Pipeline (scripts/nepali_conversation.py)

### Step 1: Transcription (Speech to Text)
```python
def transcribe_audio(audio):
    # Load audio with librosa at 16kHz
    # Run through Whisper processor
    # Generate transcription
    # Return Nepali text string
```

### Step 2: AI Response (Claude)
```python
def get_claude_response(user_text):
    # Add user message to history
    # Send to Claude with Nepali system prompt
    # Clean response (remove markdown symbols)
    # Add to history for context
    # Return Nepali response text
```

### Step 3: Text to Speech (Edge-TTS)
```python
async def speak_async(text, voice_name):
    # Choose voice: Sagar (male) or Hemkala (female)
    # Generate MP3 audio file
    # Return file path
```

### Step 4: Full Pipeline
```python
def conversation(audio, voice):
    user_text = transcribe_audio(audio)       # Step 1
    ai_text   = get_claude_response(user_text) # Step 2
    audio     = speak(ai_text, voice)          # Step 3
    return user_text, audio, chat_history
```

---

## API Keys and Secrets

### Local Development (.env file)
```
ANTHROPIC_API_KEY=sk-ant-your-key-here
```
Never commit .env to GitHub. It is listed in .gitignore.

### HuggingFace Spaces
Add ANTHROPIC_API_KEY as a secret at:
https://huggingface.co/spaces/nepaman/nepali-voice-ai/settings
Under "Variables and secrets" section.

---

## Model Performance

| Phase | Samples | WER | Notes |
|-------|---------|-----|-------|
| Baseline | 0 | 211.5% | openai/whisper-small, no fine-tuning |
| Phase 3 | 151 | ~90% | First fine-tune |
| Phase 4 | 256 | 78.6% | Re-recorded with RODE NT1 |
| Phase 6 target | 500+ | below 50% | Planned |

WER = Word Error Rate. Lower is better. 0% = perfect transcription.

---

## Key Decisions Made

### Why Whisper Tiny?
- Small enough to run on Mac M1 without GPU
- Fast inference for real-time conversation
- Good base for fine-tuning with limited data
- Can upgrade to whisper-small when more data is available

### Why Claude for AI Brain?
- Best understanding of Nepali context
- Maintains conversation history across turns
- Can be customized with system prompts
- Reliable API with good Nepali language support

### Why Edge-TTS for Voice?
- Free, no API key needed
- Has real Nepali voices (Sagar and Hemkala)
- Natural sounding, not robotic
- No complex installation unlike XTTS

### Why Gradio for Interface?
- Simple to build and maintain
- Works in any browser
- share=True gives instant 72-hour public link
- Supports audio input and output natively

### Why NOT HuggingFace Spaces SDK mode?
- Too many dependency conflicts with newer Gradio versions
- Docker mode gives full control over dependencies
- Can pin exact package versions to avoid conflicts

---

## Known Issues and Limitations

| Issue | Cause | Fix |
|-------|-------|-----|
| WER 78.6% is high | Only 256 training samples | Record 500+ samples in Phase 6 |
| No autoplay on shared links | Browser security restriction | User must press play manually |
| Hindi accent in XTTS | Nepali not supported by XTTS | Train VITS model in Phase 6 |
| Whisper hallucinates sometimes | Short or silent audio input | Add silence detection |
| HF Spaces uses CPU not GPU | Free tier limitation | Acceptable for now |

---

## Working Dependencies

### Local Mac M1 (venv)
```
torch==2.4.0
torchaudio==2.4.0
torchvision==0.19.0
transformers==4.45.0
gradio==3.50.2
gradio-client==0.6.1
anthropic==0.94.0
edge-tts==6.1.9
gtts==2.5.1
librosa==0.10.1
soundfile==0.12.1
python-dotenv==1.0.0
```

### HuggingFace Spaces (Docker Python 3.11)
```
gradio==3.39.0
torch==2.1.0
torchaudio==2.1.0
transformers==4.40.0
anthropic==0.94.0
edge-tts==6.1.9
gtts==2.5.1
librosa==0.10.1
soundfile==0.12.1
python-dotenv==1.0.0
numpy<2
anyio==3.7.1
```

---

## Useful Commands Reference

### Run conversation app locally
```bash
cd ~/Documents/nepali-voice-ai-pilot
source venv/bin/activate
python scripts/nepali_conversation.py
```

### Check audio and metadata counts match
```bash
ls data/audio/NP_*.wav | wc -l
tail -n +2 data/metadata_all.csv | wc -l
```

### Listen to a recording
```bash
afplay data/audio/NP_001.wav
```

### Check available microphones
```bash
python3 -c "import sounddevice as sd; print(sd.query_devices())"
```

### Push model to HuggingFace Hub
```bash
python3 -c "
from transformers import WhisperForConditionalGeneration, WhisperProcessor
model = WhisperForConditionalGeneration.from_pretrained('models/whisper-nepali')
processor = WhisperProcessor.from_pretrained('models/whisper-nepali')
model.push_to_hub('nepaman/whisper-nepali-tiny')
processor.push_to_hub('nepaman/whisper-nepali-tiny')
"
```

### Push code to GitHub
```bash
git add .
git commit -m "your message here"
git push origin main
```

### Push to HuggingFace Spaces
```bash
cd hf_space
git add .
git commit -m "your message"
git push origin main
```

---

## Phase 6 Plan (Next Steps)

### Phase 6A — More Data
- Target: 500+ recordings (need 250 more)
- Record using Audacity + RODE NT1
- Same format: 16kHz mono WAV
- Update metadata_all.csv after each session
- Push to GitHub after each session
- Retrain Whisper — expect WER below 60%

### Phase 6B — Train Custom Voice (VITS)
- Need 30+ minutes of clean audio (currently ~20 mins)
- Use Google Colab free GPU
- Train Coqui VITS model on your Nepali recordings
- Export voice model file
- Replace Edge-TTS with your own voice

### Phase 6C — Integration
- Plug VITS model into conversation app
- Your voice speaks the AI responses
- Deploy updated version to HF Spaces

### Phase 6D — Community Features
- Multi-dialect support (Newari, Maithili, Tamang)
- Mobile-optimized interface
- Offline mode (no internet required)
- Open dataset release for community use

---

## Project Links

- GitHub: https://github.com/nepaman/nepali-voice-ai-pilot
- HuggingFace Model: https://huggingface.co/nepaman/whisper-nepali-tiny
- HuggingFace Spaces: https://huggingface.co/spaces/nepaman/nepali-voice-ai
- Anthropic Console: https://console.anthropic.com
- HuggingFace Profile: https://huggingface.co/nepaman

---

Last updated: April 2026
Project status: Phase 5 complete, Phase 6 in progress
For the Nepali language, for the Nepali community.