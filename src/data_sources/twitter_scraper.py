import os
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime
import snscrape.modules.twitter as sntwitter

# Load environment variables
load_dotenv()

# Optional: Customize default keywords
DEFAULT_QUERY = "stock market crash OR recession OR inflation"
DEFAULT_LIMIT = 100

def scrape_tweets(query=DEFAULT_QUERY, limit=DEFAULT_LIMIT, lang="en", since="2023-01-01") -> pd.DataFrame:
    """
    Scrape recent tweets matching the query using snscrape.
    
    Parameters:
        query (str): The search keyword(s) for Twitter scraping.
        limit (int): Max number of tweets to retrieve.
        lang (str): Language filter (e.g., "en" for English).
        since (str): ISO start date for tweets.
    
    Returns:
        pd.DataFrame: DataFrame containing tweets with metadata.
    """
    print(f" Scraping Twitter for: '{query}' (limit={limit}, lang={lang})")
    
    full_query = f"{query} lang:{lang} since:{since}"
    tweets = []
    
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(full_query).get_items()):
        if i >= limit:
            break
        tweets.append({
            "date": tweet.date,
            "username": tweet.user.username,
            "display_name": tweet.user.displayname,
            "content": tweet.content,
            "retweets": tweet.retweetCount,
            "likes": tweet.likeCount,
            "replies": tweet.replyCount,
            "url": tweet.url
        })
    
    df = pd.DataFrame(tweets)
    return df

# CLI Test
if __name__ == "__main__":
    df = scrape_tweets(limit=50)
    print(df.head())

    # Save output
    os.makedirs("../../data", exist_ok=True)
    df.to_csv("../../data/twitter_market_sentiment.csv", index=False)
