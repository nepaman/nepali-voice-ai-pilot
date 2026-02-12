"""
Compare Whisper transcriptions with ground truth
Uses cleaned audio and metadata_all.csv
Separates v1 (original 51) and v2 (new 100) statistics
"""

from pathlib import Path
import csv
import whisper

PROJECT_ROOT = Path(__file__).resolve().parents[2]
AUDIO_DIR = PROJECT_ROOT / "data" / "audio_cleaned"
METADATA_PATH = PROJECT_ROOT / "data" / "metadata_all.csv"

def load_metadata():
    rows = []
    with open(METADATA_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows

def simple_char_accuracy(gt: str, pred: str) -> float:
    """Calculate character-level accuracy"""
    gt = gt.strip()
    pred = pred.strip()
    if not gt:
        return 0.0
    matches = sum(1 for g, p in zip(gt, pred) if g == p)
    return matches / len(gt)

def main():
    data = load_metadata()
    print(f"Loaded {len(data)} entries from metadata_all.csv")
    print()

    print("Loading Whisper 'small' model...")
    model = whisper.load_model("small")
    print("✓ Model loaded")
    print()

    total_acc = 0.0
    count = 0

    total_acc_v1 = 0.0  # NP_000–NP_050
    count_v1 = 0
    total_acc_v2 = 0.0  # NP_051–NP_150
    count_v2 = 0

    for row in data:
        fname = row["filename"]
        gt = row["transcript"]
        audio_path = AUDIO_DIR / fname

        if not audio_path.exists():
            print(f"⚠ Missing audio: {fname}")
            continue

        print(f"[{count+1}/{len(data)}] {fname}")
        print(f"  Ground Truth: {gt}")

        # Transcribe with best parameters
        result = model.transcribe(
            str(audio_path), 
            language="ne", 
            fp16=False,
            temperature=0.0,  # Conservative
            initial_prompt="नमस्कार शुभ प्रभात शुभ बिहानी"  # Nepali context
        )
        pred = result["text"].strip()
        print(f"  Whisper Said: {pred}")

        acc = simple_char_accuracy(gt, pred)
        print(f"  Accuracy: {acc*100:.1f}%")
        print()

        total_acc += acc
        count += 1

        # Separate by dataset version
        idx = int(fname.replace("NP_", "").replace(".wav", ""))
        if idx <= 50:
            total_acc_v1 += acc
            count_v1 += 1
        else:
            total_acc_v2 += acc
            count_v2 += 1

    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    if count > 0:
        print(f"Overall       : {count} files, avg accuracy = {total_acc/count*100:.1f}%")
    if count_v1 > 0:
        print(f"Original (000-050): {count_v1} files, avg accuracy = {total_acc_v1/count_v1*100:.1f}%")
    if count_v2 > 0:
        print(f"New (051-150)     : {count_v2} files, avg accuracy = {total_acc_v2/count_v2*100:.1f}%")
    print()

if __name__ == "__main__":
    main()