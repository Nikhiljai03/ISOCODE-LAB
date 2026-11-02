"""Initial ARANYA domain

Revision ID: 0001_initial_domain
Revises:
Create Date: 2026-11-02
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0001_initial_domain"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto")
    op.create_table("accommodation_categories",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("code", sa.String(50), nullable=False), sa.Column("name", sa.String(150), nullable=False),
        sa.Column("physical_inventory_count", sa.Integer(), nullable=False), sa.Column("active", sa.Boolean(), server_default="true", nullable=False),
        sa.CheckConstraint("physical_inventory_count >= 0", name="ck_category_inventory_nonnegative"),
        sa.PrimaryKeyConstraint("id"), sa.UniqueConstraint("code"))
    op.create_table("inventory_nights",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("category_id", postgresql.UUID(as_uuid=True), nullable=False), sa.Column("inventory_date", sa.Date(), nullable=False),
        sa.Column("physical_total", sa.Integer(), nullable=False), sa.Column("out_of_service", sa.Integer(), server_default="0", nullable=False),
        sa.Column("reserved_by_other_channels", sa.Integer(), server_default="0", nullable=False),
        sa.CheckConstraint("physical_total >= 0", name="ck_inventory_physical_nonnegative"),
        sa.CheckConstraint("out_of_service >= 0", name="ck_inventory_oos_nonnegative"),
        sa.CheckConstraint("reserved_by_other_channels >= 0", name="ck_inventory_other_nonnegative"),
        sa.CheckConstraint("out_of_service + reserved_by_other_channels <= physical_total", name="ck_inventory_counts"),
        sa.ForeignKeyConstraint(["category_id"], ["accommodation_categories.id"]), sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("category_id", "inventory_date", name="uq_inventory_category_date"))
    op.create_table("website_allotment_nights",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("category_id", postgresql.UUID(as_uuid=True), nullable=False), sa.Column("allotment_date", sa.Date(), nullable=False),
        sa.Column("website_units", sa.Integer(), nullable=False), sa.Column("version", sa.Integer(), server_default="1", nullable=False),
        sa.CheckConstraint("website_units >= 0", name="ck_allotment_nonnegative"),
        sa.ForeignKeyConstraint(["category_id"], ["accommodation_categories.id"]), sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("category_id", "allotment_date", name="uq_allotment_category_date"))
    op.create_table("daily_rates",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("category_id", postgresql.UUID(as_uuid=True), nullable=False), sa.Column("rate_date", sa.Date(), nullable=False),
        sa.Column("base_amount", sa.Numeric(12, 2), nullable=False), sa.Column("currency", sa.String(3), server_default="INR", nullable=False),
        sa.CheckConstraint("base_amount >= 0", name="ck_rate_nonnegative"),
        sa.ForeignKeyConstraint(["category_id"], ["accommodation_categories.id"]), sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("category_id", "rate_date", name="uq_rate_category_date"))
    op.create_table("blackout_dates",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("category_id", postgresql.UUID(as_uuid=True), nullable=False), sa.Column("blackout_date", sa.Date(), nullable=False),
        sa.ForeignKeyConstraint(["category_id"], ["accommodation_categories.id"]), sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("category_id", "blackout_date", name="uq_blackout_category_date"))
    op.create_table("inventory_holds",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("idempotency_key", sa.String(150), nullable=False), sa.Column("guest_email_hash", sa.String(64), nullable=False),
        sa.Column("units", sa.Integer(), nullable=False), sa.Column("status", sa.String(30), server_default="pending", nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("units > 0", name="ck_hold_units_positive"), sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("idempotency_key", name="uq_hold_idempotency_key"))
    op.create_table("inventory_hold_nights",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("hold_id", postgresql.UUID(as_uuid=True), nullable=False), sa.Column("category_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("stay_date", sa.Date(), nullable=False), sa.Column("units", sa.Integer(), nullable=False),
        sa.CheckConstraint("units > 0", name="ck_hold_night_positive"),
        sa.ForeignKeyConstraint(["hold_id"], ["inventory_holds.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["category_id"], ["accommodation_categories.id"]), sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("hold_id", "category_id", "stay_date", name="uq_hold_night"))
    op.create_table("bookings",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("public_reference", sa.String(24), nullable=False), sa.Column("guest_email_hash", sa.String(64), nullable=False),
        sa.Column("guest_name", sa.String(150), nullable=False), sa.Column("guest_phone_hash", sa.String(64), nullable=False),
        sa.Column("state", sa.String(30), server_default="DRAFT", nullable=False), sa.Column("arrival", sa.Date(), nullable=False),
        sa.Column("departure", sa.Date(), nullable=False), sa.Column("subtotal", sa.Numeric(12, 2), nullable=False),
        sa.Column("tax_total", sa.Numeric(12, 2), nullable=False), sa.Column("total_amount", sa.Numeric(12, 2), nullable=False),
        sa.Column("currency", sa.String(3), server_default="INR", nullable=False), sa.Column("hold_id", postgresql.UUID(as_uuid=True)),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("subtotal >= 0", name="ck_booking_subtotal_nonnegative"),
        sa.CheckConstraint("tax_total >= 0", name="ck_booking_tax_nonnegative"),
        sa.CheckConstraint("total_amount >= 0", name="ck_booking_total_nonnegative"),
        sa.ForeignKeyConstraint(["hold_id"], ["inventory_holds.id"]), sa.PrimaryKeyConstraint("id"), sa.UniqueConstraint("public_reference"))
    op.create_table("booking_nights",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("booking_id", postgresql.UUID(as_uuid=True), nullable=False), sa.Column("category_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("stay_date", sa.Date(), nullable=False), sa.Column("units", sa.Integer(), nullable=False),
        sa.Column("base_amount", sa.Numeric(12, 2), nullable=False), sa.Column("tax_amount", sa.Numeric(12, 2), nullable=False),
        sa.Column("total_amount", sa.Numeric(12, 2), nullable=False),
        sa.CheckConstraint("units > 0", name="ck_booking_night_positive"),
        sa.CheckConstraint("base_amount >= 0 AND tax_amount >= 0 AND total_amount >= 0", name="ck_booking_night_money_nonnegative"),
        sa.ForeignKeyConstraint(["booking_id"], ["bookings.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["category_id"], ["accommodation_categories.id"]), sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("booking_id", "category_id", "stay_date", name="uq_booking_night"))
    op.create_table("payments",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("booking_id", postgresql.UUID(as_uuid=True), nullable=False), sa.Column("provider", sa.String(50), nullable=False),
        sa.Column("provider_payment_id", sa.String(150), nullable=False), sa.Column("provider_event_id", sa.String(150), nullable=False),
        sa.Column("state", sa.String(30), server_default="INITIATED", nullable=False), sa.Column("amount", sa.Numeric(12, 2), nullable=False),
        sa.Column("currency", sa.String(3), nullable=False), sa.CheckConstraint("amount >= 0", name="ck_payment_amount_nonnegative"),
        sa.ForeignKeyConstraint(["booking_id"], ["bookings.id"]), sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("provider", "provider_payment_id", name="uq_provider_payment"), sa.UniqueConstraint("provider_event_id", name="uq_provider_event"))
    op.create_table("enquiries",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("source", sa.String(30), nullable=False), sa.Column("external_id", sa.String(150), nullable=False),
        sa.Column("sender_name", sa.String(150), nullable=False), sa.Column("sender_contact", sa.String(200), nullable=False),
        sa.Column("message", sa.Text(), nullable=False), sa.Column("status", sa.String(30), server_default="AI_PENDING", nullable=False),
        sa.Column("category", sa.String(30)), sa.Column("confidence", sa.Float()), sa.Column("extracted", postgresql.JSONB()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("source", "external_id", name="uq_enquiry_source_external"))
    op.create_table("enquiry_drafts",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("enquiry_id", postgresql.UUID(as_uuid=True), nullable=False), sa.Column("content", sa.Text(), nullable=False),
        sa.Column("status", sa.String(30), server_default="draft", nullable=False), sa.ForeignKeyConstraint(["enquiry_id"], ["enquiries.id"]),
        sa.PrimaryKeyConstraint("id"))
    op.create_table("enquiry_alerts",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("enquiry_id", postgresql.UUID(as_uuid=True), nullable=False), sa.Column("alert_type", sa.String(30), server_default="GM_COMPLAINT", nullable=False),
        sa.Column("acknowledged", sa.Boolean(), server_default="false", nullable=False), sa.ForeignKeyConstraint(["enquiry_id"], ["enquiries.id"]),
        sa.PrimaryKeyConstraint("id"), sa.UniqueConstraint("enquiry_id"))


def downgrade() -> None:
    for table in ("enquiry_alerts", "enquiry_drafts", "enquiries", "payments", "booking_nights", "bookings", "inventory_hold_nights", "inventory_holds", "blackout_dates", "daily_rates", "website_allotment_nights", "inventory_nights", "accommodation_categories"):
        op.drop_table(table)
