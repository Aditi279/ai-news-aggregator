from sqlalchemy.orm import Session

from app.db.database import engine
from app.services.fetch_content import fetch_missing_content


with Session(engine) as session:
    updated_articles = fetch_missing_content(session)

    print(
        f"Articles with content fetched: {updated_articles}"
    )