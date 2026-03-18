from __future__ import annotations

from typing import Any, Tuple

from models.schemas import (
    BlogGenerateRequest,
    EmailGenerateRequest,
    SEOArticleRequest,
    SummaryRequest,
)
from prompts.blog_prompts import BLOG_OUTLINE_PROMPT, BLOG_SYSTEM_PROMPT, BLOG_USER_PROMPT
from prompts.email_prompts import EMAIL_TEMPLATES
from prompts.seo_prompts import SEO_SYSTEM_PROMPT, SEO_USER_PROMPT
from prompts.summary_prompts import SUMMARY_STYLE_MAP, SUMMARY_SYSTEM_PROMPT, SUMMARY_USER_PROMPT


class TemplateService:
    BLOG_LENGTH_MAP = {
        "short": ("短篇", 500),
        "medium": ("中等长度", 1000),
        "long": ("长篇", 2000),
    }

    @staticmethod
    def _format_keywords(keywords: list[str]) -> str:
        return "、".join(keywords) if keywords else "无"

    @classmethod
    def build_blog_system(cls, request: BlogGenerateRequest) -> str:
        return BLOG_SYSTEM_PROMPT.format(tone=request.tone)

    @classmethod
    def build_blog_outline_prompt(cls, request: BlogGenerateRequest) -> str:
        return BLOG_OUTLINE_PROMPT.format(
            topic=request.topic,
            keywords=cls._format_keywords(request.keywords),
        )

    @classmethod
    def build_blog_prompt(
        cls, request: BlogGenerateRequest, outline: dict | None
    ) -> str:
        length_desc, word_count = cls.BLOG_LENGTH_MAP[request.length]
        outline_instruction = (
            "请先生成文章大纲，然后再写完整文章。大纲用 <outline> 标签包裹。"
            if request.outline_first
            else ""
        )
        outline_block = f"\n\n参考大纲：\n{outline}" if outline else ""
        return (
            BLOG_USER_PROMPT.format(
                length_desc=length_desc,
                topic=request.topic,
                keywords=cls._format_keywords(request.keywords),
                tone=request.tone,
                word_count=word_count,
                outline_instruction=outline_instruction,
            )
            + outline_block
        )

    @classmethod
    def build_email_prompt(cls, request: EmailGenerateRequest) -> Tuple[str, str]:
        template = EMAIL_TEMPLATES[request.email_type]
        system = template["system"]
        user = template["user"].format(
            tone=request.tone,
            email_type=request.email_type,
            recipient_name=request.recipient_name or "对方",
            sender_name=request.sender_name or "我",
            context=request.context,
        )
        return system, user

    @classmethod
    def build_summary_prompt(cls, request: SummaryRequest) -> Tuple[str, str]:
        summary_style = SUMMARY_STYLE_MAP[request.summary_type]
        user = SUMMARY_USER_PROMPT.format(
            content=request.content,
            summary_type=request.summary_type,
            max_length=request.max_length,
            language=request.language,
            summary_style=summary_style,
        )
        return SUMMARY_SYSTEM_PROMPT, user

    @classmethod
    def build_seo_prompt(cls, request: SEOArticleRequest) -> Tuple[str, str]:
        faq_instruction = "请在文章末尾添加 FAQ 小节。" if request.include_faq else ""
        user = SEO_USER_PROMPT.format(
            keyword=request.keyword,
            secondary_keywords=cls._format_keywords(request.secondary_keywords),
            target_audience=request.target_audience,
            word_count=request.word_count,
            language=request.language,
            faq_instruction=faq_instruction,
        )
        return SEO_SYSTEM_PROMPT, user

    @staticmethod
    def extract_required_keys(prompt_type: str) -> list[str]:
        if prompt_type == "email":
            return ["subject", "body", "suggested_cta"]
        if prompt_type == "outline":
            return ["title", "sections"]
        return []
