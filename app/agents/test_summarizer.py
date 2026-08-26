from sqlalchemy.orm import Session

from app.db.database import engine
from app.db.repositories import get_articles_published_after
from app.agents.summarizer import summarize_article

from datetime import datetime


cutoff = datetime(2026, 8, 18, 0, 0, 0)

with Session(engine) as session:
    articles = get_articles_published_after(
        session=session,
        published_after=cutoff,
    )

    article = articles[0]

    print("Title:")
    print(article.title)

    print("\nSummary:")
    print(summarize_article(article.content))