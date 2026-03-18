from __future__ import annotations

from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


ToneBlog = Literal["professional", "casual", "academic", "creative"]
LengthBlog = Literal["short", "medium", "long"]
EmailType = Literal["business", "follow_up", "introduction", "complaint", "thank_you"]
EmailTone = Literal["formal", "friendly", "urgent"]
SummaryType = Literal["bullet_points", "paragraph", "tldr", "executive"]


class BlogGenerateRequest(BaseModel):
    topic: str
    keywords: list[str] = Field(default_factory=list)
    tone: ToneBlog = "professional"
    length: LengthBlog = "medium"
    language: str = "zh"
    outline_first: bool = True


class EmailGenerateRequest(BaseModel):
    email_type: EmailType
    recipient_name: Optional[str] = None
    sender_name: Optional[str] = None
    context: str
    tone: EmailTone = "formal"
    language: str = "zh"


class SummaryRequest(BaseModel):
    content: str
    summary_type: SummaryType = "paragraph"
    max_length: int = 300
    language: str = "zh"


class SEOArticleRequest(BaseModel):
    keyword: str
    secondary_keywords: list[str] = Field(default_factory=list)
    word_count: int = 1500
    target_audience: str = "general"
    include_faq: bool = True
    language: str = "zh"


class GenerationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    content: str
    word_count: int
    generation_type: str
    metadata: dict
    created_at: datetime
