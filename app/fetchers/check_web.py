import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


url = "https://www.anthropic.com/news"

response = requests.get(url)

print("Status code:", response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

print("Page downloaded successfully!")

article_links = []
seen_urls = set()

for link in soup.find_all("a"):
    href = link.get("href")

    if href and href.startswith("/news/"):
        if href not in seen_urls:
            article_links.append(link)
            seen_urls.add(href)

print("Number of article links:", len(article_links))

for link in article_links:
    href = link.get("href")

    title = link.find("h4")

    if not title:
        title = link.find(
            "span",
            class_=lambda value: value and "title" in value
        )

    published = link.find("time")
    summary = link.find("p")

    print("URL:", href)
    print("Title:", title.get_text(" ", strip=True) if title else None)
    print("Published:", published.get_text(" ", strip=True) if published else None)
    print("Summary:", summary.get_text(" ", strip=True) if summary else None)
    print("-" * 50)