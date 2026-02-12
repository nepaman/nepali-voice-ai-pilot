"""
Compare Whisper transcriptions with ground truth (Nepali)
Calculate WER-based accuracy metrics
"""

import whisper
import pandas as pd
import re
import unicodedata
from jiwer import wer

# --------------------------------------------------
# Nepali text normalization
# --------------------------------------------------
def normalize_nepali(text: str) -> str:
    if not isinstance(text, str):
        return ""

    # Unicode normalization
    text = unicodedata.normalize("NFC", text)

    # Keep only Devanagari characters and spaces
    text = re.sub(r"[^\u0900-\u097F\s]", "", text)

    # Normalize spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text


# --------------------------------------------------
# Load metadata
# --------------------------------------------------
print("Loading ground truth data...")
metadata = pd.read_csv("data/metadata.csv")
print(f"Loaded {len(metadata)} reference transcriptions\n")


# --------------------------------------------------
# Load Whisper model
# --------------------------------------------------
print("Loading Whisper 'medium' model...")
model = whisper.load_model("medium")
print("✓ Model loaded\n")


# --------------------------------------------------
# Process each audio file
# --------------------------------------------------
results = []

for idx, row in metadata.iterrows():
    filename = row["filename"]
    gt_raw = row["transcript"]

    print(f"[{idx + 1}/{len(metadata)}] {filename}")

    # Transcribe (force Nepali)
    result = model.transcribe(
    audio_path,
    language="ne",
    fp16=False,
    temperature=0.0, 
    initial_prompt="नमस्कार शुभ प्रभात शुभ बिहानी शुभ रात्रि" 
    )

    pred_raw = result["text"]

    # Normalize both texts
    gt = normalize_nepali(gt_raw)
    pred = normalize_nepali(pred_raw)

    # Compute WER
    error_rate = wer(gt, pred)
    accuracy = max(0.0, (1 - error_rate) * 100)

    # Display
    print(f"  Ground Truth : {gt}")
    print(f"  Whisper Said : {pred}")
    print(f"  WER          : {error_rate:.2f}")
    print(f"  Accuracy     : {accuracy:.1f}%\n")

    results.append({
        "file": filename,
        "ground_truth": gt,
        "prediction": pred,
        "wer": error_rate,
        "accuracy": accuracy
    })


# --------------------------------------------------
# Summary
# --------------------------------------------------
df = pd.DataFrame(results)

print("=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"Total files: {len(df)}")
print(f"Average accuracy: {df['accuracy'].mean():.1f}%")
print(f"Best accuracy: {df['accuracy'].max():.1f}%")
print(f"Worst accuracy: {df['accuracy'].min():.1f}%\n")


# --------------------------------------------------
# Save results
# --------------------------------------------------
df.to_csv(
    "data/transcripts/accuracy_report.csv",
    index=False,
    encoding="utf-8"
)

print("✓ Detailed report saved to: data/transcripts/accuracy_report.csv")
