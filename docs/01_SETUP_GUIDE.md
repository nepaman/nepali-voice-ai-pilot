# Setup Guide - Nepali Voice AI Pilot

## Prerequisites Check

Before starting, verify you have or can install:
- [ ] A computer (Windows, Mac, or Linux)
- [ ] Internet connection
- [ ] At least 10GB free disk space
- [ ] Ability to install software
- [ ] GitHub account (you already have: nepaman)

---

## Part 1: Install Core Software

### 1.1 Install Python

**Check if Python is already installed:**
```bash
python --version
# or
python3 --version
```

**If not installed:**

**Windows:**
1. Go to https://www.python.org/downloads/
2. Download Python 3.11 or 3.10 (NOT 3.12 yet - compatibility)
3. Run installer
4. ✅ **IMPORTANT:** Check "Add Python to PATH"
5. Click "Install Now"

**Mac:**
```bash
# Install Homebrew first if not installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Then install Python
brew install python@3.11
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip
```

**Verify installation:**
```bash
python --version
# Should show: Python 3.11.x or 3.10.x
```

---

### 1.2 Install Git

**Check if Git is installed:**
```bash
git --version
```

**If not installed:**

**Windows:**
1. Download from https://git-scm.com/download/win
2. Run installer with default options

**Mac:**
```bash
brew install git
```

**Linux:**
```bash
sudo apt install git
```

**Configure Git (Important!):**
```bash
git config --global user.name "Gyanendra Maharjan"
git config --global user.email "your-email@example.com"
```

---

### 1.3 Install VS Code (Recommended)

**Why VS Code?**
- Free and powerful
- Great Python support
- Built-in terminal
- Git integration

**Installation:**
1. Go to https://code.visualstudio.com/
2. Download for your OS
3. Install with default options

**Install Python Extension:**
1. Open VS Code
2. Click Extensions icon (left sidebar)
3. Search "Python"
4. Install "Python" by Microsoft

---

## Part 2: Set Up Project

### 2.1 Clone Your Repository

**Open Terminal/Command Prompt:**

**Windows:** Press `Win + R`, type `cmd`, press Enter
**Mac/Linux:** Press `Cmd + Space`, type "terminal", press Enter

**Navigate to where you want the project:**
```bash
# Example: Create in Documents folder
cd Documents
# or
cd ~/Documents
```

**Clone your repository:**
```bash
git clone https://github.com/nepaman/nepali-voice-ai-pilot.git
cd nepali-voice-ai-pilot
```

---

### 2.2 Create Virtual Environment

**What is a virtual environment?**
Think of it as a separate "workspace" for this project's tools, so they don't conflict with other Python projects.

**Create it:**
```bash
# Windows
python -m venv venv

# Mac/Linux
python3 -m venv venv
```

**Activate it:**
```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

**You'll see `(venv)` appear in your terminal - this means it's active!**

---

### 2.3 Create Project Structure

**Create all folders:**

**Windows (Command Prompt):**
```cmd
mkdir docs scripts data models web tests
mkdir scripts\setup scripts\stt scripts\tts scripts\utils
mkdir data\audio data\transcripts data\datasets
mkdir data\audio\raw data\audio\processed data\audio\test
mkdir models\stt models\tts models\checkpoints
mkdir web\static web\templates
```

**Mac/Linux/Windows (PowerShell):**
```bash
mkdir -p docs
mkdir -p scripts/{setup,stt,tts,utils}
mkdir -p data/{audio/{raw,processed,test},transcripts,datasets}
mkdir -p models/{stt,tts,checkpoints}
mkdir -p web/{static,templates}
mkdir -p tests
```

---

### 2.4 Create Essential Files

**Create `.gitignore` file:**
```bash
# Mac/Linux
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# Audio files (too large for Git)
*.wav
*.mp3
*.flac
data/audio/raw/
data/audio/processed/

# Models (too large for Git)
models/*.pt
models/*.pth
models/*.ckpt

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
EOF

# Windows
# Create file manually in VS Code or Notepad
```

**Create `requirements.txt`:**
```bash
cat > requirements.txt << 'EOF'
# Core dependencies
openai-whisper>=20231117
torch>=2.0.0
torchaudio>=2.0.0

# Audio processing
numpy>=1.24.0
scipy>=1.10.0
soundfile>=0.12.0
librosa>=0.10.0

# Text-to-Speech
gTTS>=2.4.0
TTS>=0.22.0

# Web interface
gradio>=4.0.0

# Utilities
python-dotenv>=1.0.0
tqdm>=4.66.0
EOF
```

---

## Part 3: Install Dependencies

### 3.1 Upgrade pip (Important!)
```bash
python -m pip install --upgrade pip
```

### 3.2 Install PyTorch (Special handling)

**Check if you have NVIDIA GPU:**
- Windows: Open Device Manager → Display adapters
- Mac: No NVIDIA GPU support
- Linux: Run `nvidia-smi`

**Install PyTorch:**

**If you have NVIDIA GPU (Windows/Linux):**
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

**If NO GPU (CPU only) or Mac:**
```bash
pip install torch torchvision torchaudio
```

### 3.3 Install Whisper and other dependencies
```bash
pip install openai-whisper
pip install gradio
pip install gTTS
pip install soundfile
pip install librosa
```

**This will take 5-10 minutes - be patient!**

---

## Part 4: Verify Installation

### 4.1 Create Test Script

**Create file `scripts/test_setup.py`:**
```python
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
```

### 4.2 Run Test Script
```bash
python scripts/test_setup.py
```

**Expected output:**
```
Testing Python installation...
✓ Python version: 3.11.x
✓ Whisper installed
✓ PyTorch installed
✓ Gradio installed
✓ gTTS installed
✓ soundfile installed
✓ librosa installed
```

---

## Part 5: First Commit

### 5.1 Add Files to Git
```bash
git add .
git status  # Review what will be committed
```

### 5.2 Commit Changes
```bash
git commit -m "Initial setup: project structure and dependencies"
```

### 5.3 Push to GitHub
```bash
git push origin main
```

---

## Troubleshooting

### Issue: "python: command not found"
**Solution:** 
- Make sure Python is in PATH
- Try `python3` instead of `python`
- Restart terminal after installation

### Issue: "pip: command not found"
**Solution:**
```bash
python -m ensurepip --upgrade
```

### Issue: Whisper installation fails
**Solution:**
```bash
pip install --upgrade pip setuptools wheel
pip install openai-whisper --no-cache-dir
```

### Issue: Can't activate virtual environment
**Windows:** You might need to enable scripts:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue: Out of memory during installation
**Solution:** Install packages one at a time:
```bash
pip install torch
pip install openai-whisper
pip install gradio
# etc...
```

---

## Success Checklist

Before moving to next phase, verify:
- [ ] Python 3.10+ installed and working
- [ ] Git installed and configured
- [ ] VS Code installed (or your preferred editor)
- [ ] Virtual environment created and activated
- [ ] All dependencies installed successfully
- [ ] Test script runs without errors
- [ ] Changes committed and pushed to GitHub

---

## What's Next?

Once setup is complete, proceed to:
**`docs/02_LEARNING_LOG.md`** - Start documenting your journey
**`docs/03_FIRST_STT_TEST.md`** - Run your first Nepali transcription

---

## Need Help?

If you get stuck:
1. Read error messages carefully
2. Search error on Google/Stack Overflow
3. Ask me (Claude) with specific error details
4. Check Whisper documentation: https://github.com/openai/whisper

**Remember:** Every developer faces setup issues. It's normal! Document what you tried and what worked.