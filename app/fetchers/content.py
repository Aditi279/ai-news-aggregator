import requests
from bs4 import BeautifulSoup


def fetch_article_content(url):
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    paragraphs = soup.find_all("p")

    content_paragraphs = []

    for paragraph in paragraphs[1:]:
        text = paragraph.get_text(" ", strip=True)

        if text:
            content_paragraphs.append(text)

    return "\n\n".join(content_paragraphs)