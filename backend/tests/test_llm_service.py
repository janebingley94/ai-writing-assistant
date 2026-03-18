import types

import pytest

from services.llm_service import LLMService


class FakeResponse:
    def __init__(self, text: str):
        self.output_text = text


class FakeStream:
    def __init__(self, chunks: list[str]):
        self._chunks = chunks

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False

    @property
    def text_stream(self):
        async def generator():
            for chunk in self._chunks:
                yield chunk

        return generator()


class FakeResponsesClient:
    def __init__(self):
        self.stream_called = False

    async def create(self, **kwargs):
        if kwargs.get("response_format"):
            return FakeResponse('{"subject":"hi","body":"x","suggested_cta":"y"}')
        return FakeResponse("hello")

    def stream(self, **kwargs):
        self.stream_called = True
        return FakeStream(["a", "b", "c"])


class FakeOpenAI:
    def __init__(self):
        self.responses = FakeResponsesClient()


@pytest.mark.asyncio
async def test_generate_json_parses(monkeypatch):
    monkeypatch.setattr(LLMService, "client", FakeOpenAI())
    data = await LLMService.generate("sys", "user", response_format="json", required_keys=["subject", "body", "suggested_cta"])
    assert data["subject"] == "hi"


@pytest.mark.asyncio
async def test_stream_generate(monkeypatch):
    monkeypatch.setattr(LLMService, "client", FakeOpenAI())
    chunks = []
    async for chunk in LLMService.stream_generate("sys", "user"):
        chunks.append(chunk)
    assert chunks == ["a", "b", "c"]
