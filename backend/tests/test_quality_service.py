import pytest

from services.quality_service import QualityService


@pytest.mark.asyncio
async def test_quality_score_parsing(monkeypatch):
    async def fake_generate(*args, **kwargs):
        return {"score": 8, "reason": "ok"}

    monkeypatch.setattr("services.quality_service.LLMService.generate", fake_generate)
    score = await QualityService.score("content")
    assert score == 8.0
