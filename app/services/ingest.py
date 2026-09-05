import logging
from datetime import datetime
from email.utils import parsedate_to_datetime

from sqlalchemy.orm import Session

from app.db.repositories import (
    create_article,
    get_article_by_url,
    get_or_create_source,
)
from app.fetchers.router import fetch_articles


logger = logging.getLogger(__name__)


def parse_published_date(value):
    try:
        return parsedate_to_datetime(value)
    except (TypeError, ValueError):
        return datetime.strptime(value, "%b %d, %Y")


def ingest_feed(
    session: Session,
    feed_url: str,
    source_name: str,
    source_type: str,
    fetch_method: str,
) -> int:
    articles = fetch_articles(feed_url, fetch_method)

    logger.info(
        "%s → Fetched %s articles",
        source_name,
        len(articles),
    )

    source = get_or_create_source(
        session=session,
        name=source_name,
        source_type=source_type,
        url=feed_url,
        fetch_method=fetch_method,
    )

    new_articles = 0

    for article in articles:
        existing_article = get_article_by_url(
            session=session,
            url=article.url,
        )

        if existing_article:
            continue

        create_article(
            session=session,
            source_id=source.id,
            title=article.title,
            url=article.url,
            published_at=parse_published_date(article.published),
            summary=article.summary,
            content=None,
        )

        new_articles += 1

    return new_articles