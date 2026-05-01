import time
import random
from config import SUBREDDITS, CHECK_INTERVAL, MODEL_BACKEND
from model_factory import get_model_client
from reddit_client import RedditClient

class RedditAIBot:
    def __init__(self):
        self.model = get_model_client()
        self.reddit = RedditClient()
        self.processed = set()  # Track processed items

    def decide_action(self, content_type, content):
        """AI decides what action to take"""
        prompt = f"""You are a Reddit AI assistant. Analyze this {content_type} and decide your action.
Options: REPLY, CREATE_POST, SKIP

{content_type.upper()}: {content[:500]}

Respond with only one word: REPLY, CREATE_POST, or SKIP"""

        response = self.model.generate(prompt).strip().upper()
        if "REPLY" in response:
            return "REPLY"
        elif "CREATE_POST" in response:
            return "CREATE_POST"
        return "SKIP"

    def generate_reply(self, context):
        """Generate a contextual reply"""
        prompt = f"""You are participating in a Reddit conversation. Write a thoughtful, engaging reply (2-4 sentences).

Context: {context[:800]}

Your reply:"""
        return self.model.generate(prompt)

    def generate_post_idea(self, subreddit):
        """Generate a new post idea for a subreddit"""
        prompt = f"""Create an engaging post title and short content for r/{subreddit}.
Format:
TITLE: [your title]
CONTENT: [2-3 sentences]

Make it relevant and discussion-worthy."""
        return self.model.generate(prompt)

    def process_subreddit(self, subreddit_name):
        """Process a subreddit"""
        print(f"\nProcessing r/{subreddit_name}...")
        posts = self.reddit.get_hot_posts(subreddit_name, limit=3)

        for title, text, post_id, url in posts:
            if post_id in self.processed:
                continue

            content = f"{title}\n\n{text}"
            action = self.decide_action("post", content)

            if action == "REPLY":
                reply = self.generate_reply(content)
                if reply:
                    self.reddit.reply_to_post(post_id, reply)
                    self.processed.add(post_id)

            elif action == "CREATE_POST":
                # Browse other subs for inspiration
                pass

            # Check comments
            comments = self.reddit.get_comments(post_id, limit=5)
            for comment_body, comment_id, parent_id in comments:
                if comment_id in self.processed:
                    continue

                action = self.decide_action("comment", comment_body)
                if action == "REPLY":
                    reply = self.generate_reply(f"Post: {title}\nComment: {comment_body}")
                    if reply:
                        self.reddit.reply_to_comment(comment_id, reply)
                        self.processed.add(comment_id)

    def create_new_thread(self):
        """Create a new thread based on AI inspiration"""
        subreddit = random.choice(SUBREDDITS)
        result = self.generate_post_idea(subreddit)

        try:
            lines = result.split("\n")
            title = ""
            content = ""
            for line in lines:
                if line.startswith("TITLE:"):
                    title = line.replace("TITLE:", "").strip()
                elif line.startswith("CONTENT:"):
                    content = line.replace("CONTENT:", "").strip()

            if title:
                self.reddit.create_post(subreddit, title, content)
        except Exception as e:
            print(f"Error creating post: {e}")

    def run(self):
        """Main loop - runs 24/7"""
        print("Reddit AI Bot starting...")

        if not self.model.is_available():
            if MODEL_BACKEND == "ollama":
                print("ERROR: Ollama not running. Start with: ollama serve")
            else:
                print("ERROR: llama.cpp not available. Ensure:")
                print("  1. llama.cpp is compiled (./main exists)")
                print("  2. GGUF model is downloaded")
            return

        print(f"{MODEL_BACKEND} connected. Monitoring subreddits...")

        while True:
            try:
                for subreddit in SUBREDDITS:
                    self.process_subreddit(subreddit)

                # Occasionally create new threads
                if random.random() < 0.3:  # 30% chance each cycle
                    self.create_new_thread()

                print(f"\nSleeping for {CHECK_INTERVAL}s...")
                time.sleep(CHECK_INTERVAL)

            except KeyboardInterrupt:
                print("\nBot stopped by user")
                break
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(60)

if __name__ == "__main__":
    bot = RedditAIBot()
    bot.run()
