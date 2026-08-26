from app.fetchers.router import fetch_articles


articles = fetch_articles(
    "https://www.anthropic.com/news",
    "web",
)

print(f"Articles fetched: {len(articles)}")

for article in articles[:3]:
    print(article.title)