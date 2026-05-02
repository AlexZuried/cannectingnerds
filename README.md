# Reddit AI Bot

A minimal AI-powered Reddit bot that can browse subreddits, reply to conversations, and create new threads 24/7 using local models.

## Features

- **Dual Backend Support**: Use either Ollama or llama.cpp for inference
- **Autonomous Operation**: Browses subs, analyzes content, and decides actions intelligently
- **Auto-reply**: Generates contextual replies to posts and comments
- **Thread Creation**: Creates new discussion threads based on AI inspiration
- **Minimal Setup**: Simple configuration, runs continuously

## Architecture Overview

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   bot.py        │────▶│ model_factory.py │────▶│ OllamaClient    │
│ (Main Logic)    │     │ (Backend Switch) │     │ or              │
└─────────────────┘     └──────────────────┘     │ LlamaCppClient  │
         │                                        └─────────────────┘
         ▼
┌─────────────────┐
│ reddit_client.py│
│ (Reddit API)    │
└─────────────────┘
```

The bot uses a factory pattern to switch between model backends seamlessly. All you need to do is change `MODEL_BACKEND` in `config.py`.

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

#### Step 1: Build llama.cpp
```bash
# Clone and build llama.cpp
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
make

# Verify the main binary exists
ls -la ./main  # Should show the compiled binary
```

#### Step 2: Configure Your Model
Models are stored in GGUF format. You have two options:

**Option A: Auto-download from HuggingFace**
```python
# In config.py
LLAMA_CPP_CONFIG = {
    "model_path": None,  # Will auto-download
    "model_name": "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    "n_ctx": 2048,
    "n_threads": 4
}
```

**Option B: Use Your Own GGUF Model**
```bash
# Download a GGUF model manually
wget https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf
mv llama-2-7b-chat.Q4_K_M.gguf models/
```

```python
# In config.py
LLAMA_CPP_CONFIG = {
    "model_path": "models/llama-2-7b-chat.Q4_K_M.gguf",
    "model_name": None,  # Not needed when using custom path
    "n_ctx": 4096,
    "n_threads": 8
}
```

#### Step 3: Connect the Architecture
Edit `config.py` to use llama.cpp:

```python
# Switch backend
MODEL_BACKEND = "llama_cpp"

# Configure llama.cpp
LLAMA_CPP_CONFIG = {
    "model_path": None,  # Set to None for auto-download, or specify path
    "model_name": "TinyLlama/TinyLlama-1.1B-Chat-v1.0",  # HF model name
    "n_ctx": 2048,       # Context window size
    "n_threads": 4,      # CPU threads for inference
    "temperature": 0.7,  # Sampling temperature
    "top_p": 0.9,        # Top-p sampling
    "llama_cpp_path": "./llama.cpp/main"  # Path to llama.cpp main binary
}
```

#### How It Works
1. **Model Download**: On first run, if `model_path` is `None`, the bot downloads the GGUF model from HuggingFace using `huggingface_hub`
2. **Binary Execution**: The bot calls `./llama.cpp/main` via subprocess with appropriate flags
3. **Inference**: Text is sent to the model, response is parsed and returned
4. **Persistent Mode**: For faster repeated inference, the bot uses stdin/stdout pipes

#### Performance Tips
- Use quantized models (Q4_K_M, Q5_K_M) for faster inference
- Adjust `n_threads` based on your CPU cores
- Increase `n_ctx` for longer context understanding
- Set `temperature` lower (0.3-0.5) for more focused responses

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

## Troubleshooting

### llama.cpp Issues
- **"main binary not found"**: Ensure llama.cpp is built and update `llama_cpp_path` in config
- **"Model not found"**: Check that the GGUF file exists or set `model_path` to `None` for auto-download
- **"Out of memory"**: Use a smaller quantized model or reduce `n_ctx`

### Ollama Issues
- **"Connection refused"**: Make sure `ollama serve` is running
- **"Model not found"**: Run `ollama pull <model-name>`

### Reddit Issues
- **"Invalid credentials"**: Double-check your Reddit API credentials
- **"Rate limited"**: Increase `CHECK_INTERVAL` in config

## Notes

- For llama.cpp: Ensure `./main` binary exists or update `llama_cpp_path` in config
- GGUF models are automatically downloaded from HuggingFace if `model_path` is `None`
- Adjust `CHECK_INTERVAL` in config to control how often the bot checks for new content
- The bot tracks processed items to avoid duplicate actions
- Model files (*.gguf) are gitignored to keep repo size small
