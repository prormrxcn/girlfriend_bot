# 💖 Deepanshi - AI Girlfriend Chatbot (Tkinter + Ollama)

*A locally-run, privacy-focused AI companion with GUI interface*

![Demo Screenshot](screenshot.png) <!-- Add actual screenshot later -->

## 🌟 Key Features
- **100% Local** - Runs on Ollama with Mistral model (no cloud dependencies)
- **Beautiful Tkinter GUI** - Desktop-native experience with animations
- **Emotional Intelligence** - Context-aware romantic responses
- **No Database** - Memory handled purely via Python lists
- **Multithreaded** - Smooth UI while processing AI responses

## 🛠️ Tech Stack

Python 3.10+
Ollama (Mistral model)
LangChain (for prompt engineering)
Tkinter (GUI)
Pillow (image processing)
📋 Requirements
System Requirements
Any modern CPU (Intel/AMD)

Minimum 8GB RAM (16GB recommended)

4GB free disk space

GPU optional but recommended (NVIDIA/AMD)

Software Requirements
Ollama (Latest version)

Python 3.10 or newer

🔧 Installation
1. Install Ollama
bash
# Linux/macOS
curl -fsSL https://ollama.ai/install.sh | sh

# Windows (PowerShell)
winget install ollama
2. Download Mistral Model
bash
ollama pull mistral
3. Set Up Python Environment
bash
# Clone repository
git clone https://github.com/yourusername/deepanshi-chatbot.git
cd deepanshi-chatbot

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

4. Run the Application

python main.py

bash
# CPU-only mode
python main.py --device cpu

# With GPU acceleration
python main.py --device cuda
🐛 Troubleshooting
If you encounter issues:

Verify Ollama is running:

ollama serve
Check Python version:

python --version
Update packages:

pip install --upgrade -r requirements.txt
💡 Pro Tip: For smoother animations, enable hardware acceleration in your OS display settings!


