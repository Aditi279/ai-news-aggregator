from datetime import datetime

from sqlalchemy.orm import Session

from app.db.database import engine
from app.db.repositories import get_articles_published_after
from app.agents.digest import generate_digest


cutoff = datetime(2026, 8, 18, 0, 0, 0)


with Session(engine) as session:
    articles = get_articles_published_after(
        session=session,
        published_after=cutoff,
    )

    articles = [
        article
        for article in articles
        if article.ai_summary
    ]

    print(f"Articles going into digest: {len(articles)}")

    digest = generate_digest(articles)

    print("\n===== DAILY AI DIGEST =====\n")
    print(digest)