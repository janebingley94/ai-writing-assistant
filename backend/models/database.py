import uuid

from sqlalchemy import DateTime, Float, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class GenerationRecord(Base):
    __tablename__ = "generation_records"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    generation_type: Mapped[str] = mapped_column(String(40), index=True)
    content: Mapped[str] = mapped_column(Text)
    word_count: Mapped[int] = mapped_column()
    quality_score: Mapped[float] = mapped_column(Float, nullable=True)
    request_payload: Mapped[dict] = mapped_column(JSONB, default=dict)
    metadata: Mapped[dict] = mapped_column(JSONB, default=dict)
    created_at: Mapped[object] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
