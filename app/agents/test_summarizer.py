from app.agents.summarizer import summarize_article


def test_summarize_article(monkeypatch):
    class FakeResponse:
        output_text = "OpenAI released a new AI model. It matters because the model improves AI capabilities."

    class FakeClient:
        class Responses:
            def create(self, model, input):
                return FakeResponse()

        responses = Responses()

    def fake_openai(api_key):
        return FakeClient()

    monkeypatch.setattr(
        "app.agents.summarizer.OpenAI",
        fake_openai,
    )

    result = summarize_article(
        "OpenAI released a new AI model that improves AI capabilities."
    )

    assert result == (
        "OpenAI released a new AI model. "
        "It matters because the model improves AI capabilities."
    )

def test_summarize_article_requires_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    try:
        summarize_article("Test article content.")
        assert False
    except ValueError as error:
        assert str(error) == "OPENAI_API_KEY not found"