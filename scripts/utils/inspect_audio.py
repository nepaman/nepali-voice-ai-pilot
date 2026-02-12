from pathlib import Path
import soundfile as sf  # soundfile already installed

AUDIO_DIR = Path("data") / "audio_normalized"

def inspect_audio(n=5):
    wav_files = sorted(AUDIO_DIR.glob("*.wav"))
    print(f"Found {len(wav_files)} wav files")

    for i, wav_path in enumerate(wav_files[:n]):
        data, sr = sf.read(wav_path)
        duration = len(data) / sr
        print(f"{wav_path.name}: sr={sr}, duration={duration:.2f}s")

if __name__ == "__main__":
    inspect_audio()
