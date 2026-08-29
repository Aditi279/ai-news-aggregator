from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.db.models import Base
from app.db.repositories import create_article, get_or_create_source
from tests.conftest import test_engine


def test_create_article():
    Base.metadata.create_all(test_engine)

    with Session(test_engine) as session:
        source = get_or_create_source(
            session=session,
            name="Test Article Source",
            source_type="blog",
            url="https://example.com",
        )

        article = create_article(
            session=session,
            source_id=source.id,
            title="Test article for repository",
            url="https://example.com/test-article-repository",
            published_at=datetime.now(timezone.utc),
            summary="This is a test article.",
            content="This is test article content.",
        )

        assert article.id is not None
        assert article.title == "Test article for repository"