"""
Phase 3 — Step 3: Test your fine-tuned Whisper model
Compares fine-tuned model vs baseline whisper-small on your test set

Run from project root:
    python scripts/test_finetuned.py
"""

import json
import torch
import numpy as np
from pathlib import Path
from transformers import (
    WhisperProcessor,
    WhisperForConditionalGeneration,
)
import whisper
import evaluate

# ── Device ────────────────────────────────────────────────────────────────────

DEVICE = "mps" if torch.backends.mps.is_available() else "cpu"
print(f"✓ Device: {DEVICE}")

# ── Paths ─────────────────────────────────────────────────────────────────────

PROJECT_ROOT   = Path(__file__).resolve().parent.parent
DATASET_DIR    = PROJECT_ROOT / "data" / "datasets" / "whisper_finetune"
FINETUNED_DIR  = PROJECT_ROOT / "models" / "whisper-nepali"
TEST_JSONL     = DATASET_DIR / "test" / "metadata.jsonl"
TEST_AUDIO_DIR = DATASET_DIR / "test"

# ── Load test samples ─────────────────────────────────────────────────────────

test_samples = []
with open(TEST_JSONL, encoding="utf-8") as f:
    for line in f:
        r = json.loads(line.strip())
        test_samples.append({
            "audio_path":  str(TEST_AUDIO_DIR / r["file_name"]),
            "transcript":  r["transcription"],
        })

print(f"✓ Loaded {len(test_samples)} test samples")
print()

# ── Load fine-tuned model ─────────────────────────────────────────────────────

print("Loading fine-tuned model...")
ft_processor = WhisperProcessor.from_pretrained(str(FINETUNED_DIR))
ft_model     = WhisperForConditionalGeneration.from_pretrained(str(FINETUNED_DIR))
ft_model     = ft_model.to(DEVICE)
ft_model.eval()
print("✓ Fine-tuned model loaded")

# ── Load baseline model ───────────────────────────────────────────────────────

print("Loading baseline whisper-small...")
baseline_model = whisper.load_model("small")
print("✓ Baseline model loaded")
print()

# ── Run comparison ────────────────────────────────────────────────────────────

wer_metric = evaluate.load("wer")

ft_preds       = []
baseline_preds = []
references     = []

print("=" * 60)
print("Running comparison on test set...")
print("=" * 60)
print()

for i, sample in enumerate(test_samples):
    audio_path = sample["audio_path"]
    reference  = sample["transcript"]

    # ── Fine-tuned prediction ──
    import librosa
    audio_array, sr = librosa.load(audio_path, sr=16000)
    inputs = ft_processor(
        audio_array,
        sampling_rate=16000,
        return_tensors="pt"
    ).input_features.to(DEVICE)

    with torch.no_grad():
        predicted_ids = ft_model.generate(inputs)
    ft_pred = ft_processor.batch_decode(
        predicted_ids, skip_special_tokens=True
    )[0].strip()

    # ── Baseline prediction ──
    result      = baseline_model.transcribe(
        audio_path,
        language="ne",
        fp16=False,
        temperature=0.0,
        condition_on_previous_text=False,
    )
    baseline_pred = result["text"].strip()

    ft_preds.append(ft_pred)
    baseline_preds.append(baseline_pred)
    references.append(reference)

    # Print first 10 samples for visual comparison
    if i < 10:
        print(f"Sample {i+1:02d}: {audio_path.split('/')[-1]}")
        print(f"  Reference  : {reference}")
        print(f"  Fine-tuned : {ft_pred}")
        print(f"  Baseline   : {baseline_pred}")
        print()

# ── Calculate WER ─────────────────────────────────────────────────────────────

ft_wer       = 100 * wer_metric.compute(predictions=ft_preds,       references=references)
baseline_wer = 100 * wer_metric.compute(predictions=baseline_preds, references=references)
improvement  = baseline_wer - ft_wer

print("=" * 60)
print("Results")
print("=" * 60)
print(f"  Baseline WER   : {baseline_wer:.1f}%")
print(f"  Fine-tuned WER : {ft_wer:.1f}%")
print(f"  Improvement    : {improvement:.1f}% {'✓ better' if improvement > 0 else '✗ worse'}")
print()

if improvement > 0:
    print("✓ Fine-tuning improved accuracy!")
    print("  Next step: plug the model into voice_loop_demo.py")
else:
    print("⚠️  Fine-tuned model didn't improve — try more epochs")
    print("  Edit finetune_whisper.py: increase NUM_EPOCHS to 30")

# ── Save results ──────────────────────────────────────────────────────────────

results = {
    "baseline_wer":   round(baseline_wer, 2),
    "finetuned_wer":  round(ft_wer, 2),
    "improvement":    round(improvement, 2),
    "test_samples":   len(test_samples),
    "predictions": [
        {
            "file":       s["audio_path"].split("/")[-1],
            "reference":  r,
            "finetuned":  f,
            "baseline":   b,
        }
        for s, r, f, b in zip(test_samples, references, ft_preds, baseline_preds)
    ]
}

results_path = PROJECT_ROOT / "models" / "whisper-nepali" / "test_results.json"
with open(results_path, "w", encoding="utf-8") as out:
    json.dump(results, out, ensure_ascii=False, indent=2)

print(f"\n  Full results saved to: {results_path}")