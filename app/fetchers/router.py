from app.fetchers.rss import fetch_feed
from app.fetchers.anthropic import fetch_anthropic


def fetch_articles(url, fetch_method):
    if fetch_method == "rss":
        return fetch_feed(url)

    if fetch_method == "web":
        return fetch_anthropic(url)

    raise ValueError(f"Unknown fetch method: {fetch_method}")