"""
Phase 3 — Step 1: Prepare Nepali dataset for Whisper fine-tuning
Converts your metadata_all.csv + WAV files into HuggingFace format

Run from project root:
    python scripts/prepare_dataset.py

Output:
    data/datasets/whisper_finetune/
        train/   (80% of data)
        test/    (20% of data)
        dataset_info.json
"""

import os
import csv
import json
import shutil
import random
from pathlib import Path
from dataclasses import dataclass

# ── Optional: install check ───────────────────────────────────────────────────
try:
    import librosa
    import soundfile as sf
    HAS_LIBROSA = True
except ImportError:
    HAS_LIBROSA = False
    print("⚠️  librosa not installed — skipping audio validation")
    print("    Install with: pip install librosa soundfile")

# ── Paths ─────────────────────────────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).resolve().parent.parent
AUDIO_DIR    = PROJECT_ROOT / "data" / "audio"
CSV_PATH     = PROJECT_ROOT / "data" / "metadata_all.csv"
OUTPUT_DIR   = PROJECT_ROOT / "data" / "datasets" / "whisper_finetune"

TRAIN_DIR    = OUTPUT_DIR / "train"
TEST_DIR     = OUTPUT_DIR / "test"

TARGET_SR    = 16000   # Whisper requires 16kHz mono
TRAIN_SPLIT  = 0.8     # 80% train, 20% test
RANDOM_SEED  = 42

print("=" * 60)
print("Phase 3 — Whisper fine-tune dataset preparation")
print("=" * 60)
print(f"Audio dir  : {AUDIO_DIR}")
print(f"CSV        : {CSV_PATH}")
print(f"Output dir : {OUTPUT_DIR}")
print()

# ── Load CSV ──────────────────────────────────────────────────────────────────

rows = []
skipped = []

with open(CSV_PATH, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        filename   = row["filename"].strip()
        transcript = row["transcript"].strip()

        # Skip empty transcripts
        if not transcript:
            skipped.append((filename, "empty transcript"))
            continue

        audio_path = AUDIO_DIR / filename

        # Skip missing audio files
        if not audio_path.exists():
            skipped.append((filename, "audio file missing"))
            continue

        rows.append({
            "audio_path": audio_path,
            "filename":   filename,
            "transcript": transcript,
        })

print(f"✓ Loaded {len(rows)} valid samples from CSV")
if skipped:
    print(f"⚠️  Skipped {len(skipped)} rows:")
    for name, reason in skipped:
        print(f"   {name}: {reason}")
print()

# ── Audio validation + resampling ─────────────────────────────────────────────

validated = []

for item in rows:
    path = item["audio_path"]

    if HAS_LIBROSA:
        try:
            audio, sr = librosa.load(str(path), sr=None)
            duration  = len(audio) / sr

            # Skip very short clips (under 0.3s) — Whisper hallucinates on these
            if duration < 0.3:
                print(f"  ⚠️  Skipping {path.name} — too short ({duration:.2f}s)")
                continue

            # Skip very long clips (over 30s) — Whisper's max context
            if duration > 30.0:
                print(f"  ⚠️  Skipping {path.name} — too long ({duration:.2f}s)")
                continue

            item["duration"] = round(duration, 2)
            item["original_sr"] = sr

        except Exception as e:
            print(f"  ⚠️  Skipping {path.name} — audio error: {e}")
            continue
    else:
        item["duration"] = None
        item["original_sr"] = None

    validated.append(item)

print(f"✓ {len(validated)} samples passed audio validation")
if HAS_LIBROSA:
    total_dur = sum(i["duration"] for i in validated)
    print(f"  Total audio: {total_dur:.1f}s ({total_dur/60:.1f} minutes)")
print()

# ── Train / test split ────────────────────────────────────────────────────────

random.seed(RANDOM_SEED)
random.shuffle(validated)

split_idx   = int(len(validated) * TRAIN_SPLIT)
train_items = validated[:split_idx]
test_items  = validated[split_idx:]

print(f"✓ Split: {len(train_items)} train / {len(test_items)} test")
print()

# ── Create output directories ─────────────────────────────────────────────────

for d in [TRAIN_DIR, TEST_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# ── Write manifest JSONL files ────────────────────────────────────────────────
# HuggingFace datasets expect a metadata.jsonl with:
#   {"file_name": "audio/NP_001.wav", "transcription": "नमस्कार"}

def write_split(items, split_dir, split_name):
    audio_out = split_dir / "audio"
    audio_out.mkdir(exist_ok=True)

    manifest_path = split_dir / "metadata.jsonl"
    count = 0

    with open(manifest_path, "w", encoding="utf-8") as mf:
        for item in items:
            src  = item["audio_path"]
            dest = audio_out / item["filename"]

            # Resample to 16kHz if librosa available, else just copy
            if HAS_LIBROSA and item["original_sr"] != TARGET_SR:
                audio, _ = librosa.load(str(src), sr=TARGET_SR)
                sf.write(str(dest), audio, TARGET_SR)
            else:
                shutil.copy2(str(src), str(dest))

            record = {
                "file_name":     f"audio/{item['filename']}",
                "transcription": item["transcript"],
            }
            if item["duration"]:
                record["duration"] = item["duration"]

            mf.write(json.dumps(record, ensure_ascii=False) + "\n")
            count += 1

    print(f"✓ {split_name}: {count} samples → {split_dir}")
    return count

train_count = write_split(train_items, TRAIN_DIR, "Train")
test_count  = write_split(test_items,  TEST_DIR,  "Test")

# ── Write dataset_info.json ───────────────────────────────────────────────────

info = {
    "dataset_name": "nepali-voice-ai-pilot",
    "language": "ne",
    "description": "Single-speaker Nepali conversational speech dataset",
    "total_samples": train_count + test_count,
    "train_samples": train_count,
    "test_samples": test_count,
    "sample_rate": TARGET_SR,
    "audio_format": "wav",
    "transcript_column": "transcription",
    "splits": {
        "train": str(TRAIN_DIR / "metadata.jsonl"),
        "test":  str(TEST_DIR  / "metadata.jsonl"),
    }
}

info_path = OUTPUT_DIR / "dataset_info.json"
with open(info_path, "w", encoding="utf-8") as f:
    json.dump(info, f, ensure_ascii=False, indent=2)

# ── Summary ───────────────────────────────────────────────────────────────────

print()
print("=" * 60)
print("Dataset preparation complete!")
print("=" * 60)
print(f"  Train samples : {train_count}")
print(f"  Test samples  : {test_count}")
print(f"  Output        : {OUTPUT_DIR}")
print()
print("Next step — install fine-tuning dependencies:")
print()
print("  pip install transformers datasets accelerate")
print("  pip install torch torchaudio")
print("  pip install librosa soundfile jiwer")
print()
print("Then run:")
print("  python scripts/finetune_whisper.py")