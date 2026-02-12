"""
Test only the files with hallucination problems
NP_093-100, NP_101, NP_130, NP_139
"""

from pathlib import Path
import whisper

PROJECT_ROOT = Path(__file__).resolve().parents[2]
AUDIO_DIR = PROJECT_ROOT / "data" / "audio_cleaned"

# Problem files
problem_files = [
    "NP_093.wav",
    "NP_094.wav",
    "NP_095.wav",
    "NP_096.wav",
    "NP_097.wav",
    "NP_098.wav",
    "NP_099.wav",
    "NP_100.wav",
    "NP_101.wav",
    "NP_130.wav",
    "NP_139.wav",
]

print("=" * 70)
print("Testing Problem Files with Hallucinations")
print("=" * 70)
print()

# Load model
print("Loading Whisper 'small' model...")
model = whisper.load_model("small")
print("✓ Model loaded")
print()

for fname in problem_files:
    audio_path = AUDIO_DIR / fname
    
    if not audio_path.exists():
        print(f"⚠️  Missing: {fname}")
        print()
        continue
    
    print("=" * 70)
    print(f"FILE: {fname}")
    print("=" * 70)
    
    # Check audio properties
    import soundfile as sf
    import numpy as np
    
    data, sr = sf.read(audio_path)
    duration = len(data) / sr
    max_vol = np.abs(data).max()
    silence = (np.sum(np.abs(data) < 0.01) / len(data)) * 100
    
    print(f"Duration: {duration:.2f}s")
    print(f"Max volume: {max_vol:.2f}")
    print(f"Silence: {silence:.0f}%")
    print()
    
    # Transcribe
    print("Transcribing...")
    result = model.transcribe(
        str(audio_path),
        language="ne",
        fp16=False,
        temperature=0.0,
        initial_prompt="नमस्कार शुभ प्रभात"
    )
    
    transcription = result["text"].strip()
    
    # Show only first 200 characters if too long
    if len(transcription) > 200:
        print(f"Transcription (first 200 chars): {transcription[:200]}...")
        print(f"⚠️  HALLUCINATION DETECTED - {len(transcription)} characters!")
    else:
        print(f"Transcription: {transcription}")
    
    print()

print("=" * 70)
print("Test complete!")
print("=" * 70)