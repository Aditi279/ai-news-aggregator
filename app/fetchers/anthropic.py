import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from app.models import Article


def fetch_anthropic(url):
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    articles = []
    seen_urls = set()

    for link in soup.find_all("a"):
        href = link.get("href")

        if not href or not href.startswith("/news/"):
            continue

        article_url = urljoin(url, href)

        if article_url in seen_urls:
            continue

        seen_urls.add(article_url)

        published = link.find("time")

        article_response = requests.get(article_url)
        article_response.raise_for_status()

        article_soup = BeautifulSoup(
            article_response.text,
            "html.parser",
        )

        title = article_soup.find("h1")
        summary = title.find_next("p") if title else None

        articles.append(
            Article(
                title=title.get_text(" ", strip=True) if title else None,
                url=article_url,
                published=published.get_text(" ", strip=True)
                if published
                else None,
                summary=summary.get_text(" ", strip=True)
                if summary
                else None,
            )
        )

    return articles