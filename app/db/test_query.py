from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.database import engine
from app.db.models import Source


with Session(engine) as session:
    statement = select(Source).where(Source.name == "OpenAI")

    source = session.scalars(statement).first()

    print(source.id)
print(source.name)
print(source.type)
print(source.url)   