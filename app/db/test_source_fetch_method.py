from sqlalchemy.orm import Session

from app.db.database import engine
from app.db.repositories import get_all_sources


with Session(engine) as session:
    sources = get_all_sources(session)

    for source in sources:
        print(
            f"{source.name} → "
            f"fetch method: {source.fetch_method}"
        )