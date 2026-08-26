import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


def generate_digest(articles: list) -> str:
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OPENAI_API_KEY not found")

    client = OpenAI(api_key=api_key)

    article_text = "\n\n".join(
        f"""
Title: {article.title}
Source: {article.url}
Summary: {article.ai_summary}
"""
        for article in articles
    )

    response = client.responses.create(
        model="gpt-5-mini",
        input=f"""
Create a concise daily AI news digest from the articles below.

Instructions:
- Rank the articles by importance.
- Include the most important developments first.
- Give each article a 1-2 sentence summary.
- Include the source URL for every article.
- Do not invent information.
- Avoid repeating the same information.
- End with 2-3 key themes from today's news.

Articles:

{article_text}
""",
    )

    return response.output_text