from app.db.database import engine
from app.db.models import Source
from sqlalchemy.orm import Session


with Session(engine) as session:
    source = Source(
        name="OpenAI",
        type="blog",
        url="https://openai.com/news/rss.xml",
    )

    session.add(source)
    session.commit()

    print("Source inserted!")
    print("Source ID:", source.id)