from pathlib import Path
import csv
import whisper

PROJECT_ROOT = Path(__file__).resolve().parents[2]
AUDIO_DIR = PROJECT_ROOT / "data" / "audio_normalized"
METADATA_PATH = PROJECT_ROOT / "data" / "metadata.csv"

def load_metadata():
    rows = {}
    with open(METADATA_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows[row["filename"]] = row
    return rows

def main():
    meta = load_metadata()
    print(f"Loaded metadata for {len(meta)} files")

    # Whisper model load
    model = whisper.load_model("small")  # सुरुमा "small"; ढिलो भए "tiny" वा "base" use गर्न सक्छौं

    # केही फाइल test
    test_files = ["NP_000.wav", "NP_001.wav", "NP_002.wav"]

    for fname in test_files:
        audio_path = AUDIO_DIR / fname
        if not audio_path.exists():
            print(f"Missing audio: {fname}")
            continue

        print("\n=============================")
        print(f"File: {fname}")

        # Whisper expects 16kHz mono; हाम्रो normalized data त्यस्तै छ
        result = model.transcribe(str(audio_path), language="ne")  # "ne" for Nepali
        predicted = result["text"].strip()

        gt_nepali = meta[fname]["transcript"]
        gt_roman = meta[fname]["romanized"]

        print(f"GT (Nepali): {gt_nepali}")
        print(f"GT (Roman):  {gt_roman}")
        print(f"PREDICTED:   {predicted}")

if __name__ == "__main__":
    main()
