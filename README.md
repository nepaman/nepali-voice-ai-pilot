# 🇳🇵 Nepali Voice AI — Pilot Project

> A personal pilot project building Speech-to-Text (STT) and Text-to-Speech (TTS) for everyday conversational Nepali — an underrepresented language in voice AI.

---

## Overview

Nepali Voice AI is a solo, non-commercial pilot focused on improving Nepali language representation in voice-based AI systems. Built with open-source tools and a learning-first approach, the goal is to create a foundation that can grow with community contributions.

---

## Project Goals

- Build a working Nepali Speech-to-Text (STT) prototype
- Build a natural Nepali Text-to-Speech (TTS) voice
- Focus on daily, conversational Nepali (informal or literary)
- Learn and document the full AI development process
- Create a foundation that can scale with community contributions

---

## Current Status — Phase 2 Complete

### Phase 1 — STT Baseline (Complete)
- Recorded 151 single-speaker audio clips (NP_001–NP_150)
- Built and tested Whisper STT baseline
- Created metadata CSVs and transcript files
- Established project structure and documentation

### Phase 2 — Voice Loop Demo (Complete)
- Built a full voice loop: **Speak Nepali → Transcribe → Respond → Speak back**
- Integrated Whisper `small` model for live Nepali transcription
- Recorded 6 personal voice responses (greeting, morning, thanks, goodnight, how are you, default)
- Built Gradio 6.x web demo (`voice_loop_demo.py`)
- Implemented phonetic keyword matching for Whisper's Nepali output variations
- Added hallucination detection for short/silent audio inputs

**Supported phrases (Phase 2 demo):**

| Say | Response |
|-----|----------|
| नमस्ते / नमस्कार | Greeting response |
| शुभ प्रभात | Good morning response |
| धन्यवाद | Thank you response |
| शुभ रात्रि | Good night response |
| कस्तो छ | How are you response |

---

## Running the Demo

### Requirements

```bash
pip install gradio openai-whisper gtts
```

### Run

```bash
cd scripts/Demo
python voice_loop_demo.py
```

Open **http://127.0.0.1:7860** in your browser.

1. Click the microphone button
2. Speak in Nepali
3. Stop recording — response plays automatically in your voice

---

## Project Structure

```
nepali-voice-ai-pilot/
│
├── data/
│   ├── audio/              # 151 raw WAV recordings (NP_001–NP_150)
│   ├── audio_cleaned/      # Cleaned audio
│   ├── audio_normalized/   # Normalized audio
│   ├── transcripts/        # Nepali text transcripts
│   ├── datasets/           # Processed datasets
│   ├── metadata.csv        # Full metadata
│   ├── metadata_curated.csv
│   ├── metadata_all.csv
│   └── metadata_v2.csv
│
├── scripts/
│   └── Demo/
│       ├── voice_loop_demo.py       # Phase 2 Gradio demo
│       └── response_audio/          # 6 recorded voice responses
│           ├── greeting_response.wav
│           ├── morning_response.wav
│           ├── thanks_response.wav
│           ├── goodnight_response.wav
│           ├── howru_response.wav
│           └── default_response.wav
│
├── docs/
│   ├── 00_PROJECT_RESET.md
│   ├── 01_SETUP_GUIDE.md
│   ├── 02_LEARNING_LOG.md
│   ├── 03_FIRST_STT_TEST.md
│   ├── PHASE1_FINAL_REPORT.md
│   ├── PROJECT_DOCUMENTATION.md
│   ├── TECHNICAL_REPORT_PHASE1.md
│   └── TECHNICAL_SETUP_GUIDE.md
│
├── models/                 # Trained model checkpoints (future)
└── README.md
```

---

## Technology Stack

| Component | Tool |
|-----------|------|
| Language | Python 3.10 |
| Speech-to-Text | OpenAI Whisper (small) |
| Text-to-Speech | Personal recorded voice + gTTS fallback |
| Demo UI | Gradio 6.x |
| Microphone | RØDE NT1 (5th Gen) |
| Audio editing | Audacity |

---

## Roadmap

| Phase | Goal | Status |
|-------|------|--------|
| Phase 1 | Record dataset, STT baseline | Complete |
| Phase 2 | Voice loop demo, recorded responses | Complete |
| Phase 3 | Fine-tune Whisper on Nepali dataset | Planned |
| Phase 4 | Train Coqui/VITS TTS on personal voice | Planned |
| Phase 5 | Public demo, community contributions | Planned |

---

## Scope

### Included
- Single-speaker voice dataset
- STT using Whisper with Nepali phonetic matching
- Pre-recorded personal voice responses
- Simple local web demo

### Not Included (yet)
- Commercial deployment
- Mobile applications
- Multi-speaker or multi-accent support
- Real-time fine-tuned model inference

---

## Contribution

This is currently a solo pilot initiative. Documentation and datasets may be shared openly in later phases. Feedback and suggestions are welcome.

---

## License

License to be decided. Likely an open-source, research-friendly license.

---

*Building Nepali voice AI — one phrase at a time. 🇳🇵*