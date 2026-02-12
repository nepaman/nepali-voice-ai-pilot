"""
Clean audio files: Remove silence, normalize volume
"""

from pydub import AudioSegment
from pydub.silence import detect_nonsilent
import os

input_folder = "data/audio"
output_folder = "data/audio_cleaned"

# Create output folder
os.makedirs(output_folder, exist_ok=True)

print("Cleaning audio files...")
print()

for filename in sorted(os.listdir(input_folder)):
    if not filename.endswith('.wav'):
        continue
    
    input_path = os.path.join(input_folder, filename)
    output_path = os.path.join(output_folder, filename)
    
    try:
        # Load audio
        audio = AudioSegment.from_wav(input_path)
        
        # Get original duration
        original_duration = len(audio) / 1000.0
        
        # Detect non-silent parts (speech)
        # min_silence_len: minimum silence length in ms
        # silence_thresh: silence threshold in dBFS
        nonsilent_ranges = detect_nonsilent(
            audio,
            min_silence_len=100,  # 100ms of silence
            silence_thresh=-50    # -50 dBFS threshold
        )
        
        if not nonsilent_ranges:
            print(f"⚠️  {filename}: No speech detected, skipping")
            continue
        
        # Get start and end of actual speech
        start_trim = nonsilent_ranges[0][0]
        end_trim = nonsilent_ranges[-1][1]
        
        # Trim to speech only
        trimmed = audio[start_trim:end_trim]
        
        # Normalize volume (boost to -20 dBFS target)
        normalized = trimmed.normalize()
        
        # Add small padding (100ms before and after)
        silence = AudioSegment.silent(duration=100)
        final = silence + normalized + silence
        
        # Export
        final.export(output_path, format='wav')
        
        new_duration = len(final) / 1000.0
        
        print(f"✓ {filename}:")
        print(f"    Before: {original_duration:.2f}s")
        print(f"    After:  {new_duration:.2f}s")
        print(f"    Trimmed: {original_duration - new_duration:.2f}s of silence")
        
    except Exception as e:
        print(f"❌ {filename}: Error - {e}")

print()
print("Cleaning complete!")
print(f"Cleaned files saved to: {output_folder}")