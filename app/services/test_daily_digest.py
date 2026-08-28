from datetime import date, datetime, timedelta, timezone

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.db.models import Base, Digest
from app.db.repositories import create_article, get_or_create_source
from app.services.daily_digest import create_daily_digest


def test_create_daily_digest(monkeypatch):
    test_engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(test_engine)

    with Session(test_engine) as session:
        source = get_or_create_source(
            session=session,
            name="Test Digest Source",
            source_type="blog",
            url="https://example.com/digest",
        )

        article = create_article(
            session=session,
            source_id=source.id,
            title="Test AI article",
            url="https://example.com/test-digest-article",
            published_at=datetime.now(timezone.utc),
            summary="Test article summary",
            content="This is the full article content.",
        )

        article.ai_summary = "This is the AI summary."
        session.commit()

        def fake_generate_digest(articles):
            return "Today's AI news digest."

        monkeypatch.setattr(
            "app.services.daily_digest.generate_digest",
            fake_generate_digest,
        )

        published_after = article.published_at - timedelta(seconds=1)

        digest_id = create_daily_digest(
            session=session,
            digest_date=date.today(),
            published_after=published_after,
        )

        assert isinstance(digest_id, int)

        digest = session.get(Digest, digest_id)

        assert digest is not None
        assert digest.content == "Today's AI news digest."
        assert digest.digest_date == date.today()

def test_create_daily_digest_does_not_duplicate(monkeypatch):
    test_engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(test_engine)

    with Session(test_engine) as session:
        source = get_or_create_source(
            session=session,
            name="Test Duplicate Digest Source",
            source_type="blog",
            url="https://example.com/duplicate",
        )

        article = create_article(
            session=session,
            source_id=source.id,
            title="Test duplicate digest article",
            url="https://example.com/test-duplicate-digest",
            published_at=datetime.now(timezone.utc),
            summary="Test article summary",
            content="This is the full article content.",
        )

        article.ai_summary = "This is the AI summary."
        session.commit()

        def fake_generate_digest(articles):
            return "Today's AI news digest."

        monkeypatch.setattr(
            "app.services.daily_digest.generate_digest",
            fake_generate_digest,
        )

        published_after = article.published_at - timedelta(seconds=1)
        digest_date = date.today()

        first_digest_id = create_daily_digest(
            session=session,
            digest_date=digest_date,
            published_after=published_after,
        )

        second_digest_id = create_daily_digest(
            session=session,
            digest_date=digest_date,
            published_after=published_after,
        )

        assert isinstance(first_digest_id, int)
        assert second_digest_id is None

def test_create_daily_digest_with_no_articles():
    test_engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(test_engine)

    with Session(test_engine) as session:
        digest_id = create_daily_digest(
            session=session,
            digest_date=date.today(),
            published_after=datetime.now(timezone.utc),
        )

        assert digest_id is None