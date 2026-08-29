from datetime import datetime, timedelta, timezone

import requests
from sqlalchemy.orm import Session

from app.db.models import Base
from app.db.repositories import create_article, get_or_create_source
from app.services.fetch_content import fetch_missing_content
from tests.conftest import test_engine


def test_fetch_missing_content(monkeypatch):
    Base.metadata.create_all(test_engine)

    with Session(test_engine) as session:
        source = get_or_create_source(
            session=session,
            name="Test Content Source",
            source_type="blog",
            url="https://example.com",
        )

        article = create_article(
            session=session,
            source_id=source.id,
            title="Test article",
            url="https://example.com/test-article",
            published_at=datetime.now(timezone.utc),
            summary="Test summary",
            content=None,
        )

        def fake_fetch_article_content(url):
            return "This is the fetched article content."

        monkeypatch.setattr(
            "app.services.fetch_content.fetch_article_content",
            fake_fetch_article_content,
        )

        created_after = article.created_at - timedelta(seconds=1)

        updated_articles = fetch_missing_content(
            session=session,
            created_after=created_after,
        )

        session.refresh(article)

        assert updated_articles == 1
        assert article.content == "This is the fetched article content."


def test_fetch_missing_content_marks_404_as_failed(monkeypatch):
    Base.metadata.create_all(test_engine)

    with Session(test_engine) as session:
        source = get_or_create_source(
            session=session,
            name="Test 404 Source",
            source_type="blog",
            url="https://example.com",
        )

        article = create_article(
            session=session,
            source_id=source.id,
            title="Test 404 article",
            url="https://example.com/missing-article",
            published_at=datetime.now(timezone.utc),
            summary="Test summary",
            content=None,
        )

        def fake_fetch_article_content(url):
            response = requests.Response()
            response.status_code = 404
            response.url = url

            raise requests.HTTPError(
                "404 Not Found",
                response=response,
            )

        monkeypatch.setattr(
            "app.services.fetch_content.fetch_article_content",
            fake_fetch_article_content,
        )

        created_after = article.created_at - timedelta(seconds=1)

        updated_articles = fetch_missing_content(
            session=session,
            created_after=created_after,
        )

        session.refresh(article)

        assert updated_articles == 0
        assert article.content is None
        assert article.content_fetch_failed is True