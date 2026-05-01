# Reddit AI Bot

A minimal AI-powered Reddit bot that can browse subreddits, reply to conversations, and create new threads 24/7 using local models.

## Features

- **Dual Backend Support**: Use either Ollama or llama.cpp for inference
- **Autonomous Operation**: Browses subs, analyzes content, and decides actions intelligently
- **Auto-reply**: Generates contextual replies to posts and comments
- **Thread Creation**: Creates new discussion threads based on AI inspiration
- **Minimal Setup**: Simple configuration, runs continuously

## Model Backends

### Option 1: Ollama (Default)
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull a model
ollama pull llama3.2

# Start Ollama server
ollama serve
```

### Option 2: llama.cpp (HuggingFace models)
```bash
# Clone and build llama.cpp
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp && make

# Models are auto-downloaded from HuggingFace on first run
# Or specify your own .gguf model path in config.py
```

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Edit `config.py`:

```python
# Choose backend: "ollama" or "llama_cpp"
MODEL_BACKEND = "ollama"  # or "llama_cpp"

# Reddit credentials (required)
REDDIT_CONFIG = {
    "client_id": "YOUR_CLIENT_ID",
    "client_secret": "YOUR_CLIENT_SECRET",
    "user_agent": "reddit-ai-bot/1.0",
    "username": "YOUR_USERNAME",
    "password": "YOUR_PASSWORD"
}

# Subreddits to monitor
SUBREDDITS = ["technology", "programming", "artificial"]
```

## Usage

```bash
python bot.py
```

The bot will:
1. Connect to your chosen model backend
2. Monitor configured subreddits
3. Analyze posts and comments with AI
4. Decide whether to reply, create posts, or skip
5. Run continuously (24/7)

## Files

- `bot.py` - Main bot logic
- `config.py` - Configuration settings
- `model_factory.py` - Backend selector (Ollama vs llama.cpp)
- `ollama_client.py` - Ollama API client
- `llama_cpp_client.py` - llama.cpp client with HF auto-download
- `reddit_client.py` - Reddit API wrapper
- `requirements.txt` - Python dependencies

## Notes

- For llama.cpp: Ensure `./main` binary exists in the repo root or update the path
- GGUF models are automatically downloaded from HuggingFace if not specified
- Adjust `CHECK_INTERVAL` in config to control how often the bot checks for new content
- The bot tracks processed items to avoid duplicate actions
