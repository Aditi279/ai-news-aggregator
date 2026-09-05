import logging
from datetime import datetime

from sqlalchemy.orm import Session

from app.agents.summarizer import summarize_article
from app.db.repositories import (
    get_articles_without_ai_summary_after,
    update_article_ai_summary,
)


logger = logging.getLogger(__name__)


def generate_missing_summaries(
    session: Session,
    published_after: datetime,
    limit: int = 10,
) -> int:
    articles = get_articles_without_ai_summary_after(
        session=session,
        published_after=published_after,
    )[:limit]

    updated_articles = 0

    for article in articles:
        try:
            ai_summary = summarize_article(article.content)

            update_article_ai_summary(
                session=session,
                article=article,
                ai_summary=ai_summary,
            )

            updated_articles += 1

        except Exception as error:
            logger.error(
                "Failed to summarize %s: %s",
                article.url,
                error,
            )

    return updated_articles