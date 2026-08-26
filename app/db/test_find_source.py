from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.database import engine
from app.db.models import Source


with Session(engine) as session:
    statement = select(Source).where(Source.name == "Anthropic")

    source = session.scalars(statement).first()

    if source:
        print("Source found!")
        print("ID:", source.id)
        print("Name:", source.name)
    else:
        print("Source not found!")