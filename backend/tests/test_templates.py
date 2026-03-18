from models.schemas import BlogGenerateRequest, EmailGenerateRequest, SummaryRequest, SEOArticleRequest
from services.template_service import TemplateService


def test_blog_prompt_contains_outline_instruction():
    req = BlogGenerateRequest(
        topic="AI 应用",
        keywords=["LLM", "产品"],
        tone="professional",
        length="short",
        outline_first=True,
    )
    system = TemplateService.build_blog_system(req)
    prompt = TemplateService.build_blog_prompt(req, outline=None)
    assert "请先生成文章大纲" in prompt
    assert "AI 应用" in prompt
    assert "LLM" in prompt
    assert "professional" in system


def test_email_prompt_placeholders():
    req = EmailGenerateRequest(
        email_type="business",
        recipient_name="李雷",
        sender_name="韩梅梅",
        context="讨论合作",
        tone="formal",
    )
    system, user = TemplateService.build_email_prompt(req)
    assert "商务写作专家" in system
    assert "李雷" in user
    assert "韩梅梅" in user
    assert "JSON" in user


def test_summary_prompt():
    req = SummaryRequest(content="长文本", summary_type="tldr", max_length=120)
    system, user = TemplateService.build_summary_prompt(req)
    assert "总结" in system
    assert "TL;DR" in user


def test_seo_prompt():
    req = SEOArticleRequest(keyword="AI", secondary_keywords=["产品"], include_faq=True)
    system, user = TemplateService.build_seo_prompt(req)
    assert "SEO" in system
    assert "FAQ" in user
