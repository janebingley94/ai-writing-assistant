from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import PlainTextResponse
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import AsyncSessionLocal
from models.database import GenerationRecord
from models.schemas import GenerationRecordResponse

router = APIRouter(prefix="/history", tags=["history"])


async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


@router.get("", response_model=list[GenerationRecordResponse])
async def list_history(session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(GenerationRecord).order_by(GenerationRecord.created_at.desc())
    )
    return result.scalars().all()


@router.delete("/{record_id}")
async def delete_history(record_id: str, session: AsyncSession = Depends(get_session)):
    await session.execute(delete(GenerationRecord).where(GenerationRecord.id == record_id))
    await session.commit()
    return {"status": "deleted"}


@router.post("/{record_id}/export")
async def export_history(record_id: str, session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(GenerationRecord).where(GenerationRecord.id == record_id)
    )
    record = result.scalar_one_or_none()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    front_matter = (
        "---\n"
        f"id: {record.id}\n"
        f"generation_type: {record.generation_type}\n"
        f"created_at: {record.created_at}\n"
        f"word_count: {record.word_count}\n"
        f"quality_score: {record.quality_score}\n"
        "---\n\n"
    )
    body = f"{record.content}\n"
    return PlainTextResponse(front_matter + body, media_type="text/markdown")
