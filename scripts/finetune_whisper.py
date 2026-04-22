"""
Phase 3 — Step 2: Fine-tune Whisper on Nepali dataset (M1 Mac optimized)
Uses MPS (Metal Performance Shaders) for GPU acceleration on Apple Silicon

Run from project root:
    python scripts/finetune_whisper.py
"""

import os
import json
import torch
import librosa
import numpy as np
from pathlib import Path
from dataclasses import dataclass
from typing import Any, Dict, List, Union

from datasets import Dataset
from transformers import (
    WhisperFeatureExtractor,
    WhisperTokenizer,
    WhisperProcessor,
    WhisperForConditionalGeneration,
    Seq2SeqTrainingArguments,
    Seq2SeqTrainer,
)
import evaluate

# ── Device ────────────────────────────────────────────────────────────────────

if torch.backends.mps.is_available():
    DEVICE = "mps"
    print("✓ Using Apple M1 GPU (MPS)")
else:
    DEVICE = "cpu"
    print("⚠️  Using CPU")

# ── Paths ─────────────────────────────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATASET_DIR  = PROJECT_ROOT / "data" / "datasets" / "whisper_finetune"
MODEL_OUTPUT = PROJECT_ROOT / "models" / "whisper-nepali"
MODEL_OUTPUT.mkdir(parents=True, exist_ok=True)

# ── Config ────────────────────────────────────────────────────────────────────

MODEL_NAME    = "openai/whisper-tiny"
LANGUAGE      = "nepali"
TASK          = "transcribe"
SAMPLE_RATE   = 16000
BATCH_SIZE    = 4        # reduced for M1 stability
GRAD_ACCUM    = 2        # effective batch = 2 × 4 = 8
LEARNING_RATE = 1e-5
NUM_EPOCHS    = 20
WARMUP_STEPS  = 50
SAVE_STEPS    = 100
EVAL_STEPS    = 100

print("=" * 60)
print("Phase 3 — Whisper fine-tuning (M1 optimized)")
print("=" * 60)
print(f"Base model : {MODEL_NAME}")
print(f"Device     : {DEVICE}")
print(f"Epochs     : {NUM_EPOCHS}")
print(f"Batch size : {BATCH_SIZE} (effective: {BATCH_SIZE * GRAD_ACCUM})")
print()

# ── Load processor & model ────────────────────────────────────────────────────

print("Loading Whisper processor and model...")
feature_extractor = WhisperFeatureExtractor.from_pretrained(MODEL_NAME)
tokenizer = WhisperTokenizer.from_pretrained(
    MODEL_NAME, language=LANGUAGE, task=TASK
)
processor = WhisperProcessor.from_pretrained(
    MODEL_NAME, language=LANGUAGE, task=TASK
)
model = WhisperForConditionalGeneration.from_pretrained(MODEL_NAME)
model.generation_config.language = LANGUAGE
model.generation_config.task = TASK
model.generation_config.forced_decoder_ids = None
model = model.to(DEVICE)
print(f"✓ Model loaded on {DEVICE}")
print()

# ── Load dataset using librosa (avoids torchcodec issue on M1) ────────────────

def load_split(split_name):
    """Load audio with librosa directly — no torchcodec needed."""
    jsonl_path = DATASET_DIR / split_name / "metadata.jsonl"
    audio_dir  = DATASET_DIR / split_name

    records = []
    with open(jsonl_path, encoding="utf-8") as f:
        for line in f:
            r = json.loads(line.strip())
            audio_path = str(audio_dir / r["file_name"])

            # Load audio with librosa at 16kHz directly
            try:
                audio_array, _ = librosa.load(audio_path, sr=SAMPLE_RATE)
            except Exception as e:
                print(f"  ⚠️  Skipping {r['file_name']}: {e}")
                continue

            # Extract features immediately — no lazy decoding
            input_features = feature_extractor(
                audio_array,
                sampling_rate=SAMPLE_RATE
            ).input_features[0]

            # Tokenize transcript
            labels = tokenizer(r["transcription"]).input_ids

            records.append({
                "input_features": input_features,
                "labels":         labels,
            })

    return records

print("Loading and preprocessing train set...")
train_records = load_split("train")
print(f"✓ Train: {len(train_records)} samples")

print("Loading and preprocessing test set...")
test_records = load_split("test")
print(f"✓ Test:  {len(test_records)} samples")
print()

train_dataset = Dataset.from_list(train_records)
test_dataset  = Dataset.from_list(test_records)

# ── Data collator ─────────────────────────────────────────────────────────────

@dataclass
class DataCollatorSpeechSeq2SeqWithPadding:
    processor: Any
    decoder_start_token_id: int

    def __call__(self, features: List[Dict[str, Union[List[int], torch.Tensor]]]):
        input_features = [
            {"input_features": f["input_features"]} for f in features
        ]
        batch = self.processor.feature_extractor.pad(
            input_features, return_tensors="pt"
        )

        label_features = [{"input_ids": f["labels"]} for f in features]
        labels_batch = self.processor.tokenizer.pad(
            label_features, return_tensors="pt"
        )

        labels = labels_batch["input_ids"].masked_fill(
            labels_batch.attention_mask.ne(1), -100
        )

        if (labels[:, 0] == self.decoder_start_token_id).all().cpu().item():
            labels = labels[:, 1:]

        batch["labels"] = labels
        return batch

data_collator = DataCollatorSpeechSeq2SeqWithPadding(
    processor=processor,
    decoder_start_token_id=model.config.decoder_start_token_id,
)

# ── Metrics ───────────────────────────────────────────────────────────────────

wer_metric = evaluate.load("wer")

def compute_metrics(pred):
    pred_ids  = pred.predictions
    label_ids = pred.label_ids
    label_ids[label_ids == -100] = tokenizer.pad_token_id

    pred_str  = tokenizer.batch_decode(pred_ids,  skip_special_tokens=True)
    label_str = tokenizer.batch_decode(label_ids, skip_special_tokens=True)

    wer = 100 * wer_metric.compute(predictions=pred_str, references=label_str)
    print(f"\n  Sample → pred : {pred_str[0]}")
    print(f"  Sample → ref  : {label_str[0]}")
    print(f"  WER           : {wer:.2f}%\n")
    return {"wer": wer}

# ── Training arguments ────────────────────────────────────────────────────────

training_args = Seq2SeqTrainingArguments(
    output_dir=str(MODEL_OUTPUT),
    fp16=False,
    bf16=False,
    num_train_epochs=NUM_EPOCHS,
    per_device_train_batch_size=BATCH_SIZE,
    gradient_accumulation_steps=GRAD_ACCUM,
    learning_rate=LEARNING_RATE,
    warmup_steps=WARMUP_STEPS,
    weight_decay=0.01,
    per_device_eval_batch_size=BATCH_SIZE,
    eval_strategy="steps",
    eval_steps=EVAL_STEPS,
    predict_with_generate=True,
    generation_max_length=225,
    save_steps=SAVE_STEPS,
    save_total_limit=2,
    load_best_model_at_end=True,
    metric_for_best_model="wer",
    greater_is_better=False,
    logging_steps=25,
    report_to="none",
    push_to_hub=False,
)

# ── Train ─────────────────────────────────────────────────────────────────────

trainer = Seq2SeqTrainer(
    args=training_args,
    model=model,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
    data_collator=data_collator,
    compute_metrics=compute_metrics,
    tokenizer=processor.feature_extractor,
)

print("=" * 60)
print("Starting training...")
print("Expected time on M1: ~1–2 hours")
print("WER will print every 100 steps — lower is better")
print("=" * 60)
print()

trainer.train()

# ── Save ──────────────────────────────────────────────────────────────────────

print("\nSaving fine-tuned model...")
model.save_pretrained(str(MODEL_OUTPUT))
processor.save_pretrained(str(MODEL_OUTPUT))
tokenizer.save_pretrained(str(MODEL_OUTPUT))

print()
print("=" * 60)
print("Fine-tuning complete!")
print("=" * 60)
print(f"Model saved: {MODEL_OUTPUT}")
print("\nNext: python scripts/test_finetuned.py")