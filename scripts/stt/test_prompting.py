"""
Test different Whisper prompting strategies to improve accuracy
Experiments with: initial_prompt, temperature, and other parameters
"""

import whisper

print("=" * 70)
print("Whisper Prompting Experiments")
print("=" * 70)
print()

# Load model once
print("Loading Whisper 'small' model...")
model = whisper.load_model("small")
print("✓ Model loaded")
print()

# Test files - pick a few representative ones
test_files = [
    ("NP_011.wav", "शुभ प्रभात"),      # Morning greeting
    ("NP_001.wav", "नमस्कार"),           # Hello
    ("NP_024.wav", "तिमी ठीक छौ"),      # Are you okay
    ("NP_033.wav", "सबै कुरा राम्रो छ"), # Everything is good
]

# Different prompting strategies
strategies = {
    "Baseline (no tweaks)": {
        "language": "ne",
        "fp16": False
    },
    
    "With Nepali initial prompt": {
        "language": "ne",
        "fp16": False,
        "initial_prompt": "नमस्कार। शुभ प्रभात। शुभ बिहानी। नमस्ते।"
    },
    
    "Temperature 0 (conservative)": {
        "language": "ne",
        "fp16": False,
        "temperature": 0.0
    },
    
    "Combined (prompt + temp 0)": {
        "language": "ne",
        "fp16": False,
        "temperature": 0.0,
        "initial_prompt": "नमस्कार शुभ प्रभात शुभ बिहानी शुभ रात्रि"
    },
    
    "Higher temperature (creative)": {
        "language": "ne",
        "fp16": False,
        "temperature": 0.8
    }
}

# Test each file with each strategy
for filename, ground_truth in test_files:
    audio_path = f"data/audio/{filename}"
    
    print("=" * 70)
    print(f"FILE: {filename}")
    print(f"GROUND TRUTH: {ground_truth}")
    print("=" * 70)
    
    for strategy_name, params in strategies.items():
        try:
            result = model.transcribe(audio_path, **params)
            transcription = result['text'].strip()
            
            # Simple match check
            match = "✓ EXACT" if transcription == ground_truth else "✗ Different"
            
            print(f"\n{strategy_name}:")
            print(f"  Result: {transcription}")
            print(f"  {match}")
            
        except Exception as e:
            print(f"\n{strategy_name}:")
            print(f"  ERROR: {e}")
    
    print()

print("=" * 70)
print("Experiment complete!")
print("=" * 70)
print()
print("ANALYSIS:")
print("- Review which strategy produced most exact matches")
print("- Note if initial_prompt helps with Devanagari consistency")
print("- Check if temperature=0 reduces random variations")
print()