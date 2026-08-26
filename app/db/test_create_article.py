from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.db.database import engine
from app.db.repositories import create_article


with Session(engine) as session:
    article = create_article(
        session=session,
        source_id=1,
        title="Test article for repository",
        url="https://example.com/test-article-repository",
        published_at=datetime.now(timezone.utc),
        summary="This is a test article.",
    )

    print("Article created!")
    print("Article ID:", article.id)
    print("Title:", article.title)