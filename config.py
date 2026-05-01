# Configuration for Reddit AI Bot
REDDIT_CONFIG = {
    "client_id": "YOUR_CLIENT_ID",
    "client_secret": "YOUR_CLIENT_SECRET",
    "user_agent": "reddit-ai-bot/1.0",
    "username": "YOUR_USERNAME",
    "password": "YOUR_PASSWORD"
}

OLLAMA_CONFIG = {
    "host": "http://localhost:11434",
    "model": "llama3.2"  # or your preferred model
}

SUBREDDITS = ["technology", "programming", "artificial"]  # subs to monitor
CHECK_INTERVAL = 300  # seconds between checks
