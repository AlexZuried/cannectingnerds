import praw
from config import REDDIT_CONFIG

class RedditClient:
    def __init__(self):
        self.reddit = praw.Reddit(
            client_id=REDDIT_CONFIG["client_id"],
            client_secret=REDDIT_CONFIG["client_secret"],
            user_agent=REDDIT_CONFIG["user_agent"],
            username=REDDIT_CONFIG["username"],
            password=REDDIT_CONFIG["password"]
        )
    
    def get_hot_posts(self, subreddit_name, limit=5):
        """Get hot posts from a subreddit"""
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            return [(post.title, post.selftext, post.id, post.url) 
                    for post in subreddit.hot(limit=limit)]
        except Exception as e:
            print(f"Error fetching posts: {e}")
            return []
    
    def get_comments(self, post_id, limit=10):
        """Get comments from a post"""
        try:
            submission = self.reddit.submission(id=post_id)
            submission.comments.replace_more(limit=0)
            return [(comment.body, comment.id, comment.parent_id) 
                    for comment in submission.comments[:limit]]
        except Exception as e:
            print(f"Error fetching comments: {e}")
            return []
    
    def reply_to_comment(self, comment_id, text):
        """Reply to a comment"""
        try:
            comment = self.reddit.comment(comment_id)
            comment.reply(text)
            print(f"Replied to comment {comment_id}")
            return True
        except Exception as e:
            print(f"Error replying: {e}")
            return False
    
    def reply_to_post(self, post_id, text):
        """Reply to a post"""
        try:
            submission = self.reddit.submission(id=post_id)
            submission.reply(text)
            print(f"Replied to post {post_id}")
            return True
        except Exception as e:
            print(f"Error replying: {e}")
            return False
    
    def create_post(self, subreddit_name, title, text=""):
        """Create a new post"""
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            subreddit.submit(title=title, selftext=text)
            print(f"Created post: {title}")
            return True
        except Exception as e:
            print(f"Error creating post: {e}")
            return False
