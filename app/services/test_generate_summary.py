from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from sqlalchemy import create_engine
from app.db.models import Base
from app.db.repositories import create_article, get_or_create_source
from app.services.generate_summary import generate_missing_summaries


def test_generate_missing_summaries(monkeypatch):
    test_engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(test_engine)

    with Session(test_engine) as session:
        source = get_or_create_source(
            session=session,
            name="Test Summary Source",
            source_type="blog",
            url="https://example.com",
        )

        article = create_article(
            session=session,
            source_id=source.id,
            title="Test AI article",
            url="https://example.com/test-ai-article",
            published_at=datetime.now(timezone.utc),
            summary="Test article summary",
            content="This is the full article content.",
        )

        def fake_summarize_article(content):
            return "This is the AI-generated summary."

        monkeypatch.setattr(
            "app.services.generate_summary.summarize_article",
            fake_summarize_article,
        )

        published_after = article.published_at - timedelta(seconds=1)

        updated_articles = generate_missing_summaries(
            session=session,
            published_after=published_after,
        )

        session.refresh(article)

        assert updated_articles == 1
        assert article.ai_summary == "This is the AI-generated summary."

def test_generate_missing_summaries_handles_failure(monkeypatch):
    test_engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(test_engine)

    with Session(test_engine) as session:
        source = get_or_create_source(
            session=session,
            name="Test Summary Failure Source",
            source_type="blog",
            url="https://example.com/failure",
        )

        article = create_article(
            session=session,
            source_id=source.id,
            title="Test failed summary article",
            url="https://example.com/test-failed-summary",
            published_at=datetime.now(timezone.utc),
            summary="Test article summary",
            content="This is the full article content.",
        )

        def fake_summarize_article(content):
            raise Exception("AI summarization failed")

        monkeypatch.setattr(
            "app.services.generate_summary.summarize_article",
            fake_summarize_article,
        )

        published_after = article.published_at - timedelta(seconds=1)

        updated_articles = generate_missing_summaries(
            session=session,
            published_after=published_after,
        )

        session.refresh(article)

        assert updated_articles == 0
        assert article.ai_summary is None