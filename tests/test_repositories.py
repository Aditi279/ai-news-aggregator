from datetime import date, datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.db.models import Base
from app.db.repositories import (
    create_article,
    create_digest,
    get_all_sources,
    get_article_by_url,
    get_articles_published_after,
    get_articles_without_ai_summary_after,
    get_articles_without_content_after,
    get_digest_by_date,
    get_latest_digest,
    get_or_create_source,
)


def create_test_database():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return engine


def test_create_and_find_source():
    engine = create_test_database()

    with Session(engine) as session:
        source = get_or_create_source(
            session=session,
            name="Test Source",
            source_type="blog",
            url="https://example.com",
        )

        assert source.id is not None
        assert source.name == "Test Source"

        sources = get_all_sources(session)

        assert len(sources) == 1


def test_get_or_create_source_does_not_duplicate():
    engine = create_test_database()

    with Session(engine) as session:
        first_source = get_or_create_source(
            session=session,
            name="Test Source",
            source_type="blog",
            url="https://example.com",
        )

        second_source = get_or_create_source(
            session=session,
            name="Test Source",
            source_type="blog",
            url="https://example.com",
        )

        assert first_source.id == second_source.id

        sources = get_all_sources(session)

        assert len(sources) == 1


def test_create_and_find_article():
    engine = create_test_database()

    with Session(engine) as session:
        source = get_or_create_source(
            session=session,
            name="Test Source",
            source_type="blog",
            url="https://example.com",
        )

        article = create_article(
            session=session,
            source_id=source.id,
            title="Test Article",
            url="https://example.com/article",
            published_at=datetime(2026, 8, 25, 10, 0, 0),
            summary="Test summary",
            content="Test content",
        )

        found_article = get_article_by_url(
            session=session,
            url="https://example.com/article",
        )

        assert found_article is not None
        assert found_article.id == article.id
        assert found_article.title == "Test Article"


def test_get_articles_published_after():
    engine = create_test_database()

    with Session(engine) as session:
        source = get_or_create_source(
            session=session,
            name="Test Source",
            source_type="blog",
            url="https://example.com",
        )

        create_article(
            session=session,
            source_id=source.id,
            title="Older Article",
            url="https://example.com/older",
            published_at=datetime(2026, 8, 23, 10, 0, 0),
            summary="Older",
            content="Older content",
        )

        create_article(
            session=session,
            source_id=source.id,
            title="Newer Article",
            url="https://example.com/newer",
            published_at=datetime(2026, 8, 25, 10, 0, 0),
            summary="Newer",
            content="Newer content",
        )

        articles = get_articles_published_after(
            session=session,
            published_after=datetime(2026, 8, 24, 0, 0, 0),
        )

        assert len(articles) == 1
        assert articles[0].title == "Newer Article"


def test_get_articles_without_content_after():
    engine = create_test_database()

    with Session(engine) as session:
        source = get_or_create_source(
            session=session,
            name="Test Source",
            source_type="blog",
            url="https://example.com",
        )

        article = create_article(
            session=session,
            source_id=source.id,
            title="Missing Content",
            url="https://example.com/missing",
            published_at=datetime(2026, 8, 25, 10, 0, 0),
            summary="Summary",
            content=None,
        )

        articles = get_articles_without_content_after(
            session=session,
            created_after=datetime(2026, 8, 24, 0, 0, 0),
        )

        assert len(articles) == 1
        assert articles[0].id == article.id


def test_get_articles_without_ai_summary_after():
    engine = create_test_database()

    with Session(engine) as session:
        source = get_or_create_source(
            session=session,
            name="Test Source",
            source_type="blog",
            url="https://example.com",
        )

        article = create_article(
            session=session,
            source_id=source.id,
            title="Missing AI Summary",
            url="https://example.com/no-summary",
            published_at=datetime(2026, 8, 25, 10, 0, 0),
            summary="Original summary",
            content="Article content",
        )

        articles = get_articles_without_ai_summary_after(
            session=session,
            published_after=datetime(2026, 8, 24, 0, 0, 0),
        )

        assert len(articles) == 1
        assert articles[0].id == article.id


def test_create_and_find_digest():
    engine = create_test_database()

    with Session(engine) as session:
        digest = create_digest(
            session=session,
            digest_date=date(2026, 8, 25),
            content="Daily AI Digest",
        )

        found_digest = get_digest_by_date(
            session=session,
            digest_date=date(2026, 8, 25),
        )

        assert found_digest is not None
        assert found_digest.id == digest.id
        assert found_digest.content == "Daily AI Digest"


def test_get_latest_digest():
    engine = create_test_database()

    with Session(engine) as session:
        create_digest(
            session=session,
            digest_date=date(2026, 8, 23),
            content="Older digest",
        )

        latest = create_digest(
            session=session,
            digest_date=date(2026, 8, 25),
            content="Latest digest",
        )

        found_digest = get_latest_digest(session)

        assert found_digest is not None
        assert found_digest.id == latest.id
        assert found_digest.content == "Latest digest"