from datetime import date, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Article, Digest, Source

def get_or_create_source(
    session: Session,
    name: str,
    source_type: str,
    url: str,
) -> Source:
    statement = select(Source).where(Source.name == name)

    source = session.scalars(statement).first()

    if source:
        return source

    source = Source(
        name=name,
        type=source_type,
        url=url,
    )

    session.add(source)
    session.commit()
    session.refresh(source)

    return source

def get_all_sources(
    session: Session,
) -> list[Source]:
    statement = select(Source)

    sources = session.scalars(statement).all()

    return sources



def get_article_by_url(
    session: Session,
    url: str,
) -> Article | None:
    statement = select(Article).where(Article.url == url)

    article = session.scalars(statement).first()

    return article    

def get_articles_published_after(
    session: Session,
    published_after: datetime,
) -> list[Article]:
    statement = (
        select(Article)
        .where(Article.published_at > published_after)
        .order_by(Article.published_at.desc())
    )

    articles = session.scalars(statement).all()

    return articles

def get_articles_without_content(
    session: Session,
) -> list[Article]:
    statement = (
        select(Article)
        .where(
            Article.content.is_(None),
            Article.content_fetch_failed.is_(False),
        )
    )

    articles = session.scalars(statement).all()

    return articles

def get_articles_without_ai_summary(
    session: Session,
) -> list[Article]:
    statement = select(Article).where(Article.ai_summary.is_(None))

    articles = session.scalars(statement).all()

    return articles

def create_article(
    session: Session,
    source_id: int,
    title: str,
    url: str,
    published_at,
    summary: str | None,
    content: str | None,
) -> Article:
    article = Article(
    source_id=source_id,
    title=title,
    url=url,
    published_at=published_at,
    summary=summary,
    content=content,
    created_at=datetime.now(),
)

    session.add(article)
    session.commit()
    session.refresh(article)

    return article

def update_article_ai_summary(
    session: Session,
    article: Article,
    ai_summary: str,
) -> None:
    article.ai_summary = ai_summary

    session.commit()

def get_articles_without_ai_summary_after(
    session: Session,
    published_after: datetime,
) -> list[Article]:
    statement = (
        select(Article)
        .where(
            Article.published_at > published_after,
            Article.ai_summary.is_(None),
        )
        .order_by(Article.published_at.desc())
    )

    articles = session.scalars(statement).all()

    return articles

def create_digest(
    session: Session,
    digest_date: date,
    content: str,
) -> Digest:
    digest = Digest(
        digest_date=digest_date,
        content=content,
        created_at=datetime.now(),
    )

    session.add(digest)
    session.commit()
    session.refresh(digest)

    return digest

def get_digest_by_date(
    session: Session,
    digest_date: date,
) -> Digest | None:
    statement = (
        select(Digest)
        .where(Digest.digest_date == digest_date)
    )

    digest = session.scalars(statement).first()

    return digest

def get_latest_digest(
    session: Session,
) -> Digest | None:
    statement = (
        select(Digest)
        .order_by(Digest.digest_date.desc())
    )

    digest = session.scalars(statement).first()

    return digest

def get_articles_without_content_after(
    session: Session,
    created_after: datetime,
) -> list[Article]:
    statement = (
        select(Article)
        .where(
            Article.created_at > created_after,
            Article.content.is_(None),
            Article.content_fetch_failed.is_(False),
        )
        .order_by(Article.created_at.asc())
    )

    articles = session.scalars(statement).all()

    return articles