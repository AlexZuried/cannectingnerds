# Configuration for Reddit AI Bot
REDDIT_CONFIG = {
    "client_id": "YOUR_CLIENT_ID",
    "client_secret": "YOUR_CLIENT_SECRET",
    "user_agent": "reddit-ai-bot/1.0",
    "username": "YOUR_USERNAME",
    "password": "YOUR_PASSWORD"
}

# Model backend selection: "ollama" or "llama_cpp"
MODEL_BACKEND = "ollama"  # Change to "llama_cpp" to use llama.cpp

OLLAMA_CONFIG = {
    "host": "http://localhost:11434",
    "model": "llama3.2"  # or your preferred model
}

LLAMA_CPP_CONFIG = {
    "model_path": None,  # Path to .gguf file (None = auto-download from HF)
    "model_name": "TinyLlama/TinyLlama-1.1B-Chat-v1.0",  # HF model for auto-download
    "n_ctx": 2048,  # Context window size
    "n_threads": 4  # Number of CPU threads
}

SUBREDDITS = ["technology", "programming", "artificial"]  # subs to monitor
CHECK_INTERVAL = 300  # seconds between checks
