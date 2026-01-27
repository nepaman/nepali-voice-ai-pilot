# Nepali Voice AI - Complete Project Reset

## Date: January 23, 2026
## Author: Gyanendra Maharjan
## Status: Foundation Phase - Starting Fresh

---

## Why We're Resetting

After initial exploration with ChatGPT, we encountered multilingual issues with STT. We pivoted to TTS-first approach, but after strategic review with Claude, we've determined that:

1. **STT-first is more feasible** for a solo non-developer
2. **The multilingual issue was solvable** with simple configuration
3. **Quick wins are essential** for motivation and learning
4. **Proper documentation** will prevent future confusion

---

## Previous Learnings (What We Keep)

✅ Understanding that we DON'T need to record every word for TTS
✅ Rejection of SaaS platforms for core functionality  
✅ Commitment to open-source and model ownership
✅ Phase-based development approach
✅ Community-first mindset
✅ Professional documentation standards

---

## New Strategic Direction

### Development Sequence

**Phase 0: Foundation (Current)** - Weeks 1-2
- Clean repository structure
- Set up development environment
- Create comprehensive documentation
- Install basic tools

**Phase 1: STT Demo (Quick Win)** - Weeks 3-4
- Implement Nepali Speech-to-Text using Whisper
- Fix multilingual issue with language parameter
- Create simple test scripts
- Record 10 test sentences

**Phase 2: Basic TTS Integration** - Weeks 5-6
- Add simple TTS using existing libraries (gTTS or Coqui)
- Connect STT → TTS for complete loop
- Create web demo interface
- Test with community

**Phase 3: Voice Dataset Collection** - Weeks 7-12
- Record 100+ sentences while system runs
- Organize and label audio files
- Build dataset incrementally
- Continue improving STT accuracy

**Phase 4: Custom TTS Training** - Weeks 13-20
- Train custom voice model with collected data
- Fine-tune for natural Nepali pronunciation
- Replace generic TTS with custom model

**Phase 5: Web Application** - Weeks 21-24
- Build proper web interface
- Deploy publicly
- Gather community feedback

---

## Key Principle: Document Everything

Every step will be documented in real-time:
- Daily learning logs
- Code with detailed comments
- Decision rationale
- Problems encountered and solutions
- Progress metrics

---

## Technical Foundation Decisions

### Primary Tools
- **Language:** Python 3.9+
- **STT Model:** OpenAI Whisper (small or base model)
- **TTS Model:** gTTS (initial) → Coqui TTS (custom)
- **Web Framework:** Gradio (prototyping) → FastAPI (production)
- **Audio Recording:** Audacity
- **Microphone:** RØDE NT1 (5th Gen)

### Development Environment
- **OS:** [Your operating system]
- **IDE:** VS Code (recommended) or your choice
- **Version Control:** Git + GitHub
- **Virtual Environment:** Python venv

---

## Repository Structure (New)

```
nepali-voice-ai-pilot/
│
├── README.md                          # Main project overview
├── CHANGELOG.md                       # Track all changes
├── LICENSE                            # To be decided
├── requirements.txt                   # Python dependencies
├── .gitignore                        # Exclude unnecessary files
│
├── docs/                              # All documentation
│   ├── 00_PROJECT_RESET.md           # This document
│   ├── 01_SETUP_GUIDE.md             # Installation instructions
│   ├── 02_LEARNING_LOG.md            # Daily/weekly progress
│   ├── 03_TECHNICAL_DECISIONS.md     # Why we chose what
│   ├── 04_TROUBLESHOOTING.md         # Common issues & fixes
│   └── 05_RESOURCES.md               # Helpful links & references
│
├── scripts/                           # Python scripts
│   ├── setup/                        # Environment setup scripts
│   ├── stt/                          # Speech-to-Text scripts
│   ├── tts/                          # Text-to-Speech scripts
│   └── utils/                        # Helper functions
│
├── data/                              # All datasets
│   ├── audio/                        # Audio files
│   │   ├── raw/                      # Original recordings
│   │   ├── processed/                # Cleaned audio
│   │   └── test/                     # Test samples
│   ├── transcripts/                  # Text transcriptions
│   └── datasets/                     # Training datasets
│
├── models/                            # Trained models
│   ├── stt/                          # STT models
│   ├── tts/                          # TTS models
│   └── checkpoints/                  # Training checkpoints
│
├── web/                               # Web application
│   ├── app.py                        # Main application
│   ├── static/                       # CSS, JS, images
│   └── templates/                    # HTML templates
│
└── tests/                             # Test scripts
    ├── test_stt.py
    └── test_tts.py
```

---

## Immediate Next Steps

### Today (Day 1):
1. ✅ Read and understand this reset document
2. ✅ Back up any existing work locally
3. ✅ Confirm commitment to new direction
4. ✅ Set up proper workspace on computer

### Tomorrow (Day 2):
1. Clean GitHub repository
2. Create new folder structure
3. Add all documentation templates
4. Commit with message: "Project reset - new foundation"

### Day 3:
1. Install Python and verify installation
2. Set up virtual environment
3. Install basic dependencies
4. Test installation with simple script

### Day 4:
1. Install Whisper
2. Run first Nepali transcription test
3. Document results

---

## Success Metrics for Phase 0

By end of Week 2, you should have:
- ✅ Clean, organized GitHub repository
- ✅ Complete documentation structure
- ✅ Working Python environment
- ✅ Whisper installed and tested
- ✅ First Nepali audio transcribed successfully
- ✅ Detailed learning log documenting journey

---

## Commitment Statement

I, Gyanendra Maharjan, commit to:
- Following this structured approach
- Documenting every step
- Asking questions when stuck
- Completing Phase 0 before moving forward
- Being patient with the learning process
- Celebrating small wins

**Date:** _____________
**Signature/Note:** _____________

---

## Notes Section (For Your Use)

Use this space to add thoughts, questions, or observations:

```
[Space for your notes]
```

---

**Next Document to Create:** `01_SETUP_GUIDE.md`