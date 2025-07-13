import os
import pandas as pd
import praw
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables (Reddit credentials)
load_dotenv()

# Load Reddit API credentials from .env
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "crashsentinel-agent")

if not all([REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT]):
    raise ValueError("Reddit API credentials missing in environment variables.")

# Initialize Reddit client
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

def scrape_reddit_posts(subreddit_name="wallstreetbets", query="market crash", limit=100):
    """
    Scrapes recent Reddit posts from a given subreddit using a keyword search.

    Parameters:
        subreddit_name (str): Subreddit to search.
        query (str): Search keyword.
        limit (int): Number of posts to retrieve.

    Returns:
        pd.DataFrame: DataFrame of post titles, dates, scores, and comments.
    """
    print(f" Scraping r/{subreddit_name} for '{query}' (limit={limit})...")
    subreddit = reddit.subreddit(subreddit_name)
    posts = subreddit.search(query, limit=limit, sort="new")

    records = []
    for post in posts:
        records.append({
            "title": post.title,
            "score": post.score,
            "num_comments": post.num_comments,
            "created_utc": datetime.utcfromtimestamp(post.created_utc),
            "url": post.url,
            "id": post.id
        })

    return pd.DataFrame(records)


# CLI test
if __name__ == "__main__":
    df = scrape_reddit_posts(query="recession", limit=50)
    print(df.head())

    # Save to file
    os.makedirs("../../data", exist_ok=True)
    df.to_csv("../../data/reddit_recession_posts.csv", index=False)
