from __future__ import annotations

from services.llm_service import LLMService


QUALITY_SYSTEM_PROMPT = "你是一位严格的内容质量评估专家。"
QUALITY_USER_PROMPT = """请对以下内容质量进行评分，范围 1-10 分：

内容：
{content}

请以 JSON 输出：
{{
  "score": 0-10,
  "reason": "评分理由，简短说明"
}}"""


class QualityService:
    @staticmethod
    async def score(content: str) -> float:
        payload = QUALITY_USER_PROMPT.format(content=content)
        result = await LLMService.generate(
            system=QUALITY_SYSTEM_PROMPT,
            user=payload,
            response_format="json",
            required_keys=["score", "reason"],
        )
        score = result.get("score", 0)
        try:
            return float(score)
        except (TypeError, ValueError):
            return 0.0
