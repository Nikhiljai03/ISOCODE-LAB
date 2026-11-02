import uuid
from datetime import datetime, date
from sqlalchemy import CheckConstraint, Date, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from aranya_api.shared.database import Base


class InventoryHold(Base):
    __tablename__ = "inventory_holds"
    __table_args__ = (
        UniqueConstraint("idempotency_key", name="uq_hold_idempotency_key"),
        CheckConstraint("units > 0", name="ck_hold_units_positive"),
    )
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    idempotency_key: Mapped[str] = mapped_column(String(150), nullable=False)
    guest_email_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    units: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="pending", nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)


class InventoryHoldNight(Base):
    __tablename__ = "inventory_hold_nights"
    __table_args__ = (
        UniqueConstraint("hold_id", "category_id", "stay_date", name="uq_hold_night"),
        CheckConstraint("units > 0", name="ck_hold_night_positive"),
    )
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    hold_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("inventory_holds.id"), nullable=False)
    category_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("accommodation_categories.id"), nullable=False)
    stay_date: Mapped[date] = mapped_column(Date, nullable=False)
    units: Mapped[int] = mapped_column(Integer, nullable=False)
