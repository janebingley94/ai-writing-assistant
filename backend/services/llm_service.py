from __future__ import annotations

from typing import AsyncGenerator, Literal, Optional

from openai import AsyncOpenAI

from core.config import settings
from services.structured_output import StructuredOutputParser


ResponseFormat = Literal["json", "markdown", "text"]


class LLMService:
    client = AsyncOpenAI(
        api_key=settings.openai_api_key,
        base_url=settings.openai_base_url,
    )

    @classmethod
    async def generate(
        cls,
        system: str,
        user: str,
        response_format: ResponseFormat = "text",
        required_keys: Optional[list[str]] = None,
        model: Optional[str] = None,
    ) -> str | dict:
        model_name = model or settings.default_model
        payload: dict = {
            "model": model_name,
            "input": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        }
        if response_format == "json":
            payload["response_format"] = {"type": "json_object"}

        response = await cls.client.responses.create(**payload)
        text = cls._extract_text(response)

        if response_format == "json":
            return StructuredOutputParser.parse_json(text, required_keys=required_keys)
        return text

    @classmethod
    async def stream_generate(
        cls,
        system: str,
        user: str,
        model: Optional[str] = None,
    ) -> AsyncGenerator[str, None]:
        model_name = model or settings.default_model
        async with cls.client.responses.stream(
            model=model_name,
            input=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        ) as stream:
            async for text in stream.text_stream:
                yield text

    @staticmethod
    def _extract_text(response: object) -> str:
        if hasattr(response, "output_text"):
            return getattr(response, "output_text")
        if hasattr(response, "output") and response.output:
            parts = []
            for item in response.output:
                content = getattr(item, "content", None)
                if not content:
                    continue
                for chunk in content:
                    text = getattr(chunk, "text", None)
                    if text:
                        parts.append(text)
            if parts:
                return "".join(parts)
        raise ValueError("No text output from response.")
