import logging
from datetime import date, datetime

from sqlalchemy.orm import Session

from app.agents.digest import generate_digest
from app.db.repositories import (
    create_digest,
    get_articles_published_after,
    get_digest_by_date,
)
from app.services.generate_summary import generate_missing_summaries


logger = logging.getLogger(__name__)


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
        logger.info(
            "Digest already exists for %s",
            digest_date,
        )
        return None

    articles = get_articles_published_after(
        session=session,
        published_after=published_after,
    )

    if not articles:
        logger.info("No new articles found")
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
        logger.info("No summarized articles available")
        return None

    digest_content = generate_digest(articles)

    digest = create_digest(
        session=session,
        digest_date=digest_date,
        content=digest_content,
    )

    logger.info(
        "Digest created with ID: %s",
        digest.id,
    )

    return digest.id