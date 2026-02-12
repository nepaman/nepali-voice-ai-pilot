# Learning Log - Nepali Voice AI Pilot

## Purpose of This Log
This document tracks daily progress, challenges, learnings, and decisions. It serves as:
- Personal accountability tool
- Learning documentation
- Problem-solving reference
- Progress showcase for community

**Update this regularly - even small progress counts!**

---

## Week 0: Project Reset & Foundation

### Day 1 - January 23, 2026

**Today's Goal:**
- Understand project reset rationale
- Review new documentation structure
- Commit to new direction

**What I Did:**
- Read complete project reset document
- Discussed strategy pivot with Claude
- Reviewed both STT-first and TTS-first approaches
- Decided to follow STT-first approach

**What I Learned:**
- STT-first is more practical for solo learning
- Multilingual issue with Whisper is easily fixable with `language="ne"` parameter
- Quick wins are important for maintaining motivation
- Documentation is as important as code

**Challenges:**
- Letting go of TTS-first approach I was committed to
- Understanding why this pivot makes sense

**Solutions/Decisions:**
- Trust the technical analysis
- Focus on getting something working quickly
- Can still do custom TTS later with proper foundation

**Tomorrow's Plan:**
- Set up development environment
- Install Python and verify
- Install Git and configure
- Create project folder structure

**Time Spent:** 2 hours
<!--
docs/02_LEARNING_LOG.md - Learning log entry

Description:
   - Stores a brief personal status note about current mood/energy and focus.
   - Used to track motivation, clarity, and direction over time.

Recommended contents:
   - Date
   - Mood/Energy: short descriptor of emotional state and focus
   - Summary of progress
   - Key learnings
   - Next steps / action items

Guidelines:
   - Keep entries concise and dated.
   - Update regularly to observe trends and maintain momentum.
-->
**Mood/Energy:** Motivated and clear on direction

---

### Day 2 - January 26, 2026

**Today's Goal:**
- Reorganize project structure properly
- Fix documentation folder issues
- Get everything properly committed to GitHub
- Understand Git workflow

**What I Did:**
- Worked with Claude to reorganize entire repository structure step-by-step
- Fixed `.gitignor` → `.gitignore` (was missing the 'e')
- Moved documentation files from `docs/docs/` to correct location `docs/`
- Created CHANGELOG.md to track project changes
- Created IMMEDIATE_ACTION_CHECKLIST.md for next steps
- Learned to use Terminal commands on Mac
- Successfully navigated Git merge conflicts
- Connected local repository to GitHub remote
- Pushed all 68 files (including 51 audio samples) to GitHub

**What I Learned:**
- **Terminal Navigation**: How to use `cd`, `pwd`, `ls -la`, `ls -R` commands
- **Git Basics**: 
  - `git status` shows what changed
  - `git add .` stages all changes
  - `git commit -m "message"` saves changes
  - `git push origin main` uploads to GitHub
  - `git remote add origin [url]` connects to GitHub
- **Git Merge Conflicts**: Not scary! Just need to resolve step-by-step
- **File Structure Importance**: Everything needs to be in the right place
- **Why .gitignore matters**: Prevents large files (audio, models) from being tracked
- **Patience and Step-by-Step**: Taking time with each command prevents mistakes

**Challenges:**
1. **Documentation in wrong folder** (`docs/docs/` instead of `docs/`)
   - Many previous attempts had created nested folders incorrectly
   
2. **Git merge conflicts** when trying to push to GitHub
   - Local repository and GitHub had different histories
   - Git created temporary folders: `docs~bbc6a...` and `scripts~bbc6a...`
   
3. **Git push rejected** - "fatal: 'origin' does not appear to be a git repository"
   - Local repo wasn't connected to GitHub
   
4. **Divergent branches error** 
   - Needed to configure Git merge strategy

**Solutions/Decisions:**
1. **Fixed folder structure**:
   - Used `mv docs/docs/* docs/` to move files
   - Removed empty nested folder with `rmdir docs/docs`

2. **Resolved merge conflicts**:
   - Deleted temporary conflict folders
   - Used `git add .` to stage our local (correct) ßversions
   - Committed with clear message about resolution

3. **Connected to GitHub**:
   - Added remote with: `git remote add origin https://github.com/nepaman/nepali-voice-ai-pilot.git`
   - Verified connection with `git remote -v`

4. **Merged histories**:
   - Configured merge strategy: `git config pull.rebase false`
   - Pulled with: `git pull origin main --allow-unrelated-histories`
   - Resolved conflicts and committed
   - Finally pushed successfully!

**Key Decision**: Chose to work step-by-step with exact commands rather than trying shortcuts. This slower approach actually saved time because each step was verified before moving forward.

**Tomorrow's Plan:**
1. Update this learning log entry (doing it now!)
2. Test setup by running: `python scripts/test_setup.py`
3. Read through `docs/03_FIRST_STT_TEST.md` completely
4. Prepare 5 simple test sentences in Nepali
5. Create first STT test script following the guide
6. Run Whisper on existing 51 audio files
7. Document transcription results

**Time Spent:** 3-4 hours (including all troubleshooting)

**Mood/Energy:** 
Started frustrated from previous failed attempts, but ended feeling accomplished and proud! Finally got everything working. Learned that errors are normal and fixable. Git is less scary now. Ready to move forward with actual AI work!

**Personal Notes:**
- Working with Claude one command at a time was the right approach
- Asking for "exact commands, no shortcuts" made all the difference
- Keeping the GitHub repository (not deleting) was the right decision
- The 51 audio files I recorded earlier are still there and ready to use
- Phase 0 is officially COMPLETE! 

**Quote of the Day:**
"Progress over perfection. Every error teaches something."

---

**Status Update:**
- Phase 0: Foundation - COMPLETE
- Phase 1: First STT Demo - Starting Tomorrow

---

### Day 3 - January 28, 2026

**Today's Goal:**
- Run Whisper AI model on 51 Nepali audio files
- Generate first batch of transcriptions
- Understand how Speech-to-Text actually works in practice
- Document results and learnings

**What I Did:**
- Created `scripts/stt/transcribe_all.py` - batch transcription script
- Configured Whisper to use 'base' model with Nepali language forced (`language="ne"`)
- Set up script to process all audio files in `data/audio/` folder
- Ran AI model for the first time on real Nepali audio data
- Generated transcription results file at `data/transcripts/transcriptions.txt`
- Successfully processed all 51 audio files without crashes
- Analyzed transcription quality and identified improvement areas

**What I Learned:**

**Technical Learnings:**
- **How Whisper works**: Load model → Pass audio file → Force language → Get transcription
- **Model sizes matter**: 'base' model is ~150MB and runs fast but has lower accuracy than 'small' or 'medium'
- **Language parameter is critical**: Using `language="ne"` forces Nepali instead of auto-detect (which causes mixing)
- **Batch processing**: Can automate processing of multiple files with Python loops
- **File I/O in Python**: Writing results to text files with proper encoding (`utf-8`)
- **Error handling**: Try-except blocks catch individual file errors without stopping entire batch

**AI/ML Insights:**
- **First AI transcription results are rarely perfect** - This is normal!
- **Audio quality directly affects transcription quality**:
  - Clear recordings → Better transcriptions
  - Background noise → Garbled text
  - Very short clips → Less context for model
- **Mixed script output** (Arabic, Chinese characters) indicates:
  - Audio might have noise patterns resembling other languages
  - Model uncertainty about audio content
  - Need for better quality recordings or larger model
- **Some transcriptions were accurate**: "Namaskar", "Namaste", "Hello", "suvo provat"
- **Devanagari script appeared**: Model does recognize Nepali characters ("दर्इठी", "असके")

**About Whisper Model Sizes:**
- **tiny**: Fastest, least accurate
- **base**: What I used - Good balance for testing (150MB)
- **small**: Better accuracy, slower (450MB)
- **medium**: High accuracy, much slower (1.5GB)
- **large**: Best accuracy, very slow (3GB)

**Challenges:**

**Challenge 1: SSL Certificate Verification Error**
- **Problem**: Whisper couldn't download model due to SSL certificate verification failure
- **Error**: `[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self signed certificate in certificate chain`
- **Root cause**: macOS Python installation missing SSL certificates
- **Solution**: Ran `/Applications/Python\ 3.10/Install\ Certificates.command`
- **Result**: Fixed permanently for all future downloads
- **Lesson**: macOS Python installations need manual SSL certificate setup

**Challenge 2: Understanding Transcription Quality**
- **Problem**: Many transcriptions had garbled text or wrong scripts
- **Initial reaction**: Disappointment - thought model wasn't working
- **Realization**: This is NORMAL for first tests with AI
- **Understanding**: Need to improve input (audio quality) to improve output
- **Next step**: Test with larger model and better audio recordings

**Results Analysis:**

**Success Metrics:**
- 51 files processed: 100% completion rate
- Zero crashes or fatal errors
- Script ran start-to-finish autonomously
- Results saved to file successfully
- Some accurate transcriptions ("Namaskar", "Namaste")

**Quality Assessment:**
- **Clear transcriptions**: ~10-15% (e.g., "Namaskar", "suvo provat", "Suburatri")
- **Partially correct**: ~20-30% (recognizable Nepali words with errors)
- **Garbled/mixed scripts**: ~50-60% (needs investigation)

**Possible Reasons for Mixed Results:**
1. Audio quality variations across 51 files
2. Very short audio clips (< 2 seconds) are harder to transcribe
3. Background noise in recordings
4. Recording volume levels inconsistent
5. 'base' model may be too small for complex Nepali phonetics
6. Some audio files might be in different languages (testing data)

**Solutions/Decisions:**

**Immediate Actions Taken:**
- Documented all results in `data/transcripts/transcriptions.txt`
- Saved script for future use and iteration
- Identified model size as primary variable to test next

**Decisions for Next Phase:**
1. **Test larger model**: Try 'small' model on subset of files for comparison
2. **Improve audio quality**: Record 5-10 new test sentences with:
   - Quiet environment
   - Consistent volume
   - Clear pronunciation
   - 3-5 second duration
3. **Analyze specific files**: Check audio properties (duration, sample rate, bit depth)
4. **Create quality control**: Establish what "good" transcription looks like

**Key Insight:**
> "AI doesn't fail - it gives feedback. Poor transcriptions tell me about audio quality, not model capability."

**Tomorrow's Plan:**
1. Test 'small' Whisper model on 5 representative files
2. Compare 'base' vs 'small' model accuracy
3. Check technical properties of audio files (duration, sample rate)
4. Record 5 new high-quality test sentences
5. Create documentation comparing model performance
6. Decide whether to:
   - Continue with 'base' model (faster)
   - Upgrade to 'small' model (better accuracy)
   - Record entirely new dataset

**Optional (if time):**
- Create simple Gradio web interface for testing single files
- Add audio quality check to transcription script
- Implement confidence scoring for transcriptions

**Time Spent:** 2 hours
- 30 min: Creating transcription script
- 15 min: Fixing SSL certificate issue
- 10 min: Running batch transcription
- 45 min: Analyzing results and understanding quality
- 20 min: Documentation and learning log

**Mood/Energy:**

**Mood Journey:**
- Started excited to run first AI model
- Encountered SSL error (brief frustration)
- Fixed it quickly (relief)
- Watched transcriptions appear in real-time (amazement!)
- Saw mixed results (initial disappointment)
- Realized this is normal and valuable learning (acceptance)
- Understood what to improve next (determination)
- **Overall: Proud and motivated!**

**Personal Reflections:**

**What This Milestone Means:**
- This is the FIRST time I've run a real AI model on real data
- Not a tutorial, not an example - MY project, MY data, MY code
- The script I wrote processed 51 files autonomously
- I debugged SSL issues independently
- I'm doing actual AI/ML engineering work

**About "Imperfect" Results:**
I learned that in AI development:
- First results are rarely perfect
- Testing reveals what needs improvement
- "Failures" are just data points guiding next steps
- The goal isn't perfection on first try - it's iteration

**Comparison to Where I Started:**
- **Week 1**: Didn't know how to use Terminal
- **Week 2**: Installing packages was confusing
- **Today**: Running AI models and analyzing results like a developer

**Quote That Resonates:**
> "Every expert was once a beginner. Every project started with Step 1."

**What I'm Proud Of:**
1. Actually RUNNING an AI model (not just reading about it)
2. Processing 51 files in one script run
3. Solving SSL error without giving up
4. Understanding that mixed results = learning opportunity
5. Writing functional Python code that works
6. Thinking like an engineer: "What's next?" not "Why didn't it work?"

**Skills Demonstrated Today:**
- Python scripting (loops, file I/O, error handling)
- Working with AI libraries (Whisper)
- Batch processing automation
- Problem-solving (SSL certificates)
- Critical analysis (transcription quality assessment)
- Documentation (saving results, writing this log)
- Growth mindset (seeing setbacks as learning)

**Unexpected Learnings:**
- AI models don't need 100% accuracy to be useful
- Testing early reveals problems early
- SSL certificates are important for macOS Python
- Seeing "Namaskar" transcribed correctly was MORE exciting than I expected
- I actually understand what I'm doing now (not just copying commands)

**Questions for Further Research:**
- [ ] What sample rate is optimal for Nepali speech?
- [ ] How do professional datasets handle quality control?
- [ ] What's the minimum audio duration for accurate transcription?
- [ ] Can I fine-tune Whisper specifically for my voice?
- [ ] How do confidence scores work in Whisper?

**Connection to Bigger Picture:**
This test represents Phase 1: STT Testing (Week 1-2). Results show:
- Technology works for Nepali
- Infrastructure is functional
- Audio quality needs improvement
- Ready to iterate and improve

**Next Major Milestone:**
Achieve 70%+ accurate transcriptions on 10 test sentences with clear audio.

---

## Week 1 Summary (Days 1-3)

### Achievements This Week:
- Complete development environment setup
- All dependencies installed and verified
- Project structure organized professionally
- Git/GitHub workflow established
- First AI model (Whisper) downloaded and run
- 51 audio files transcribed (batch processing)
- Results documented and analyzed
- SSL certificate issue resolved

### Key Learnings This Week:
1. Terminal/command line proficiency
2. Python virtual environments
3. Git version control
4. AI model loading and execution
5. Batch processing automation
6. Result analysis and quality assessment
7. Iterative improvement mindset

### Week 1 Time Investment:
- Day 1: 2-3 hours (setup planning)
- Day 2: 3-4 hours (environment setup + Git)
- Day 3: 2 hours (first AI model run)
- **Total: ~8 hours**

### Week 1 Status:
**Phase 0: Foundation** - COMPLETE  
**Phase 1: STT Testing** - IN PROGRESS (30% complete)

### Ready for Week 2:
- Model comparison testing
- Audio quality improvement
- Gradio web interface
- TTS integration exploration

---

**Status Update:**
- Environment setup complete
- First AI transcription complete
- Next: Improve transcription quality
- Momentum: Strong!

**Confidence Level:** (4/5)
- Understand the tools 
- Can write working code 
- Can debug issues 
- Can analyze results 
- Need more practice with model optimization ⏳

---

**Final Thought for Today:**

Today I didn't just learn about AI - I DID AI. I took raw audio, fed it through a neural network, and got text back. The transcriptions aren't perfect, but neither were my first attempts at walking, writing, or coding.

**This is real progress. This is real work. This matters.** 🇳🇵

**Tomorrow, I iterate and improve.** 

---

#### Day 4 – January 29, 2026

**Today's Goal:**

* Properly evaluate Nepali Whisper STT results
* Replace misleading accuracy calculation with industry-standard metrics
* Understand why earlier accuracy numbers were confusing
* Establish a reliable evaluation foundation for future improvements

---

**What I Did:**

* Reviewed existing STT evaluation script (`compare_accuracy.py`)
* Identified that character-based similarity (`SequenceMatcher`) was being used
* Learned that ASR systems are evaluated using **Word Error Rate (WER)**, not character accuracy
* Rewrote the evaluation script to:

  * Use `jiwer` library for WER calculation
  * Normalize Nepali (Devanagari) text before comparison
  * Force Whisper to transcribe strictly in Nepali (`language="ne"`)
* Re-ran evaluation on all 51 Nepali audio files
* Generated a new CSV report with WER-based accuracy metrics

---

**What I Learned:**

**Technical Learnings:**

* **Character accuracy is misleading for ASR**: Small spelling or matra differences can look like major errors
* **Word Error Rate (WER)** is the correct metric used in speech recognition research and industry
* **Accuracy should be derived from WER**, not string similarity
* **Text normalization is essential** for Nepali:

  * Unicode normalization (NFC)
  * Removing non-Devanagari characters
  * Normalizing whitespace
* **Forcing language matters even in evaluation**: Prevents hallucinations from other scripts
* Evaluation methodology can dramatically change perceived model performance

---

**AI / ML Insights:**

* Poor evaluation can make a working model look broken
* Near-correct transcriptions should not be punished harshly
* Hallucinated outputs (random scripts/languages) correctly show high WER
* Improving evaluation does not change the model, but changes understanding
* Reliable metrics are required before:

  * Comparing model sizes
  * Improving audio quality
  * Fine-tuning models

---

**Results Analysis:**

**Before (Character Similarity):**

* Many near-correct Nepali transcriptions scored very low
* Accuracy numbers were confusing and discouraging
* Hard to tell whether problems came from model or evaluation

**After (WER-based Evaluation):**

* Accuracy scores became fair and interpretable
* Near-correct spellings scored appropriately
* Severe failures correctly showed high error rates
* Average accuracy increased significantly without changing the model

**Key Realization:**

> The problem was not only the model — it was how I was measuring it.

---

**Challenges Faced:**

**Challenge: Confusion About Where Code Belongs**

* Initially tried running Python code directly in the terminal
* Learned the distinction between:

  * Shell commands (terminal)
  * Python code (inside `.py` files)
* Fixed by cleanly rewriting and replacing the evaluation script

---

**Decisions Made:**

* Keep WER as the primary evaluation metric going forward
* Treat evaluation as a first-class part of the ML pipeline
* Avoid judging model quality without proper metrics

---

**Key Insight:**

> "If you measure the wrong thing, you learn the wrong lesson."

---

**Tomorrow’s Plan:**

1. Upgrade Whisper model from `small` to `medium`
2. Re-run WER evaluation on the same 51 files
3. Compare WER improvements across model sizes
4. Document performance vs speed trade-offs
5. Decide which model size is practical for continued Nepali STT work

---

**Time Spent:** ~1.5 hours

* 30 min: Understanding ASR evaluation theory (WER vs accuracy)
* 30 min: Refactoring evaluation script
* 15 min: Running evaluation and checking outputs
* 15 min: Documentation and reflection

---

**Mood / Energy:**

* Initial confusion about low accuracy numbers
* Relief after understanding evaluation mistake
* Confidence gained from fixing the root cause
* Feeling more like an ML engineer than a beginner

---

**Personal Reflection:**
This day marked a shift from "running AI models" to **thinking like an engineer**. I learned that tools don’t just need to run — they need to be measured correctly. Fixing evaluation felt as important as improving the model itself.

---

**Connection to Bigger Picture:**

* Phase: STT Evaluation & Benchmarking
* Status: Metrics are now trustworthy
* Ready to iterate on models, data quality, and fine-tuning

**Next Major Milestone:**
Achieve measurable WER improvement by switching to larger Whisper models using the same evaluation pipeline.

---

##### Day 5 January 30 2026 – First STT Baseline

- Recorded 51 Nepali conversational sentences (single speaker).
- Created `data/metadata.csv` with columns: `filename, transcript, romanized`.
- Normalized all audio to 16 kHz mono into `data/audio_normalized/`.
- Added utility scripts:
  - `scripts/utils/preview_metadata.py` – quick check of CSV.
  - `scripts/utils/inspect_audio.py` – sample rate & duration check.
  - `scripts/utils/normalize_audio.py` – resample + normalize volume.
- Implemented first STT tests:
  - `scripts/stt/test_small_model.py` – quick check on a few files.
  - `scripts/stt/compare_accuracy.py` – runs on all 51 files and writes `data/transcripts/accuracy_report.csv`.
- Evaluated Whisper `medium` and `small` models on the dataset.



## Week 1: Environment Setup & First Tests

### Summary (End of Week)
**Week Started:** [Date]
**Week Ended:** [Date]

**Major Achievements:**
- [ ] 
- [ ] 
- [ ] 

**Key Learnings:**
- 
- 
- 

**Biggest Challenge:**


**How I Overcame It:**


**Next Week's Focus:**


**Weekly Time Spent:** ___ hours

---

## Week 2: First Nepali STT Demo

[Follow same format]

---

## Important Milestones

### Milestone 1: Setup Complete ✓
**Date:** [When achieved]
**Description:** Development environment fully set up and tested
**Evidence:** Test script runs successfully

### Milestone 2: First Nepali Transcription
**Date:** [When achieved]
**Description:** Successfully transcribed first Nepali audio
**Evidence:** [Link to audio file and transcript]

### Milestone 3: Web Demo Created
**Date:** [When achieved]
**Description:** Simple web interface working
**Evidence:** [Screenshot or link]

---

## Technical Glossary (Build As You Learn)

**Terms I've learned:**

**STT (Speech-to-Text):**
Converts spoken audio into written text

**TTS (Text-to-Speech):**
Converts written text into spoken audio

**Whisper:**
OpenAI's speech recognition model that supports multiple languages including Nepali

**Virtual Environment:**
Isolated Python workspace for project-specific dependencies

**Git Commit:**
Saving a snapshot of project changes

[Add more as you learn them]

---

## Questions to Research Later

- [ ] How does Whisper actually work internally?
- [ ] What makes a good quality audio recording?
- [ ] How much data is needed for TTS training?
- [ ] How to improve transcription accuracy?
- [ ] What is a neural network?

---

## Resources I Found Helpful

**Tutorials:**
- 

**Documentation:**
- 

**Videos:**
- 

**Articles:**
- 

**Communities:**
- 

---

## Personal Reflections

### What's Going Well:


### What's Challenging:


### What I'm Most Excited About:


### How I'm Feeling About Progress:


---

## Notes Section

[Free space for random thoughts, ideas, observations]

---

**Last Updated:** [Date]
**Total Days Worked:** [Count]
**Total Hours Invested:** [Sum]
**Current Phase:** [Phase number and name]