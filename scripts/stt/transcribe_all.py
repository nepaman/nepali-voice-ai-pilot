"""
Nepali Voice AI - Batch Audio Transcription
Transcribes all audio files in data/audio/ using Whisper
"""

import whisper
import os
from datetime import datetime

# Configuration
AUDIO_FOLDER = "data/audio"
OUTPUT_FILE = "data/transcripts/transcriptions.txt"
MODEL_SIZE = "base"  # Options: tiny, base, small, medium, large

# Print header
print("=" * 70)
print("Nepali Voice AI - Batch Transcription")
print("=" * 70)
print()

# Load Whisper model
print(f"Loading Whisper '{MODEL_SIZE}' model...")
print("(First time will download ~150MB - be patient!)")
model = whisper.load_model(MODEL_SIZE)
print("✓ Model loaded successfully!")
print()

# Find all audio files
print(f"Scanning folder: {AUDIO_FOLDER}")
audio_files = []

for file in os.listdir(AUDIO_FOLDER):
    if file.endswith(('.wav', '.mp3', '.m4a', '.flac')):
        audio_files.append(file)

audio_files.sort()  # Sort alphabetically

if not audio_files:
    print(f"❌ No audio files found in {AUDIO_FOLDER}")
    print("Please add .wav, .mp3, .m4a, or .flac files to that folder.")
    exit()

print(f"Found {len(audio_files)} audio file(s)")
print()

# Create output folder if doesn't exist
os.makedirs("data/transcripts", exist_ok=True)

# Open output file
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    # Write header
    f.write("=" * 70 + "\n")
    f.write("Nepali Voice AI - Transcription Results\n")
    f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"Model: Whisper {MODEL_SIZE}\n")
    f.write(f"Total Files: {len(audio_files)}\n")
    f.write("=" * 70 + "\n\n")
    
    # Process each audio file
    for i, audio_file in enumerate(audio_files, 1):
        audio_path = os.path.join(AUDIO_FOLDER, audio_file)
        
        print(f"[{i}/{len(audio_files)}] Processing: {audio_file}")
        print("-" * 70)
        
        try:
            # Transcribe with Nepali language forced
            result = model.transcribe(
                audio_path,
                language="ne",  # Force Nepali language
                task="transcribe",  # Transcribe (don't translate)
                fp16=False  # CPU compatibility
            )
            
            transcription = result["text"].strip()
            
            # Print to console
            print(f"Transcription: {transcription}")
            
            # Write to file
            f.write(f"File: {audio_file}\n")
            f.write(f"Transcription: {transcription}\n")
            f.write("-" * 70 + "\n\n")
            
            print("✓ Success")
            
        except Exception as e:
            error_msg = f"❌ Error: {str(e)}"
            print(error_msg)
            f.write(f"File: {audio_file}\n")
            f.write(f"{error_msg}\n")
            f.write("-" * 70 + "\n\n")
        
        print()

print("=" * 70)
print("TRANSCRIPTION COMPLETE!")
print("=" * 70)
print(f"Results saved to: {OUTPUT_FILE}")
print()
print("To view results, run:")
print(f"  cat {OUTPUT_FILE}")
print()