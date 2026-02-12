"""
Re-clean the problem files (NP_093-100, NP_101, NP_130, NP_139)
with more aggressive silence detection
"""

from pydub import AudioSegment
from pydub.silence import detect_nonsilent
import os

problem_files = [
    "NP_093.wav", "NP_094.wav", "NP_095.wav", "NP_096.wav",
    "NP_097.wav", "NP_098.wav", "NP_099.wav", "NP_100.wav",
    "NP_101.wav", "NP_130.wav", "NP_139.wav"
]

input_folder = "data/audio"
output_folder = "data/audio_cleaned"

print("Re-cleaning problem files with stricter settings...")
print()

for filename in problem_files:
    input_path = os.path.join(input_folder, filename)
    output_path = os.path.join(output_folder, filename)
    
    if not os.path.exists(input_path):
        print(f"⚠️  {filename}: Not found in originals")
        continue
    
    try:
        audio = AudioSegment.from_wav(input_path)
        original_duration = len(audio) / 1000.0
        
        # More aggressive silence detection
        nonsilent_ranges = detect_nonsilent(
            audio,
            min_silence_len=50,   # Shorter silence threshold (was 100)
            silence_thresh=-40    # Less aggressive (was -50)
        )
        
        if not nonsilent_ranges:
            print(f"⚠️  {filename}: No speech detected")
            continue
        
        # Take ONLY the first speech segment (ignore rest)
        start_trim = nonsilent_ranges[0][0]
        end_trim = nonsilent_ranges[0][1]  # First segment only!
        
        trimmed = audio[start_trim:end_trim]
        
        # Normalize
        normalized = trimmed.normalize()
        
        # Small padding
        silence = AudioSegment.silent(duration=100)
        final = silence + normalized + silence
        
        # Export
        final.export(output_path, format='wav')
        
        new_duration = len(final) / 1000.0
        
        print(f"✓ {filename}:")
        print(f"    Original: {original_duration:.2f}s")
        print(f"    Cleaned:  {new_duration:.2f}s")
        
    except Exception as e:
        print(f"❌ {filename}: {e}")

print()
print("Re-cleaning complete!")