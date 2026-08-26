from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.database import engine
from app.db.models import Article


with Session(engine) as session:
    statement = select(Article).where(Article.id == 1)

    article = session.scalars(statement).first()

    print(article.id)
    print(article.title)
    print(article.url)
    print(article.summary)