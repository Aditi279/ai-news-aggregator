import os

from sqlalchemy import create_engine


TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql+psycopg://ai_news:ai_news_password@localhost:5432/ai_news_test",
)

test_engine = create_engine(TEST_DATABASE_URL)