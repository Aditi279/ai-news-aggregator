from datetime import date

from sqlalchemy.orm import Session

from app.db.database import engine
from app.db.repositories import get_digest_by_date


with Session(engine) as session:
    digest = get_digest_by_date(
        session=session,
        digest_date=date(2026, 8, 19),
    )

    if digest:
        print(f"Digest found: {digest.id}")
    else:
        print("Digest not found")