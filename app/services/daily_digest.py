from datetime import date, datetime

from sqlalchemy.orm import Session

from app.agents.digest import generate_digest
from app.db.repositories import (
    create_digest,
    get_articles_published_after,
    get_digest_by_date,
)
from app.services.generate_summary import generate_missing_summaries


def create_daily_digest(
    session: Session,
    digest_date: date,
    published_after: datetime,
) -> int | None:

    existing_digest = get_digest_by_date(
        session=session,
        digest_date=digest_date,
    )

    if existing_digest:
        print(
            f"Digest already exists for {digest_date}"
        )
        return None

    articles = get_articles_published_after(
        session=session,
        published_after=published_after,
    )

    if not articles:
        print("No new articles found")
        return None

    articles_needing_summaries = [
        article
        for article in articles
        if not article.ai_summary
    ]

    if articles_needing_summaries:
        generate_missing_summaries(
            session=session,
            published_after=published_after,
            limit=len(articles_needing_summaries),
        )

    session.expire_all()

    articles = get_articles_published_after(
        session=session,
        published_after=published_after,
    )

    articles = [
        article
        for article in articles
        if article.ai_summary
    ]

    if not articles:
        print("No summarized articles available")
        return None

    digest_content = generate_digest(articles)

    digest = create_digest(
        session=session,
        digest_date=digest_date,
        content=digest_content,
    )

    print(f"Digest created with ID: {digest.id}")

    return digest.id

def test_create_daily_digest_with_no_summarized_articles(monkeypatch):
    test_engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(test_engine)

    with Session(test_engine) as session:
        source = get_or_create_source(
            session=session,
            name="Test No Summary Source",
            source_type="blog",
            url="https://example.com/no-summary",
        )

        article = create_article(
            session=session,
            source_id=source.id,
            title="Test unsummarized article",
            url="https://example.com/test-unsummarized",
            published_at=datetime.now(timezone.utc),
            summary="Test article summary",
            content="This is the full article content.",
        )

        published_after = article.published_at - timedelta(seconds=1)

        def fake_generate_summaries(
            session,
            published_after,
            limit=10,
        ):
            return 0

        monkeypatch.setattr(
            "app.services.daily_digest.generate_missing_summaries",
            fake_generate_summaries,
        )

        digest_id = create_daily_digest(
            session=session,
            digest_date=date.today(),
            published_after=published_after,
        )

        assert digest_id is None