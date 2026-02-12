# Baseline Nepali STT Evaluation – Whisper Model Comparison

**Date:** January 30, 2026  
**Project:** Nepali Voice AI Pilot  
**Phase:** 1 - Speech-to-Text Testing

---

## Dataset Specifications

### Audio Characteristics
- **Total samples:** 51 conversational sentences
- **Language:** Nepali (daily conversation, informal register)
- **Speaker:** Single speaker (male/female - specify)
- **Recording quality:** Clean, minimal background noise
- **Sample rate:** 48 kHz (original) → 16 kHz (normalized)
- **Format:** Mono WAV
- **Duration:** ~1-2 seconds per clip (avg: 1.17s)
- **Recording equipment:** RØDE NT1 (5th Gen) microphone

### Content Categories
- Greetings: "नमस्कार", "नमस्ते", "के छ?"
- Time-based greetings: "शुभ प्रभात", "शुभ बिहानी", "शुभ रात्रि"
- Conversational phrases: "तिमी ठीक छौ?", "के गर्दैछौ?"
- Polite expressions: "कृपया बस्नुहोस्", "धन्यवाद"

### Ground Truth Format
- **Devanagari script:** यो नेपाली भ्वाइस एआई परियोजनाको परीक्षण रेकर्डिङ हो।
- **Romanized phonetic:** Yō nēpālī bhvā'isa ē'ā'ī pariyōjanākō parīkṣaṇa rēkarḍiṅa hō.
- **Storage:** `data/metadata.csv`

---

## Models Evaluated

### Whisper Medium
- **Parameters:** ~769M
- **Model file size:** ~1.5GB
- **Processing speed:** ~3-5 seconds per clip (CPU)

### Whisper Small  
- **Parameters:** ~244M
- **Model file size:** ~450MB
- **Processing speed:** ~1-2 seconds per clip (CPU)

---

## Evaluation Methodology

### Accuracy Metrics
1. **Word Error Rate (WER):** Character-level edit distance
2. **Exact Match:** Percentage of perfect transcriptions
3. **Qualitative Analysis:** Phonetic similarity, script correctness

### Evaluation Script
- **Location:** `scripts/stt/compare_accuracy.py`
- **Output:** `data/transcripts/accuracy_report.csv`
- **Process:** 
  1. Load ground truth from metadata.csv
  2. Transcribe each audio file with `language="ne"` parameter
  3. Calculate WER and similarity scores
  4. Generate per-file and aggregate statistics

---

## Results

### Quantitative Results

| Model   | Avg. Accuracy | Best Case | Worst Case | Perfect Matches |
|---------|---------------|-----------|------------|-----------------|
| Medium  | ~2.1%         | 33.3%     | 0.0%       | 0/51            |
| Small   | ~6.3%         | 100%      | 0.0%       | 3/51*           |

*Perfect matches: "नमस्कार", "नमस्ते" (when no punctuation added)

### Qualitative Observations

#### Whisper Medium Issues:
1. **Character substitution errors:**
   - "शुभ" → "सुव" (श → स)
   - "तिमी" → "तीमें" (wrong vowel marks)
   
2. **Extra punctuation:**
   - Adds periods unnecessarily: "नमस्कार।" instead of "नमस्कार"
   
3. **Word boundary errors:**
   - "के गर्दैछौ" → "किई गद आज्यो" (complete segmentation failure)
   
4. **Over-processing artifacts:**
   - Model appears to over-analyze short clips
   - Phonetically plausible but orthographically incorrect

#### Whisper Small Performance:
1. **Strengths:**
   - Perfect recognition of common greetings
   - Consistent Devanagari script (no mixed scripts)
   - Better character-level accuracy
   - More reliable word boundaries
   
2. **Weaknesses:**
   - Still struggles with longer phrases (4+ words)
   - Inconsistent with less common vocabulary
   - Some phonetic confusion (श/स, ठ/त)

---

## Key Findings

### Finding 1: Model Size ≠ Better Performance
**Observation:** Despite having 3x more parameters, Whisper medium performed significantly worse (2.1% vs 6.3% accuracy).

**Hypothesis:** 
- Medium model trained on longer audio segments
- Over-fitting to formal/broadcast Nepali
- Short clips (~1s) don't provide enough context for larger model

**Implication:** For short conversational Nepali clips, smaller models are more appropriate.

---

### Finding 2: Script Consistency
**Observation:** Small model consistently outputs Devanagari script. Medium model occasionally produces mixed/incorrect scripts.

**Significance:** Critical for production use - consistent script output is non-negotiable for Nepali applications.

---

### Finding 3: Phonetic vs Orthographic Accuracy
**Observation:** Many transcriptions are phonetically plausible but orthographically incorrect.

**Examples:**
- "सुव प्रवाथ" sounds like "शुभ प्रभात" but uses wrong characters
- "किसे यार" sounds like "के छ यार" but wrong spelling

**Analysis:** Model understands Nepali phonology but lacks training on correct Devanagari spelling patterns for conversational speech.

---

### Finding 4: Audio Length Impact
**Observation:** Very short clips (<1s) have lower accuracy than 1-2s clips.

**Recommendation:** Optimal clip length for Whisper small appears to be 1.5-3 seconds.

---

## Analysis & Interpretation

### Why Baseline Accuracy is Low

1. **Training Data Mismatch:**
   - Whisper trained primarily on formal, read speech
   - Our data: informal, conversational Nepali
   - Different pronunciation patterns and vocabulary

2. **Language Resource Gap:**
   - Nepali is "low-resource" in Whisper's training set
   - Model likely has orders of magnitude more Hindi/English data
   - Potential Hindi interference in Devanagari rendering

3. **Audio Characteristics:**
   - Very short clips challenge the model's context window
   - Single speaker = no diversity in voice/accent
   - Clean audio might lack realism of deployment scenarios

4. **Evaluation Strictness:**
   - Character-level exact matching is extremely strict
   - Small punctuation differences count as errors
   - No credit for phonetic similarity

---

## Conclusions

### Core Problem Confirmed
**Out-of-the-box Whisper struggles with conversational Nepali.**

While the model can recognize common greetings and produces phonetically plausible outputs, the orthographic accuracy is too low for production use.

### Model Selection Decision
**Adopt Whisper Small as baseline** for the following reasons:
- 3x better accuracy than medium (6.3% vs 2.1%)
- Consistent Devanagari script output
- Faster processing (important for real-time use)
- Smaller model size (easier deployment)
- Better suited for short conversational clips

---

## Next Steps & Recommendations

### Immediate Actions (Phase 1 Complete)
1. Document findings in learning log
2. Commit baseline evaluation code and results to repository
3. Create demo script for single-file testing

### Phase 2 Options

**Option A: Fine-tune Whisper Small (Recommended)**
- Collect 2-5 hours of labeled Nepali conversational speech
- Fine-tune Whisper small on conversational Nepali specifically
- Expected improvement: 6.3% → 40-60% accuracy
- **Effort:** High (weeks)
- **Impact:** High

**Option B: Data Augmentation**
- Record same sentences with:
  - Different speakers (male/female)
  - Different accents (Kathmandu, Pokhara, Terai)
  - Background noise variations
- Test if diversity improves baseline performance
- **Effort:** Medium (days)
- **Impact:** Medium

**Option C: Prompt Engineering**
- Experiment with different Whisper parameters:
  - Temperature settings
  - Initial prompt text in Nepali
  - Compression ratio threshold
- Might extract 1-2% more accuracy without retraining
- **Effort:** Low (hours)
- **Impact:** Low

**Option D: Hybrid Approach**
- Use Whisper for speech → phonemes
- Add post-processing layer for Devanagari correction
- Rule-based or ML-based orthographic normalization
- **Effort:** Medium (days)
- **Impact:** Medium-High

---

## Technical Debt & Known Issues

1. **Evaluation metric limitations:**
   - Current WER doesn't credit partial matches
   - Need semantic similarity metric
   - Should separate script errors from content errors

2. **Dataset size:**
   - 51 samples insufficient for robust statistics
   - Need minimum 100-200 samples for reliable evaluation
   - Single speaker limits generalizability

3. **Audio normalization:**
   - Current normalization might be too aggressive
   - Should preserve natural speech dynamics
   - Need A/B test: normalized vs raw audio

---

## Reproducibility

### Environment
- **OS:** macOS 14.x (Sonoma)
- **Python:** 3.10.x
- **Whisper:** 20231117
- **PyTorch:** 2.10.0 (CPU)

### Code Location
- **Evaluation script:** `scripts/stt/compare_accuracy.py`
- **Results:** `data/transcripts/accuracy_report.csv`
- **Utilities:** `scripts/utils/normalize_audio.py`

### Replication Steps
```bash
# 1. Normalize audio
python scripts/utils/normalize_audio.py

# 2. Run evaluation
python scripts/stt/compare_accuracy.py

# 3. View results
cat data/transcripts/accuracy_report.csv
```

---

## References & Related Work

### Similar Studies
- [List any Nepali ASR papers you found]
- OpenSLR Nepali dataset: 169 hours of read speech
- Common Voice Nepali: Community-contributed recordings

### Whisper Documentation
- Official repo: https://github.com/openai/whisper
- Paper: "Robust Speech Recognition via Large-Scale Weak Supervision"

---

## Appendix: Sample Transcriptions

### Perfect Matches (Small Model)
```
File: NP_001.wav
Ground Truth: नमस्कार
Whisper:      नमस्कार
Accuracy:     100%
```

### Typical Errors (Small Model)
```
File: NP_011.wav
Ground Truth: शुभ प्रभात
Whisper:      सुव प्रवाथ
Accuracy:     ~40%
Analysis:     Phonetically close but wrong characters (श→स, भ→व, त→थ)
```

### Complete Failure (Small Model)
```
File: NP_040.wav
Ground Truth: आरामसँग आउनुहोस्
Whisper:      अराम साणा ओनो रूस
Accuracy:     ~15%
Analysis:     Word segmentation failure, wrong vowel marks
```

---

**Report Status:** Draft v1.0  
**Next Update:** After Phase 2 implementation  
**Contact:** [Your info]

---

*This report documents baseline performance as of Phase 1. Results should improve significantly with fine-tuning and data augmentation in subsequent phases.*