# Reddit AI Bot

Autonomous AI bot that connects local Ollama models to Reddit API. It browses subreddits, reads conversations, replies to comments, and creates new threads 24/7.

## Requirements

- Python 3.8+
- [Ollama](https://ollama.ai) running locally
- Reddit API credentials

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start Ollama (in a separate terminal):
```bash
ollama serve
```

3. Pull a model:
```bash
ollama pull llama3.2
```

4. Configure `config.py` with your Reddit credentials:
   - Get credentials at https://www.reddit.com/prefs/apps
   - Create a "script" app type
   - Update REDDIT_CONFIG in config.py

5. Run the bot:
```bash
python bot.py
```

## Files

- `config.py` - Configuration for Reddit and Ollama
- `ollama_client.py` - Local LLM interface
- `reddit_client.py` - Reddit API wrapper
- `bot.py` - Main bot logic with autonomous decision making

## How It Works

1. Monitors configured subreddits every 5 minutes
2. AI analyzes posts and comments to decide actions
3. Generates contextual replies using local Ollama model
4. Creates new discussion threads autonomously
5. Runs continuously without manual intervention

## Customization

Edit `config.py` to:
- Change monitored subreddits
- Adjust check interval
- Use different Ollama model
