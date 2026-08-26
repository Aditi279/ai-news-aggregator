import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


def summarize_article(content: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OPENAI_API_KEY not found")

    client = OpenAI(api_key=api_key)

    response = client.responses.create(
        model="gpt-5-mini",
        input=f"""
Summarize the following AI news article in 2-3 concise sentences.

Focus on:
- What happened
- Why it matters

Do not add information that is not present in the article.

Article:
{content}
""",
    )

    return response.output_text