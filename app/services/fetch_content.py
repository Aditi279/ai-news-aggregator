import logging
from datetime import datetime

import requests
from sqlalchemy.orm import Session

from app.db.repositories import get_articles_without_content_after
from app.fetchers.content import fetch_article_content


logger = logging.getLogger(__name__)


def fetch_missing_content(
    session: Session,
    created_after: datetime,
    limit: int = 10,
) -> int:
    articles = get_articles_without_content_after(
        session=session,
        created_after=created_after,
    )[:limit]

    updated_articles = 0

    for article in articles:
        try:
            content = fetch_article_content(article.url)
            article.content = content
            updated_articles += 1

        except requests.HTTPError as error:
            if (
                error.response is not None
                and error.response.status_code == 404
            ):
                article.content_fetch_failed = True

                logger.warning(
                    "Skipping permanently unavailable article: %s",
                    article.url,
                )
            else:
                logger.error(
                    "Failed to fetch content for %s: %s",
                    article.url,
                    error,
                )

        except Exception as error:
            logger.error(
                "Failed to fetch content for %s: %s",
                article.url,
                error,
            )

    session.commit()

    return updated_articles