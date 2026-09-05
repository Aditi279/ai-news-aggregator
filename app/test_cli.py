from datetime import date, datetime, timezone

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.db.models import Base
from app.db.repositories import get_or_create_source
from app.cli import run_daily_digest, run_ingestion


def test_run_daily_digest(monkeypatch):
    test_engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(test_engine)

    def fake_ingest_feed(
        session,
        feed_url,
        source_name,
        source_type,
        fetch_method,
    ):
        return 0

    def fake_run_content_fetching(
        session,
        created_after,
    ):
        return 0

    def fake_create_daily_digest(
        session,
        digest_date,
        published_after,
    ):
        return 1

    monkeypatch.setattr(
        "app.cli.engine",
        test_engine,
    )

    monkeypatch.setattr(
        "app.cli.ingest_feed",
        fake_ingest_feed,
    )

    monkeypatch.setattr(
        "app.cli.run_content_fetching",
        fake_run_content_fetching,
    )

    monkeypatch.setattr(
        "app.cli.create_daily_digest",
        fake_create_daily_digest,
    )

    with Session(test_engine) as session:
        get_or_create_source(
            session=session,
            name="Test CLI Source",
            source_type="blog",
            url="https://example.com",
        )

    run_daily_digest()


def test_run_ingestion_continues_when_source_fails(monkeypatch):
    test_engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(test_engine)

    with Session(test_engine) as session:
        get_or_create_source(
            session=session,
            name="Working Source",
            source_type="blog",
            url="https://working.example.com",
        )

        get_or_create_source(
            session=session,
            name="Failing Source",
            source_type="blog",
            url="https://failing.example.com",
        )

        def fake_ingest_feed(
            session,
            feed_url,
            source_name,
            source_type,
            fetch_method,
        ):
            if source_name == "Failing Source":
                raise Exception("Source failed")

            return 5

        monkeypatch.setattr(
            "app.cli.ingest_feed",
            fake_ingest_feed,
        )

        total = run_ingestion(session)

    assert total == 5