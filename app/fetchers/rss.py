import feedparser

from app.models import Article


def fetch_feed(url):
    feed = feedparser.parse(url)

    articles = []

    for entry in feed.entries:
        articles.append(
            Article(
                title=entry.get("title"),
                url=entry.get("link"),
                published=entry.get("published"),
                summary=entry.get("summary"),
            )
        )

    return articles