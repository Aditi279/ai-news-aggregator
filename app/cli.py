import logging
from datetime import date, datetime

from sqlalchemy.orm import Session

from app.db.database import engine
from app.db.repositories import get_all_sources, get_latest_digest
from app.services.daily_digest import create_daily_digest
from app.services.fetch_content import fetch_missing_content
from app.services.ingest import ingest_feed


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


def run_ingestion(session: Session) -> int:
    total_new_articles = 0

    sources = get_all_sources(session)

    for source in sources:
        try:
            new_articles = ingest_feed(
                session=session,
                feed_url=source.url,
                source_name=source.name,
                source_type=source.type,
                fetch_method=source.fetch_method,
            )
        except Exception as error:
            logger.error(
                "%s → Ingestion failed: %s",
                source.name,
                error,
            )
            continue

        logger.info(
            "%s → New articles inserted: %s",
            source.name,
            new_articles,
        )
        total_new_articles += new_articles

    return total_new_articles


def run_content_fetching(
    session: Session,
    created_after: datetime,
) -> int:
    total_fetched = 0

    while True:
        fetched = fetch_missing_content(
            session=session,
            created_after=created_after,
            limit=10,
        )

        total_fetched += fetched

        if fetched == 0:
            break

    return total_fetched


def run_daily_digest():
    digest_date = date.today()

    with Session(engine) as session:
        latest_digest = get_latest_digest(session)

        if latest_digest and latest_digest.digest_date == digest_date:
            logger.info(
                "Digest already exists for %s",
                digest_date,
            )
            return

        if latest_digest:
            published_after = datetime.combine(
                latest_digest.digest_date,
                datetime.min.time(),
            )
        else:
            published_after = datetime.min

        ingestion_started_at = datetime.now()

        logger.info("Starting article ingestion...")

        new_articles = run_ingestion(session)

        logger.info(
            "Total new articles: %s",
            new_articles,
        )

        logger.info("Fetching article content...")

        content_fetched = run_content_fetching(
            session=session,
            created_after=ingestion_started_at,
        )

        logger.info(
            "Total article contents fetched: %s",
            content_fetched,
        )

        logger.info("Generating daily digest...")

        create_daily_digest(
            session=session,
            digest_date=digest_date,
            published_after=published_after,
        )


if __name__ == "__main__":
    run_daily_digest()