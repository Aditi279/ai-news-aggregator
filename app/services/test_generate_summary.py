from datetime import datetime

from sqlalchemy.orm import Session

from app.db.database import engine
from app.services.generate_summary import generate_missing_summaries


cutoff = datetime(2026, 8, 18, 0, 0, 0)


with Session(engine) as session:
    updated_articles = generate_missing_summaries(
        session=session,
        published_after=cutoff,
        limit=10,
    )

    print(
        f"AI summaries generated: {updated_articles}"
    )