import json
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import AsyncSessionLocal
from models.database import GenerationRecord
from models.schemas import (
    BlogGenerateRequest,
    EmailGenerateRequest,
    GenerationResponse,
    SEOArticleRequest,
    SummaryRequest,
    TemplateResponse,
)
from services.llm_service import LLMService
from services.quality_service import QualityService
from services.structured_output import StructuredOutputError
from services.template_service import TemplateService

router = APIRouter(prefix="/generate", tags=["generate"])


async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


def count_words(text: str) -> int:
    words = [item for item in text.split() if item.strip()]
    if words:
        return len(words)
    return len(text)


async def save_record(
    session: AsyncSession,
    generation_type: str,
    content: str,
    word_count: int,
    quality_score: float | None,
    request_payload: dict,
    metadata: dict,
) -> GenerationRecord:
    record = GenerationRecord(
        generation_type=generation_type,
        content=content,
        word_count=word_count,
        quality_score=quality_score,
        request_payload=request_payload,
        metadata=metadata,
    )
    session.add(record)
    await session.commit()
    await session.refresh(record)
    return record


@router.get("/templates", response_model=TemplateResponse)
async def list_templates():
    return TemplateResponse(
        blog_tones=["professional", "casual", "academic", "creative"],
        blog_lengths=["short", "medium", "long"],
        email_types=["business", "follow_up", "introduction", "complaint", "thank_you"],
        email_tones=["formal", "friendly", "urgent"],
        summary_types=["bullet_points", "paragraph", "tldr", "executive"],
    )


@router.post("/blog", response_model=GenerationResponse)
async def generate_blog(
    request: BlogGenerateRequest,
    session: AsyncSession = Depends(get_session),
):
    outline = None
    if request.outline_first:
        outline_prompt = TemplateService.build_blog_outline_prompt(request)
        try:
            outline = await LLMService.generate(
                system="你是一位擅长构建文章大纲的专业编辑。",
                user=outline_prompt,
                response_format="json",
                required_keys=TemplateService.extract_required_keys("outline"),
            )
        except StructuredOutputError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    system_prompt = TemplateService.build_blog_system(request)
    user_prompt = TemplateService.build_blog_prompt(request, outline)

    content = await LLMService.generate(
        system=system_prompt,
        user=user_prompt,
        response_format="markdown",
    )

    word_count = count_words(content)
    quality_score = await QualityService.score(content)
    metadata = {"outline": outline, "request": request.model_dump()}

    record = await save_record(
        session,
        generation_type="blog",
        content=content,
        word_count=word_count,
        quality_score=quality_score,
        request_payload=request.model_dump(),
        metadata=metadata,
    )

    return GenerationResponse(
        id=record.id,
        content=record.content,
        word_count=record.word_count,
        generation_type="blog",
        metadata=record.metadata,
        created_at=record.created_at,
    )


@router.post("/email", response_model=GenerationResponse)
async def generate_email(
    request: EmailGenerateRequest,
    session: AsyncSession = Depends(get_session),
):
    system_prompt, user_prompt = TemplateService.build_email_prompt(request)
    try:
        email_payload = await LLMService.generate(
            system=system_prompt,
            user=user_prompt,
            response_format="json",
            required_keys=TemplateService.extract_required_keys("email"),
        )
    except StructuredOutputError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    content = json.dumps(email_payload, ensure_ascii=False, indent=2)
    word_count = count_words(email_payload.get("body", content))
    quality_score = await QualityService.score(email_payload.get("body", content))
    metadata = {"structured": email_payload, "request": request.model_dump()}

    record = await save_record(
        session,
        generation_type="email",
        content=content,
        word_count=word_count,
        quality_score=quality_score,
        request_payload=request.model_dump(),
        metadata=metadata,
    )

    return GenerationResponse(
        id=record.id,
        content=record.content,
        word_count=record.word_count,
        generation_type="email",
        metadata=record.metadata,
        created_at=record.created_at,
    )


@router.post("/summary", response_model=GenerationResponse)
async def generate_summary(
    request: SummaryRequest,
    session: AsyncSession = Depends(get_session),
):
    system_prompt, user_prompt = TemplateService.build_summary_prompt(request)
    content = await LLMService.generate(
        system=system_prompt,
        user=user_prompt,
        response_format="markdown",
    )
    word_count = count_words(content)
    quality_score = await QualityService.score(content)
    metadata = {"request": request.model_dump()}

    record = await save_record(
        session,
        generation_type="summary",
        content=content,
        word_count=word_count,
        quality_score=quality_score,
        request_payload=request.model_dump(),
        metadata=metadata,
    )

    return GenerationResponse(
        id=record.id,
        content=record.content,
        word_count=record.word_count,
        generation_type="summary",
        metadata=record.metadata,
        created_at=record.created_at,
    )


@router.post("/seo", response_model=GenerationResponse)
async def generate_seo(
    request: SEOArticleRequest,
    session: AsyncSession = Depends(get_session),
):
    system_prompt, user_prompt = TemplateService.build_seo_prompt(request)
    content = await LLMService.generate(
        system=system_prompt,
        user=user_prompt,
        response_format="markdown",
    )
    word_count = count_words(content)
    quality_score = await QualityService.score(content)
    metadata = {"request": request.model_dump()}

    record = await save_record(
        session,
        generation_type="seo",
        content=content,
        word_count=word_count,
        quality_score=quality_score,
        request_payload=request.model_dump(),
        metadata=metadata,
    )

    return GenerationResponse(
        id=record.id,
        content=record.content,
        word_count=record.word_count,
        generation_type="seo",
        metadata=record.metadata,
        created_at=record.created_at,
    )


@router.post("/stream/{generation_type}")
async def generate_stream(
    generation_type: str,
    payload: dict = Body(...),
):
    if generation_type not in {"blog", "email", "summary", "seo"}:
        raise HTTPException(status_code=400, detail="Unsupported generation type")

    system_prompt = ""
    user_prompt = ""

    if generation_type == "blog":
        request = BlogGenerateRequest(**payload)
        system_prompt = TemplateService.build_blog_system(request)
        user_prompt = TemplateService.build_blog_prompt(request, outline=None)
    elif generation_type == "email":
        request = EmailGenerateRequest(**payload)
        system_prompt, user_prompt = TemplateService.build_email_prompt(request)
    elif generation_type == "summary":
        request = SummaryRequest(**payload)
        system_prompt, user_prompt = TemplateService.build_summary_prompt(request)
    elif generation_type == "seo":
        request = SEOArticleRequest(**payload)
        system_prompt, user_prompt = TemplateService.build_seo_prompt(request)

    async def event_stream():
        async for chunk in LLMService.stream_generate(system_prompt, user_prompt):
            yield f"data: {chunk}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
