from pathlib import Path
import soundfile as sf
import numpy as np

SRC_DIR = Path("data") / "audio"
OUT_DIR = Path("data") / "audio_normalized"

TARGET_SR = 16000

def resample_audio():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    wav_files = sorted(SRC_DIR.glob("*.wav"))
    print(f"Found {len(wav_files)} source wav files")

    for wav_path in wav_files:
        data, sr = sf.read(wav_path)

        # stereo भए mono मा convert
        if data.ndim > 1:
            data = np.mean(data, axis=1)

        # resample (simple method)
        if sr != TARGET_SR:
            duration = len(data) / sr
            new_length = int(duration * TARGET_SR)
            data = np.interp(
                np.linspace(0, len(data), new_length, endpoint=False),
                np.arange(len(data)),
                data,
            )
            sr = TARGET_SR

        # हल्का volume normalize
        peak = np.max(np.abs(data))
        if peak > 0:
            data = data / peak * 0.95

        out_path = OUT_DIR / wav_path.name
        sf.write(out_path, data, sr)
        print(f"Saved {out_path.name} at {sr} Hz")

if __name__ == "__main__":
    resample_audio()
