from pydantic import BaseModel



class Article(BaseModel):
    title: str
    url: str
    published: str
    summary: str | None = None