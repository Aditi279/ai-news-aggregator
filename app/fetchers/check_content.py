from app.fetchers.content import fetch_article_content


url = "https://www.anthropic.com/news/claude-text-watermark"

content = fetch_article_content(url)

print("Content length:", len(content))
print()
print(content[:2000])