from sqlalchemy.orm import Session

from app.db.database import engine
from app.db.repositories import get_all_sources
from app.fetchers.rss import fetch_feed
from app.fetchers.anthropic import fetch_anthropic


with Session(engine) as session:
    sources = get_all_sources(session)

    for source in sources:
        if source.fetch_method == "rss":
            articles = fetch_feed(source.url)
            print(f"{source.name} → Fetched {len(articles)} articles")
        elif source.fetch_method == "web":
            if source.name == "Anthropic":
                articles = fetch_anthropic(source.url)
                print(f"{source.name} → Fetched {len(articles)} articles")
            else:
                print(f"{source.name} → Web fetcher not built yet")