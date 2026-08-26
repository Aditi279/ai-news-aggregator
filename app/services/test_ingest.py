from sqlalchemy.orm import Session

from app.db.database import engine
from app.db.repositories import get_all_sources
from app.services.ingest import ingest_feed


with Session(engine) as session:
    sources = get_all_sources(session)

    for source in sources:
        if source.fetch_method in ("rss", "web"):
            new_articles = ingest_feed(
                session=session,
                feed_url=source.url,
                source_name=source.name,
                source_type=source.type,
                fetch_method=source.fetch_method,
            )

            print(
                f"{source.name} → "
                f"New articles inserted: {new_articles}"
            )