from pathlib import Path
import csv

METADATA_PATH = Path("data") / "metadata.csv"

def preview_metadata(n=5):
    rows = []
    with open(METADATA_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            rows.append(row)
            if i + 1 >= n:
                break

    print(f"Loaded {len(rows)} rows")
    for r in rows:
        print(f"{r['filename']} -> {r['transcript']}  |  {r['romanized']}")

if __name__ == "__main__":
    preview_metadata()
