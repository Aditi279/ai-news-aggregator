import requests
from unittest.mock import Mock, patch

from app.fetchers.anthropic import fetch_anthropic


def test_fetch_anthropic_skips_failed_article():
    listing_response = Mock()
    listing_response.text = """
        <a href="/news/article-one">
            <time>Jan 1, 2026</time>
        </a>
        <a href="/news/article-two">
            <time>Jan 2, 2026</time>
        </a>
        <a href="/news/article-three">
            <time>Jan 3, 2026</time>
        </a>
    """
    listing_response.raise_for_status.return_value = None

    article_one_response = Mock()
    article_one_response.text = """
        <h1>Article One</h1>
        <p>Summary one</p>
    """
    article_one_response.raise_for_status.return_value = None

    article_two_response = Mock()
    article_two_response.raise_for_status.side_effect = requests.RequestException(
    "Article failed"
)

    article_three_response = Mock()
    article_three_response.text = """
        <h1>Article Three</h1>
        <p>Summary three</p>
    """
    article_three_response.raise_for_status.return_value = None

    responses = [
        listing_response,
        article_one_response,
        article_two_response,
        article_three_response,
    ]

    with patch(
        "app.fetchers.anthropic.requests.get",
        side_effect=responses,
    ):
        articles = fetch_anthropic("https://www.anthropic.com/news")

    assert len(articles) == 2
    assert articles[0].title == "Article One"
    assert articles[1].title == "Article Three"