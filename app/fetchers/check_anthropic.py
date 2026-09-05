from app.fetchers.anthropic import fetch_anthropic


articles = fetch_anthropic("https://www.anthropic.com/news")

print("Articles fetched:", len(articles))

for article in articles:
    print("Title:", article.title)
    print("URL:", article.url)
    print("Published:", article.published)
    print("Summary:", article.summary)
    print()