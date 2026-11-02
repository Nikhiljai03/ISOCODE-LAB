import uuid
from datetime import datetime
from sqlalchemy import Boolean, DateTime, ForeignKey, Float, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column
from aranya_api.shared.database import Base


class Enquiry(Base):
    __tablename__ = "enquiries"
    __table_args__ = (UniqueConstraint("source", "external_id", name="uq_enquiry_source_external"),)
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source: Mapped[str] = mapped_column(String(30), nullable=False)
    external_id: Mapped[str] = mapped_column(String(150), nullable=False)
    sender_name: Mapped[str] = mapped_column(String(150), nullable=False)
    sender_contact: Mapped[str] = mapped_column(String(200), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="AI_PENDING", nullable=False)
    category: Mapped[str | None] = mapped_column(String(30), nullable=True)
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    extracted: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)


class EnquiryDraft(Base):
    __tablename__ = "enquiry_drafts"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    enquiry_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("enquiries.id"), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="draft", nullable=False)


class EnquiryAlert(Base):
    __tablename__ = "enquiry_alerts"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    enquiry_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("enquiries.id"), unique=True, nullable=False)
    alert_type: Mapped[str] = mapped_column(String(30), default="GM_COMPLAINT", nullable=False)
    acknowledged: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
