# Nepali Voice AI - Complete Technical Setup Guide
## From Zero to Production-Ready Environment

**Document Version**: 1.0  
**Last Updated**: January 26, 2026  
**Target Platform**: macOS (with Windows notes where applicable)  
**Skill Level Required**: Beginner-friendly  
**Estimated Time**: 2-3 hours for complete setup

---

## Table of Contents

1. [Prerequisites & System Requirements](#1-prerequisites--system-requirements)
2. [Install Core Software](#2-install-core-software)
3. [GitHub Account & Repository Setup](#3-github-account--repository-setup)
4. [Local Development Environment](#4-local-development-environment)
5. [Python Virtual Environment](#5-python-virtual-environment)
6. [Install AI Dependencies](#6-install-ai-dependencies)
7. [Project Structure Creation](#7-project-structure-creation)
8. [Verification & Testing](#8-verification--testing)
9. [First Git Commit & Push](#9-first-git-commit--push)
10. [What You Have Now](#10-what-you-have-now)

---

## 1. Prerequisites & System Requirements

### Hardware Requirements

**Minimum**:
- Mac with Apple Silicon (M1/M2/M3) or Intel processor
- 8GB RAM
- 20GB free disk space
- Internet connection

**Recommended**:
- 16GB RAM
- 50GB free disk space
- Stable broadband connection

### Software Requirements

**macOS Version**: 
- macOS 11 (Big Sur) or later
- Tested on macOS Sonoma 14.x

**Account Requirements**:
- GitHub account (free tier sufficient)
- Administrator access on your Mac

---

## 2. Install Core Software

### 2.1 Install Homebrew (Package Manager)

**What it is**: Homebrew is macOS's package manager, making software installation easier.

**Open Terminal**:
- Press `Command + Space`
- Type: `terminal`
- Press `Enter`

**Install Homebrew**:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**Follow on-screen prompts**:
- Enter your Mac password when asked
- Press `Enter` to continue
- Wait 5-10 minutes for installation

**Verify Installation**:
```bash
brew --version
```

**Expected Output**:
```
Homebrew 4.x.x
```

---

### 2.2 Install Python 3.10

**Why Python 3.10**: Best compatibility with AI libraries. Not 3.12 (too new), not 3.9 (too old).

**Install via Homebrew**:
```bash
brew install python@3.10
```

**Wait 3-5 minutes for installation.**

**Verify Installation**:
```bash
python3.10 --version
```

**Expected Output**:
```
Python 3.10.x
```

**Create Symlink (makes commands easier)**:
```bash
echo 'export PATH="/opt/homebrew/opt/python@3.10/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

**Verify Symlink Works**:
```bash
python3 --version
```

Should show `Python 3.10.x`

---

### 2.3 Install Git

**Check if Git is Already Installed**:
```bash
git --version
```

**If you see version number**: Git is already installed, skip to configuration.

**If not installed**:
```bash
brew install git
```

**Configure Git (Required)**:
```bash
git config --global user.name "Your Full Name"
git config --global user.email "your-email@example.com"
```

**Example**:
```bash
git config --global user.name "Gyanendra Maharjan"
git config --global user.email "gyanendra@example.com"
```

**Verify Configuration**:
```bash
git config --global --list
```

**Expected Output**:
```
user.name=Your Full Name
user.email=your-email@example.com
```

---

### 2.4 Install VS Code (Text Editor)

**Download**:
1. Go to: https://code.visualstudio.com/
2. Click "Download for macOS"
3. Open the downloaded `.zip` file
4. Drag `Visual Studio Code.app` to Applications folder

**Launch VS Code**:
- Open Applications folder
- Double-click Visual Studio Code

**Install Python Extension**:
1. Click Extensions icon (left sidebar, looks like 4 squares)
2. Search: `Python`
3. Click "Install" on "Python" by Microsoft
4. Wait for installation

**Install Command Line Tools**:
1. In VS Code: Press `Command + Shift + P`
2. Type: `shell command`
3. Select: "Shell Command: Install 'code' command in PATH"
4. Click "Install"

**Verify**:
```bash
code --version
```

Should show version number.

---

## 3. GitHub Account & Repository Setup

### 3.1 Create GitHub Account

**If you don't have one**:
1. Go to: https://github.com/signup
2. Enter email, create password
3. Verify email address
4. Complete setup

**If you already have one**: Continue to next step.

---

### 3.2 Create New Repository

**On GitHub Website**:
1. Click green "New" button (top right)
2. Repository name: `nepali-voice-ai-pilot`
3. Description: `Building a Nepali language Voice AI system (STT + TTS)`
4. Select: **Public** (or Private if you prefer)
5. **Check** "Add a README file"
6. Click "Create repository"

**Important**: Copy your repository URL. It will look like:
```
https://github.com/YOUR-USERNAME/nepali-voice-ai-pilot.git
```

Save this URL - you'll need it soon.

---

## 4. Local Development Environment

### 4.1 Choose Project Location

**Recommended Location**: `Documents` folder

**Navigate to Documents**:
```bash
cd ~/Documents
```

**Verify Location**:
```bash
pwd
```

**Expected Output**:
```
/Users/your-username/Documents
```

---

### 4.2 Clone Repository from GitHub

**Clone Command** (replace YOUR-USERNAME with your actual GitHub username):
```bash
git clone https://github.com/YOUR-USERNAME/nepali-voice-ai-pilot.git
```

**Example**:
```bash
git clone https://github.com/nepaman/nepali-voice-ai-pilot.git
```

**Expected Output**:
```
Cloning into 'nepali-voice-ai-pilot'...
remote: Enumerating objects: 3, done.
remote: Counting objects: 100% (3/3), done.
remote: Total 3 (delta 0), reused 0 (delta 0)
Receiving objects: 100% (3/3), done.
```

**Enter Project Folder**:
```bash
cd nepali-voice-ai-pilot
```

**Verify You're Inside**:
```bash
pwd
```

**Expected Output**:
```
/Users/your-username/Documents/nepali-voice-ai-pilot
```

---

## 5. Python Virtual Environment

### 5.1 Create Virtual Environment

**What is Virtual Environment**: An isolated Python workspace for this project only. Prevents conflicts with other projects.

**Create Environment**:
```bash
python3 -m venv venv
```

**This takes 1-2 minutes. Wait for command prompt to return.**

**Verify Creation**:
```bash
ls -la | grep venv
```

**Expected Output**:
```
drwxr-xr-x  6 user  staff  192 Jan 26 10:00 venv
```

---

### 5.2 Activate Virtual Environment

**Activation Command**:
```bash
source venv/bin/activate
```

**Visual Confirmation**:
Your terminal prompt should change from:
```
your-username@MacBook nepali-voice-ai-pilot %
```

To:
```
(venv) your-username@MacBook nepali-voice-ai-pilot %
```

**The `(venv)` prefix means it's active. **

**Important**: You MUST activate the virtual environment every time you work on this project.

---

### 5.3 Upgrade pip

**Why**: Ensures latest package installer version.

```bash
python -m pip install --upgrade pip
```

**Verify pip Version**:
```bash
pip --version
```

**Expected Output**:
```
pip 24.x.x from /Users/your-username/Documents/nepali-voice-ai-pilot/venv/lib/python3.10/site-packages/pip (python 3.10)
```

---

## 6. Install AI Dependencies

### 6.1 Install PyTorch (AI Framework)

**For Mac (CPU-based)**:
```bash
pip install torch torchvision torchaudio
```

**This is LARGE (1-2 GB). Takes 5-10 minutes.**

**Progress Indicator**:
```
Collecting torch
  Downloading torch-2.10.0-cp310-none-macosx_11_0_arm64.whl (60.1 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 60.1/60.1 MB 8.5 MB/s eta 0:00:00
```

**Wait for "Successfully installed..." message.**

**Verify Installation**:
```bash
python -c "import torch; print(f'PyTorch {torch.__version__} installed')"
```

**Expected Output**:
```
PyTorch 2.10.0 installed
```

---

### 6.2 Install OpenAI Whisper (Speech-to-Text)

**Install Command**:
```bash
pip install openai-whisper
```

**Takes 2-3 minutes.**

**Verify Installation**:
```bash
python -c "import whisper; print('Whisper installed successfully')"
```

**Expected Output**:
```
Whisper installed successfully
```

---

### 6.3 Install Audio Processing Libraries

**Install All at Once**:
```bash
pip install numpy scipy soundfile librosa
```

**Takes 2-3 minutes.**

**Verify Installation**:
```bash
python -c "import soundfile; import librosa; print('Audio libraries installed')"
```

**Expected Output**:
```
Audio libraries installed
```

---

### 6.4 Install Text-to-Speech Library

**Install gTTS**:
```bash
pip install gTTS
```

**Takes 30 seconds.**

**Verify Installation**:
```bash
python -c "from gtts import gTTS; print('gTTS installed')"
```

**Expected Output**:
```
gTTS installed
```

---

### 6.5 Install Gradio (Web Interface)

**Install Command**:
```bash
pip install gradio
```

**Takes 2-3 minutes.**

**Verify Installation**:
```bash
python -c "import gradio; print(f'Gradio {gradio.__version__} installed')"
```

**Expected Output**:
```
Gradio 6.x.x installed
```

---

### 6.6 Install Additional Utilities

**Install Remaining Packages**:
```bash
pip install python-dotenv tqdm
```

**Verify All Installations**:
```bash
pip list
```

**You should see a LONG list including**:
- torch
- openai-whisper
- gradio
- gTTS
- librosa
- soundfile
- numpy
- scipy

---

## 7. Project Structure Creation

### 7.1 Create Folder Structure

**Create All Folders with One Command**:
```bash
mkdir -p docs scripts/{setup,stt,tts,utils} data/audio/{raw,processed,test} data/{transcripts,datasets} models/{stt,tts,checkpoints} web/{static,templates} tests
```

**Verify Structure**:
```bash
tree -L 2 -d
```

**If `tree` not installed**:
```bash
brew install tree
```

**Then run `tree -L 2 -d` again.**

**Expected Output**:
```
.
├── data
│   ├── audio
│   ├── datasets
│   └── transcripts
├── docs
├── models
│   ├── checkpoints
│   ├── stt
│   └── tts
├── scripts
│   ├── setup
│   ├── stt
│   ├── tts
│   └── utils
├── tests
├── venv
└── web
    ├── static
    └── templates
```

---

### 7.2 Create .gitignore File

**Purpose**: Tells Git which files NOT to track (large files, temporary files).

**Create File**:
```bash
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
*.m4a
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
```

**Verify File Created**:
```bash
cat .gitignore
```

Should display the content you just created.

---

### 7.3 Create requirements.txt

**Purpose**: Documents all Python packages needed for the project.

**Create File**:
```bash
cat > requirements.txt << 'EOF'
# Core AI Dependencies
openai-whisper>=20231117
torch>=2.0.0
torchaudio>=2.0.0
torchvision>=0.15.0

# Audio Processing
numpy>=1.24.0
scipy>=1.10.0
soundfile>=0.12.0
librosa>=0.10.0

# Text-to-Speech
gTTS>=2.4.0
TTS>=0.22.0

# Web Interface
gradio>=4.0.0

# Utilities
python-dotenv>=1.0.0
tqdm>=4.66.0
EOF
```

**Verify File Created**:
```bash
cat requirements.txt
```

---

### 7.4 Create Test Setup Script

**Purpose**: Verify all packages are installed correctly.

**Create File**:
```bash
cat > scripts/test_setup.py << 'EOF'
"""
Setup Verification Script
Tests that all required packages are installed and working.
"""

import sys

print("=" * 60)
print("Nepali Voice AI - Setup Verification")
print("=" * 60)
print()

# Test Python version
print(f"Python version: {sys.version}")
print()

# Test imports
packages = [
    ("whisper", "OpenAI Whisper"),
    ("torch", "PyTorch"),
    ("gradio", "Gradio"),
    ("gtts", "gTTS"),
    ("soundfile", "Soundfile"),
    ("librosa", "Librosa"),
    ("numpy", "NumPy"),
    ("scipy", "SciPy"),
]

print("Testing package imports...")
print()

all_ok = True

for module_name, display_name in packages:
    try:
        module = __import__(module_name)
        version = getattr(module, "__version__", "unknown")
        print(f"✓ {display_name:20} - version {version}")
    except ImportError:
        print(f"✗ {display_name:20} - NOT INSTALLED")
        all_ok = False

print()
print("=" * 60)

if all_ok:
    print("SUCCESS: All packages installed correctly!")
    print("You are ready to begin development.")
else:
    print("ERROR: Some packages are missing.")
    print("Run: pip install -r requirements.txt")

print("=" * 60)
EOF
```

**Verify File Created**:
```bash
cat scripts/test_setup.py
```

---

### 7.5 Create CHANGELOG.md

**Purpose**: Track all project changes over time.

**Create File**:
```bash
cat > CHANGELOG.md << 'EOF'
# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - 2026-01-26

### Added
- Initial project structure
- Complete development environment setup
- Python 3.10 with virtual environment
- Installed core dependencies:
  - OpenAI Whisper for Speech-to-Text
  - PyTorch for AI/ML operations
  - Gradio for web interfaces
  - gTTS for Text-to-Speech
  - Audio processing libraries (librosa, soundfile)
- Created folder structure for organized development
- Setup verification script
- Documentation framework
- Git repository initialized and connected to GitHub

### Technical Setup Completed
- macOS development environment
- Git version control configured
- Virtual environment isolated from system Python
- All AI dependencies installed and verified
- Ready for Phase 1: STT testing
EOF
```

---

## 8. Verification & Testing

### 8.1 Run Setup Test Script

**Ensure Virtual Environment is Active**:
Check for `(venv)` prefix in terminal. If not there:
```bash
source venv/bin/activate
```

**Run Test Script**:
```bash
python scripts/test_setup.py
```

**Expected Output**:
```
============================================================
Nepali Voice AI - Setup Verification
============================================================

Python version: 3.10.x

Testing package imports...

✓ OpenAI Whisper       - version 20231117
✓ PyTorch              - version 2.10.0
✓ Gradio               - version 6.4.0
✓ gTTS                 - version 2.5.4
✓ Soundfile            - version 0.13.1
✓ Librosa              - version 0.11.0
✓ NumPy                - version 2.2.6
✓ SciPy                - version 1.15.3

============================================================
SUCCESS: All packages installed correctly!
You are ready to begin development.
============================================================
```

**If any package shows ✗**: Go back to section 6 and reinstall that package.

---

### 8.2 Test Whisper Model Loading

**Quick Test** (downloads small model, ~150MB):
```bash
python -c "import whisper; model = whisper.load_model('tiny'); print('Whisper model loaded successfully')"
```

**This will**:
1. Download tiny model (~150MB) - takes 1-3 minutes
2. Load it into memory
3. Print success message

**Expected Output**:
```
100%|████████████████████████████████████| 150M/150M [00:45<00:00, 3.50MB/s]
Whisper model loaded successfully
```

**Note**: The downloaded model is saved in `~/.cache/whisper/` for future use.

---

### 8.3 Verify Git Status

**Check Git Status**:
```bash
git status
```

**Expected Output**:
```
On branch main
Your branch is up to date with 'origin/main'.

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        .gitignore
        CHANGELOG.md
        requirements.txt
        scripts/
        data/
        models/
        tests/
        web/
        docs/
```

This is normal - these are new files Git hasn't tracked yet.

---

## 9. First Git Commit & Push

### 9.1 Stage All Files

**Add All New Files to Git**:
```bash
git add .
```

**Verify What's Staged**:
```bash
git status
```

**Expected Output** (files should be GREEN):
```
On branch main
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        new file:   .gitignore
        new file:   CHANGELOG.md
        new file:   requirements.txt
        new file:   scripts/test_setup.py
        [... more files ...]
```

---

### 9.2 Create First Commit

**Commit with Descriptive Message**:
```bash
git commit -m "Initial setup: Complete development environment

- Installed Python 3.10 with virtual environment
- Installed all AI dependencies (Whisper, PyTorch, Gradio, gTTS)
- Created project folder structure
- Added setup verification script
- Configured Git with .gitignore
- Ready for Phase 1: STT testing"
```

**Expected Output**:
```
[main abc1234] Initial setup: Complete development environment
 XX files changed, XXX insertions(+)
 create mode 100644 .gitignore
 create mode 100644 CHANGELOG.md
 create mode 100644 requirements.txt
 create mode 100755 scripts/test_setup.py
 [... more files ...]
```

---

### 9.3 Push to GitHub

**Push to Remote Repository**:
```bash
git push origin main
```

**Expected Output**:
```
Enumerating objects: XX, done.
Counting objects: 100% (XX/XX), done.
Delta compression using up to 8 threads
Compressing objects: 100% (XX/XX), done.
Writing objects: 100% (XX/XX), XX.XX KiB | XX.XX MiB/s, done.
Total XX (delta X), reused 0 (delta 0), pack-reused 0
To https://github.com/YOUR-USERNAME/nepali-voice-ai-pilot.git
   abc1234..def5678  main -> main
```

---

### 9.4 Verify on GitHub

**Open Browser**:
1. Go to: `https://github.com/YOUR-USERNAME/nepali-voice-ai-pilot`
2. You should see:
   - Updated README.md
   - Folder structure (data/, docs/, scripts/, models/, etc.)
   - .gitignore file
   - requirements.txt
   - CHANGELOG.md
   - Latest commit message visible

**Take a screenshot! This is your first major milestone.**

---

## 10. What You Have Now

### Complete Development Environment

**Software Installed**:
- Python 3.10 (isolated virtual environment)
- Git (version control)
- VS Code (code editor)
- Homebrew (package manager)

**AI & ML Packages**:
- OpenAI Whisper (Speech-to-Text)
- PyTorch 2.x (AI framework)
- Gradio (web interfaces)
- gTTS (Text-to-Speech)
- Audio processing libraries (librosa, soundfile, numpy, scipy)

**Project Infrastructure**:
- Professional folder structure
- Git repository connected to GitHub
- Setup verification script
- Documentation framework
- .gitignore (prevents large file uploads)
- requirements.txt (package documentation)

---

### Current Status

**Phase 0: Foundation Setup** - **COMPLETE**

You now have:
1. A fully functional AI development environment
2. All necessary tools installed and verified
3. Professional project organization
4. Version control connected to GitHub
5. Ability to run AI models (Whisper)

**You are production-ready for AI development.**

---

### What's Next: Phase 1

**Next Steps** (Week 1-2):
1. Record 5-10 test sentences in Nepali
2. Create first STT (Speech-to-Text) script
3. Load Whisper model
4. Transcribe Nepali audio
5. Evaluate accuracy
6. Document results

**Estimated Time**: 5-10 hours of work

**Expected Outcome**: Working demo that transcribes spoken Nepali into text

---

### Daily Workflow Going Forward

**Every Time You Work on This Project**:

```bash
# 1. Navigate to project
cd ~/Documents/nepali-voice-ai-pilot

# 2. Activate virtual environment
source venv/bin/activate

# 3. Check status
git status

# 4. Do your work (write code, test, etc.)

# 5. When done, commit changes
git add .
git commit -m "Description of what you did"
git push origin main

# 6. Deactivate when completely done
deactivate
```

---

### Troubleshooting Reference

**If Virtual Environment Won't Activate**:
```bash
# Try with full path
source ~/Documents/nepali-voice-ai-pilot/venv/bin/activate
```

**If Package Import Fails**:
```bash
# Ensure virtual environment is active (look for (venv) prefix)
# Reinstall package
pip install --force-reinstall [package-name]
```

**If Git Push Fails**:
```bash
# Pull latest changes first
git pull origin main
# Then push again
git push origin main
```

**If Python Version Wrong**:
```bash
# Use explicit version
python3.10 -m venv venv
```

---

### Documentation Files

Your project now includes:

| File | Purpose |
|------|---------|
| `README.md` | Project overview (from GitHub) |
| `CHANGELOG.md` | Track all changes |
| `requirements.txt` | Python dependencies |
| `.gitignore` | Files Git should ignore |
| `scripts/test_setup.py` | Verify installation |

---

### Skills You've Gained

By completing this setup, you now know:
- How to use Terminal/command line
- How to install software via Homebrew
- How to create Python virtual environments
- How to install Python packages with pip
- Basic Git workflow (add, commit, push)
- GitHub repository management
- Project structure organization
- How to verify AI package installations

**These are foundational skills for any AI/ML developer.**

---

### Congratulations!

You have successfully built a professional AI development environment from scratch.

**What seemed complex is now organized and manageable.**

The hardest part (setup) is done. The exciting part (building AI features) begins next.

**You're ready to build something amazing.** 

---

## Quick Reference Commands

```bash
# Navigate to project
cd ~/Documents/nepali-voice-ai-pilot

# Activate environment
source venv/bin/activate

# Check what changed
git status

# Save changes
git add .
git commit -m "Your message"
git push origin main

# Run test script
python scripts/test_setup.py

# Deactivate environment
deactivate

# Update packages
pip install --upgrade [package-name]

# List installed packages
pip list

# Check Python version
python --version
```

---

**Document End**

This setup is complete and verified. Proceed to Phase 1: STT Testing when ready.

**Setup Date**: January 26, 2026  
**Environment**: macOS with Python 3.10  
**Status**: Production Ready