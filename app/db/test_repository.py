from sqlalchemy.orm import Session

from app.db.database import engine
from app.db.repositories import get_or_create_source


with Session(engine) as session:
    source = get_or_create_source(
        session=session,
        name="Google AI",
        source_type="blog",
        url="https://blog.google/technology/ai/",
    )

    print("Source ID:", source.id)
    print("Source name:", source.name)