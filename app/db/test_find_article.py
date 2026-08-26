from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.database import engine
from app.db.models import Article


with Session(engine) as session:
    statement = select(Article).where(
        Article.url
        == "https://openai.com/index/responding-next-frontier-critical-cyber-capabilities"
    )

    article = session.scalars(statement).first()

    if article:
        print("Article found!")
        print("ID:", article.id)
        print("Title:", article.title)
    else:
        print("Article not found!")