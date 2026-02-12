# First Nepali STT Test - Step by Step

## Goal
Successfully transcribe your first Nepali audio using Whisper.

**Expected time:** 1-2 hours
**Prerequisite:** Completed setup guide

---

## Step 1: Record Test Audio

### 1.1 Prepare Test Sentences

Choose 5 simple Nepali sentences to record:

```
1. नमस्ते, मेरो नाम ज्ञानेन्द्र हो।
   (Namaste, mero naam Gyanendra ho.)
   Hello, my name is Gyanendra.

2. म काठमाडौंमा बस्छु।
   (Ma Kathmandu ma baschu.)
   I live in Kathmandu.

3. आज मौसम राम्रो छ।
   (Aaja mausam ramro cha.)
   The weather is good today.

4. तपाईंलाई कस्तो छ?
   (Tapai lai kasto cha?)
   How are you?

5. म नेपाली भाषा सिक्दैछु।
   (Ma Nepali bhasha sikdaichu.)
   I am learning Nepali language.
```

### 1.2 Recording Instructions

**Option A: Use Your Phone (Easiest)**
1. Open Voice Recorder app
2. Hold phone 15-20 cm from your mouth
3. Speak clearly and naturally (not too slow, not too fast)
4. Record each sentence separately
5. Name files: `test_01.m4a`, `test_02.m4a`, etc.
6. Transfer to your computer

**Option B: Use Audacity (Better Quality)**
1. Open Audacity
2. Click red Record button
3. Speak sentence
4. Stop recording
5. File → Export → Export as MP3
6. Name: `test_01.mp3`
7. Repeat for each sentence

**Recording Tips:**
- Find quiet location
- Speak naturally (like daily conversation)
- Don't shout or whisper
- If you make mistake, just record again
- Each recording should be 3-5 seconds long

### 1.3 Save Files

Create folder and save recordings:
```bash
# Navigate to your project
cd nepali-voice-ai-pilot

# Your recordings go here:
# data/audio/test/test_01.mp3
# data/audio/test/test_02.mp3
# etc.
```

---

## Step 2: Create Your First Script

### 2.1 Create New Python File

**File:** `scripts/stt/first_test.py`

**Copy this code:**

```python
"""
First Nepali STT Test
This script transcribes Nepali audio files using Whisper
"""

import whisper
import os

# Print welcome message
print("="*60)
print("Nepali Voice AI - First STT Test")
print("="*60)
print()

# Load Whisper model
print("Loading Whisper model (this may take a minute)...")
model = whisper.load_model("base")  # Using 'base' model for balance of speed/accuracy
print("✓ Model loaded successfully!")
print()

# Path to your test audio
audio_folder = "data/audio/test/"

# List all audio files
audio_files = [f for f in os.listdir(audio_folder) 
               if f.endswith(('.mp3', '.wav', '.m4a', '.flac'))]

if not audio_files:
    print("❌ No audio files found in", audio_folder)
    print("Please add your recordings there first.")
    exit()

print(f"Found {len(audio_files)} audio file(s)")
print()

# Process each audio file
for audio_file in sorted(audio_files):
    audio_path = os.path.join(audio_folder, audio_file)
    
    print("-" * 60)
    print(f"Processing: {audio_file}")
    print("-" * 60)
    
    try:
        # THIS IS THE KEY FIX - Force Nepali language!
        result = model.transcribe(
            audio_path,
            language="ne",  # Force Nepali (not auto-detect)
            task="transcribe",  # Transcribe (not translate)
            fp16=False  # Use FP32 for CPU compatibility
        )
        
        # Print result
        print(f"Transcription: {result['text']}")
        print()
        
        # Also show detected language (should be 'ne')
        if 'language' in result:
            print(f"Detected language: {result['language']}")
        
    except Exception as e:
        print(f"❌ Error processing {audio_file}: {e}")
        print()

print("="*60)
print("Test complete!")
print("="*60)
```

---

## Step 3: Run Your First Test

### 3.1 Make Sure Virtual Environment is Active

```bash
# Check if (venv) appears at start of terminal line
# If not, activate it:

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3.2 Run the Script

```bash
python scripts/stt/first_test.py
```

### 3.3 What to Expect

**First time running:**
- Whisper will download the model (~150MB for 'base' model)
- This takes 1-5 minutes depending on internet speed
- Progress bar will show download

**Then you'll see:**
```
============================================================
Nepali Voice AI - First STT Test
============================================================

Loading Whisper model (this may take a minute)...
✓ Model loaded successfully!

Found 5 audio file(s)

------------------------------------------------------------
Processing: test_01.mp3
------------------------------------------------------------
Transcription: नमस्ते मेरो नाम ज्ञानेन्द्र हो
Detected language: ne

------------------------------------------------------------
Processing: test_02.mp3
------------------------------------------------------------
[etc...]
```

---

## Step 4: Document Results

### 4.1 Create Results File

**File:** `docs/test_results_day1.md`

```markdown
# First STT Test Results

**Date:** [Today's date]
**Model Used:** Whisper base
**Number of Tests:** 5

## Test Recordings

### Test 1
**Expected:** नमस्ते, मेरो नाम ज्ञानेन्द्र हो।
**Transcribed:** [Paste actual output]
**Accuracy:** [Good/OK/Poor]
**Notes:** [Any observations]

### Test 2
**Expected:** म काठमाडौंमा बस्छु।
**Transcribed:** [Paste actual output]
**Accuracy:** 
**Notes:**

[Continue for all tests...]

### Baseline Nepali STT – Whisper tests (51 sentences, single speaker)

**Data**
- 51 short daily-conversation sentences
- 16 kHz mono, single speaker, clean microphone
- Transcripts: Nepali (Devanagari) + Romanized

**Models tested**
- Whisper `medium`
- Whisper `small`

**Results (character-level / custom WER metric)**

| Model   | Avg. accuracy | Best case          | Notes                                  |
|---------|---------------|--------------------|----------------------------------------|
| medium  | ~2.1%         | ~33.3%             | Often phonetically close but noisy     |
| small   | ~6.3%         | 100% (e.g. नमस्कार) | Some short phrases perfect, others bad |

- Many outputs are **phonetically similar** to Nepali but with wrong spelling and noisy characters.
- Certain greetings like “नमस्कार”, “नमस्ते” are recognized perfectly.
- Longer or less common phrases often degrade badly, sometimes with repeated syllables.
- This confirms the core problem: **out-of-the-box Whisper struggles with conversational Nepali**, and we need adaptation / fine‑tuning.


## Overall Observations

**What worked well:**
- 

**What needs improvement:**
- 

**Pronunciation issues noticed:**
- 

**Next steps:**
- 
```

---

## Step 5: Troubleshooting

### Issue: "No module named 'whisper'"
**Solution:**
```bash
pip install openai-whisper
```

### Issue: "No audio files found"
**Solution:**
- Check files are in correct folder: `data/audio/test/`
- Check file extensions (should be .mp3, .wav, etc.)
- Check spelling of folder name

### Issue: Model download fails
**Solution:**
```bash
# Download manually and specify path
python -c "import whisper; whisper.load_model('base', download_root='./models')"
```

### Issue: Transcription is in wrong language
**Solution:**
- Verify `language="ne"` is in the code
- Check your audio is actually Nepali
- Try speaking more clearly

### Issue: Poor transcription quality
**Possible causes:**
- Background noise in recording
- Speaking too fast or unclear
- Audio quality too low
- Try re-recording in quieter place

---

## Step 6: Experiment and Learn

### 6.1 Try Different Models

Whisper has multiple model sizes. Edit line 15 in your script:

```python
# Faster, less accurate:
model = whisper.load_model("tiny")   # ~39M parameters

# Balanced (current):
model = whisper.load_model("base")   # ~74M parameters

# Better accuracy, slower:
model = whisper.load_model("small")  # ~244M parameters

# Best quality (needs good computer):
model = whisper.load_model("medium") # ~769M parameters
```

### 6.2 Test Different Scenarios

Record and test:
- Speaking fast vs slow
- With/without background noise
- Different microphones
- Different voice tones
- Male vs female voices (if available)

### 6.3 Document Everything

In your learning log, note:
- Which model size works best for you
- What recording conditions give best results
- Common transcription errors
- Nepali words that are often misunderstood

---

## Success Checklist

- [ ] Recorded 5 test audio files
- [ ] Created first_test.py script
- [ ] Successfully ran script
- [ ] Got Nepali transcriptions (even if imperfect)
- [ ] Documented results
- [ ] Updated learning log
- [ ] Committed changes to Git

---

## Celebrate! 

You just:
- Ran your first AI model
- Processed audio with code
- Got Nepali speech transcribed
- Solved the multilingual issue

**This is real progress!**

---

## What's Next?

Once this test is successful, you'll:
1. Create web interface for easier testing
2. Add simple TTS to complete the loop
3. Start building your dataset systematically

**Next Document:** `docs/04_WEB_DEMO.md`

---

## Notes

[Your observations, questions, ideas]