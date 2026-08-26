from datetime import date, datetime

from sqlalchemy.orm import Session

from app.db.database import engine
from app.services.daily_digest import create_daily_digest


digest_date = date(2026, 8, 23)
published_after = datetime(2026, 8, 18, 0, 0, 0)


with Session(engine) as session:
    digest_id = create_daily_digest(
        session=session,
        digest_date=digest_date,
        published_after=published_after,
    )

    print(f"Returned digest ID: {digest_id}")