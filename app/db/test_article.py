from datetime import datetime

from sqlalchemy.orm import Session

from app.db.database import engine
from app.db.models import Article


with Session(engine) as session:
    article = Article(
        source_id=1,
        title="Responding to the next frontier of critical cyber capabilities",
        url="https://openai.com/index/responding-next-frontier-critical-cyber-capabilities",
        published_at=datetime(2026, 8, 7, 15, 20),
        summary="OpenAI is sharing preliminary cybersecurity evaluations for Astra and the steps we’re taking to strengthen safeguards and security controls.",
        created_at=datetime.now(),
    )

    session.add(article)
    session.commit()

    print("Article inserted!")
    print("Article ID:", article.id)