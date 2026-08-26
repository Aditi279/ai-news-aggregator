from sqlalchemy.orm import Session

from app.db.database import engine
from app.db.models import Source


with Session(engine) as session:
    source = Source(
        name="Anthropic",
        type="blog",
        url="https://www.anthropic.com/news",
    )

    session.add(source)
    session.commit()

    print("Source created!")
    print("Source ID:", source.id)