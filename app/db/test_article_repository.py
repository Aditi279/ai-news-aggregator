from sqlalchemy.orm import Session

from app.db.database import engine
from app.db.repositories import get_article_by_url


with Session(engine) as session:
    article = get_article_by_url(
        session=session,
       url="https://example.com/article-that-does-not-exist",
    )

    if article:
        print("Article found!")
        print("ID:", article.id)
        print("Title:", article.title)
    else:
        print("Article not found!")