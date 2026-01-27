"""
Test script to verify all installations are working
"""

print("Testing Python installation...")
import sys
print(f"✓ Python version: {sys.version}")

print("\nTesting required packages...")

try:
    import whisper
    print("✓ Whisper installed")
except ImportError:
    print("✗ Whisper NOT installed")

try:
    import torch
    print(f"✓ PyTorch installed (version {torch.__version__})")
    print(f"  CUDA available: {torch.cuda.is_available()}")
except ImportError:
    print("✗ PyTorch NOT installed")

try:
    import gradio
    print(f"✓ Gradio installed (version {gradio.__version__})")
except ImportError:
    print("✗ Gradio NOT installed")

try:
    from gtts import gTTS
    print("✓ gTTS installed")
except ImportError:
    print("✗ gTTS NOT installed")

try:
    import soundfile
    print("✓ soundfile installed")
except ImportError:
    print("✗ soundfile NOT installed")

try:
    import librosa
    print("✓ librosa installed")
except ImportError:
    print("✗ librosa NOT installed")

print("\n" + "="*50)
print("Setup verification complete!")
print("="*50)
