"""
Phase 3 — Step 2: Fine-tune Whisper on Nepali dataset (M1 Mac optimized)
Uses MPS (Metal Performance Shaders) for GPU acceleration on Apple Silicon

Run from project root:
    python scripts/finetune_whisper.py

Output:
    models/whisper-nepali/   ← your fine-tuned model
"""

import os
import json
import torch
import numpy as np
from pathlib import Path
from dataclasses import dataclass
from typing import Any, Dict, List, Union

from datasets import Dataset, DatasetDict, Audio
from transformers import (
    WhisperFeatureExtractor,
    WhisperTokenizer,
    WhisperProcessor,
    WhisperForConditionalGeneration,
    Seq2SeqTrainingArguments,
    Seq2SeqTrainer,
)
import evaluate

# ── Device setup (M1 MPS) ─────────────────────────────────────────────────────

if torch.backends.mps.is_available():
    DEVICE = "mps"
    print("✓ Using Apple M1 GPU (MPS)")
elif torch.cuda.is_available():
    DEVICE = "cuda"
    print("✓ Using CUDA GPU")
else:
    DEVICE = "cpu"
    print("⚠️  Using CPU — training will be slow")

# ── Paths ─────────────────────────────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATASET_DIR  = PROJECT_ROOT / "data" / "datasets" / "whisper_finetune"
MODEL_OUTPUT = PROJECT_ROOT / "models" / "whisper-nepali"
MODEL_OUTPUT.mkdir(parents=True, exist_ok=True)

# ── Config ────────────────────────────────────────────────────────────────────

MODEL_NAME   = "openai/whisper-small"   # base model to fine-tune
LANGUAGE     = "nepali"
TASK         = "transcribe"
SAMPLE_RATE  = 16000

# M1-optimized training settings
# Small dataset (151 samples) → small batch, more epochs
BATCH_SIZE       = 4    # M1 has 8GB unified memory — 4 is safe
GRAD_ACCUM       = 2    # effective batch = 4 × 2 = 8
LEARNING_RATE    = 1e-5
NUM_EPOCHS       = 20   # more epochs compensates for small dataset
WARMUP_STEPS     = 50
SAVE_STEPS       = 100
EVAL_STEPS       = 100
MAX_AUDIO_LENGTH = 30   # seconds — Whisper's max

print("=" * 60)
print("Phase 3 — Whisper fine-tuning (M1 optimized)")
print("=" * 60)
print(f"Base model   : {MODEL_NAME}")
print(f"Device       : {DEVICE}")
print(f"Dataset      : {DATASET_DIR}")
print(f"Output       : {MODEL_OUTPUT}")
print(f"Epochs       : {NUM_EPOCHS}")
print(f"Batch size   : {BATCH_SIZE} (effective: {BATCH_SIZE * GRAD_ACCUM})")
print()

# ── Load dataset from JSONL ───────────────────────────────────────────────────

def load_split(split_name):
    jsonl_path = DATASET_DIR / split_name / "metadata.jsonl"
    audio_dir  = DATASET_DIR / split_name

    records = []
    with open(jsonl_path, encoding="utf-8") as f:
        for line in f:
            record = json.loads(line.strip())
            audio_path = audio_dir / record["file_name"]
            records.append({
                "audio":         str(audio_path),
                "transcription": record["transcription"],
            })
    return records

print("Loading dataset...")
train_records = load_split("train")
test_records  = load_split("test")

train_dataset = Dataset.from_list(train_records)
test_dataset  = Dataset.from_list(test_records)

# Cast audio column so HuggingFace handles resampling automatically
train_dataset = train_dataset.cast_column("audio", Audio(sampling_rate=SAMPLE_RATE))
test_dataset  = test_dataset.cast_column("audio",  Audio(sampling_rate=SAMPLE_RATE))

print(f"✓ Train: {len(train_dataset)} samples")
print(f"✓ Test:  {len(test_dataset)} samples")
print()

# ── Load processor ────────────────────────────────────────────────────────────

print("Loading Whisper processor and model...")
feature_extractor = WhisperFeatureExtractor.from_pretrained(MODEL_NAME)
tokenizer = WhisperTokenizer.from_pretrained(
    MODEL_NAME,
    language=LANGUAGE,
    task=TASK
)
processor = WhisperProcessor.from_pretrained(
    MODEL_NAME,
    language=LANGUAGE,
    task=TASK
)

# ── Load model ────────────────────────────────────────────────────────────────

model = WhisperForConditionalGeneration.from_pretrained(MODEL_NAME)
model.generation_config.language = LANGUAGE
model.generation_config.task = TASK
model.generation_config.forced_decoder_ids = None

# Move to M1 GPU
model = model.to(DEVICE)
print(f"✓ Model loaded on {DEVICE}")
print()

# ── Preprocessing ─────────────────────────────────────────────────────────────

def prepare_dataset(batch):
    audio = batch["audio"]

    # Extract log-mel features
    batch["input_features"] = feature_extractor(
        audio["array"],
        sampling_rate=audio["sampling_rate"]
    ).input_features[0]

    # Tokenize transcript
    batch["labels"] = tokenizer(batch["transcription"]).input_ids
    return batch

print("Preprocessing audio...")
train_dataset = train_dataset.map(
    prepare_dataset,
    remove_columns=train_dataset.column_names,
    desc="Train"
)
test_dataset = test_dataset.map(
    prepare_dataset,
    remove_columns=test_dataset.column_names,
    desc="Test"
)
print("✓ Preprocessing complete")
print()

# ── Data collator ─────────────────────────────────────────────────────────────

@dataclass
class DataCollatorSpeechSeq2SeqWithPadding:
    processor: Any
    decoder_start_token_id: int

    def __call__(self, features: List[Dict[str, Union[List[int], torch.Tensor]]]):
        # Pad input features
        input_features = [
            {"input_features": f["input_features"]} for f in features
        ]
        batch = self.processor.feature_extractor.pad(
            input_features, return_tensors="pt"
        )

        # Pad labels
        label_features = [{"input_ids": f["labels"]} for f in features]
        labels_batch = self.processor.tokenizer.pad(
            label_features, return_tensors="pt"
        )

        # Replace padding token id with -100 (ignored in loss)
        labels = labels_batch["input_ids"].masked_fill(
            labels_batch.attention_mask.ne(1), -100
        )

        # Strip decoder start token if present
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
    pred_ids   = pred.predictions
    label_ids  = pred.label_ids

    # Replace -100 back to pad token
    label_ids[label_ids == -100] = tokenizer.pad_token_id

    pred_str  = tokenizer.batch_decode(pred_ids,  skip_special_tokens=True)
    label_str = tokenizer.batch_decode(label_ids, skip_special_tokens=True)

    wer = 100 * wer_metric.compute(predictions=pred_str, references=label_str)
    print(f"\n  Sample prediction : {pred_str[0]}")
    print(f"  Actual transcript : {label_str[0]}")
    print(f"  WER               : {wer:.2f}%\n")
    return {"wer": wer}

# ── Training arguments (M1 optimized) ────────────────────────────────────────

training_args = Seq2SeqTrainingArguments(
    output_dir=str(MODEL_OUTPUT),

    # M1 MPS settings
    use_mps_device=True,              # enable Metal GPU
    fp16=False,                       # MPS does not support fp16 yet
    bf16=False,                       # bf16 also not stable on MPS

    # Training
    num_train_epochs=NUM_EPOCHS,
    per_device_train_batch_size=BATCH_SIZE,
    gradient_accumulation_steps=GRAD_ACCUM,
    learning_rate=LEARNING_RATE,
    warmup_steps=WARMUP_STEPS,
    weight_decay=0.01,

    # Evaluation
    per_device_eval_batch_size=BATCH_SIZE,
    evaluation_strategy="steps",
    eval_steps=EVAL_STEPS,
    predict_with_generate=True,
    generation_max_length=225,

    # Saving
    save_steps=SAVE_STEPS,
    save_total_limit=2,               # keep only 2 checkpoints (saves disk)
    load_best_model_at_end=True,
    metric_for_best_model="wer",
    greater_is_better=False,          # lower WER = better

    # Logging
    logging_steps=25,
    report_to="none",                 # no wandb/tensorboard needed
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
print("You will see WER (Word Error Rate) improve each eval step")
print("Lower WER = better. Baseline (no fine-tune) ≈ 60–80% WER")
print("=" * 60)
print()

trainer.train()

# ── Save final model ──────────────────────────────────────────────────────────

print()
print("Saving fine-tuned model...")
model.save_pretrained(str(MODEL_OUTPUT))
processor.save_pretrained(str(MODEL_OUTPUT))
tokenizer.save_pretrained(str(MODEL_OUTPUT))

print()
print("=" * 60)
print("Fine-tuning complete!")
print("=" * 60)
print(f"Model saved to: {MODEL_OUTPUT}")
print()
print("Next step — test your fine-tuned model:")
print("  python scripts/test_finetuned.py")
print()
print("Then plug into demo:")
print("  Change whisper.load_model('small') to load from:")
print(f"  {MODEL_OUTPUT}")