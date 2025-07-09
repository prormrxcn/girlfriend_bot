import subprocess
import platform
import time
from graphics import ChatbotUI
from main_chat_bot import DeepanshiChatbot


def is_ollama_running():
    """Check if Ollama is already serving on localhost:11434"""
    import socket
    try:
        with socket.create_connection(("localhost", 11434), timeout=1):
            return True
    except:
        return False


def start_ollama():
    """Start Ollama in background if it's not already running"""
    if is_ollama_running():
        print("✅ Ollama is already running.")
        return

    try:
        if platform.system() == "Windows":
            subprocess.Popen("ollama serve", creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:
            subprocess.Popen(["ollama", "serve"])

        print("🟢 Ollama is starting...")
        time.sleep(5)  # wait a few seconds for model to load

    except Exception as e:
        print(f"❌ Failed to start Ollama: {e}")


if __name__ == "__main__":
    start_ollama()
    chatbot = DeepanshiChatbot()
    ui = ChatbotUI(chatbot)
    ui.run()
