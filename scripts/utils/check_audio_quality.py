"""
Check audio file quality - detect issues
"""

import soundfile as sf
import numpy as np
import os

audio_folder = "data/audio"

print("Checking audio quality...")
print()

issues = []

for filename in sorted(os.listdir(audio_folder)):
    if not filename.endswith('.wav'):
        continue
    
    filepath = os.path.join(audio_folder, filename)
    data, sr = sf.read(filepath)
    
    duration = len(data) / sr
    max_volume = np.abs(data).max()
    
    # Detect issues
    problems = []
    
    if duration < 0.5:
        problems.append("TOO SHORT (<0.5s)")
    
    if max_volume < 0.1:
        problems.append("TOO QUIET")
    
    if max_volume > 0.95:
        problems.append("CLIPPING")
    
    # Check for long silence
    silence_threshold = 0.01
    silent_samples = np.sum(np.abs(data) < silence_threshold)
    silence_percent = (silent_samples / len(data)) * 100
    
    if silence_percent > 70:
        problems.append(f"MOSTLY SILENCE ({silence_percent:.0f}%)")
    
    if problems:
        print(f"⚠️  {filename}: {duration:.2f}s - {', '.join(problems)}")
        issues.append(filename)
    else:
        print(f"✓  {filename}: {duration:.2f}s - OK")

print()
print(f"Total files checked: {len(os.listdir(audio_folder))}")
print(f"Files with issues: {len(issues)}")

if issues:
    print("\nProblematic files:")
    for f in issues:
        print(f"  - {f}")