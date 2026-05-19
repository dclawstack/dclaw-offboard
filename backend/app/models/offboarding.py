"""Offboarding domain models — P0 & P1 features."""

import uuid
from datetime import date, datetime
from typing import Optional

from sqlalchemy import Boolean, Date, DateTime, Enum, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.core.utils import utc_now


# ── Enums ────────────────────────────────────────────────────────────────────

import enum


class ChecklistStatus(str, enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"


class TaskStatus(str, enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    blocked = "blocked"


class TaskCategory(str, enum.Enum):
    it = "it"
    hr = "hr"
    finance = "finance"
    manager = "manager"
    legal = "legal"
    facilities = "facilities"


class AssetCondition(str, enum.Enum):
    excellent = "excellent"
    good = "good"
    fair = "fair"
    damaged = "damaged"
    lost = "lost"


class RevocationStatus(str, enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    failed = "failed"


class InterviewStatus(str, enum.Enum):
    scheduled = "scheduled"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"


class SentimentLabel(str, enum.Enum):
    positive = "positive"
    neutral = "neutral"
    negative = "negative"


class RehireEligibility(str, enum.Enum):
    eligible = "eligible"
    conditional = "conditional"
    not_eligible = "not_eligible"
    pending_review = "pending_review"


# ── P0.2: Offboarding Checklist & Workflow ────────────────────────────────────


class OffboardingChecklist(Base):
    __tablename__ = "offboarding_checklists"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    employee_name: Mapped[str] = mapped_column(String(255), nullable=False)
    employee_email: Mapped[str] = mapped_column(String(255), nullable=False)
    employee_role: Mapped[str] = mapped_column(String(255), nullable=False)
    department: Mapped[str] = mapped_column(String(255), nullable=False)
    last_day: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[ChecklistStatus] = mapped_column(
        Enum(ChecklistStatus), default=ChecklistStatus.pending, nullable=False
    )
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, onupdate=utc_now, nullable=False
    )

    tasks: Mapped[list["OffboardingTask"]] = relationship(
        "OffboardingTask", back_populates="checklist", lazy="selectin", cascade="all, delete-orphan"
    )
    assets: Mapped[list["AssetReturn"]] = relationship(
        "AssetReturn", back_populates="checklist", lazy="selectin", cascade="all, delete-orphan"
    )
    revocations: Mapped[list["AccessRevocation"]] = relationship(
        "AccessRevocation", back_populates="checklist", lazy="selectin", cascade="all, delete-orphan"
    )


class OffboardingTask(Base):
    __tablename__ = "offboarding_tasks"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    checklist_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("offboarding_checklists.id", ondelete="CASCADE"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    category: Mapped[TaskCategory] = mapped_column(
        Enum(TaskCategory), nullable=False
    )
    assigned_to: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus), default=TaskStatus.pending, nullable=False
    )
    due_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, onupdate=utc_now, nullable=False
    )

    checklist: Mapped["OffboardingChecklist"] = relationship(
        "OffboardingChecklist", back_populates="tasks"
    )


# ── P0.3: Asset Recovery & Inventory ─────────────────────────────────────────


class Asset(Base):
    __tablename__ = "assets"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    asset_type: Mapped[str] = mapped_column(String(100), nullable=False)  # laptop, phone, key, card, etc.
    serial_number: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    assigned_to: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    assigned_to_email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="assigned", nullable=False)  # assigned, returned, lost
    value: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, onupdate=utc_now, nullable=False
    )


class AssetReturn(Base):
    __tablename__ = "asset_returns"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    checklist_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("offboarding_checklists.id", ondelete="CASCADE"), nullable=False
    )
    asset_name: Mapped[str] = mapped_column(String(255), nullable=False)
    asset_type: Mapped[str] = mapped_column(String(100), nullable=False)
    serial_number: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    condition: Mapped[Optional[AssetCondition]] = mapped_column(
        Enum(AssetCondition), nullable=True
    )
    returned: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    return_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, onupdate=utc_now, nullable=False
    )

    checklist: Mapped["OffboardingChecklist"] = relationship(
        "OffboardingChecklist", back_populates="assets"
    )


# ── P0.4: Access Revocation ──────────────────────────────────────────────────


class AccessRevocation(Base):
    __tablename__ = "access_revocations"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    checklist_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("offboarding_checklists.id", ondelete="CASCADE"), nullable=False
    )
    system_name: Mapped[str] = mapped_column(String(255), nullable=False)  # e.g. Slack, GitHub, VPN
    system_type: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # saas, vpn, email, physical
    status: Mapped[RevocationStatus] = mapped_column(
        Enum(RevocationStatus), default=RevocationStatus.pending, nullable=False
    )
    revoked_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    revoked_by: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, onupdate=utc_now, nullable=False
    )

    checklist: Mapped["OffboardingChecklist"] = relationship(
        "OffboardingChecklist", back_populates="revocations"
    )


# ── P1.5: AI Exit Interview ──────────────────────────────────────────────────


class ExitInterview(Base):
    __tablename__ = "exit_interviews"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    checklist_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("offboarding_checklists.id", ondelete="SET NULL"), nullable=True
    )
    employee_name: Mapped[str] = mapped_column(String(255), nullable=False)
    employee_email: Mapped[str] = mapped_column(String(255), nullable=False)
    scheduled_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    status: Mapped[InterviewStatus] = mapped_column(
        Enum(InterviewStatus), default=InterviewStatus.scheduled, nullable=False
    )
    transcript: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    sentiment_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # -1 to 1
    sentiment_label: Mapped[Optional[SentimentLabel]] = mapped_column(
        Enum(SentimentLabel), nullable=True
    )
    key_themes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON array of themes
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    actionable_insights: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, onupdate=utc_now, nullable=False
    )


# ── P1.6: Knowledge Transfer & Handover ──────────────────────────────────────


class KnowledgeTransfer(Base):
    __tablename__ = "knowledge_transfers"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    checklist_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("offboarding_checklists.id", ondelete="SET NULL"), nullable=True
    )
    employee_name: Mapped[str] = mapped_column(String(255), nullable=False)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    content_type: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # project_docs, contacts, passwords, processes, other
    content: Mapped[str] = mapped_column(Text, nullable=False)
    attachments: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON array of file URLs
    successor_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    successor_email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    validated: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    validated_by: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, onupdate=utc_now, nullable=False
    )


# ── P1.7: Alumni Network ─────────────────────────────────────────────────────


class AlumniRecord(Base):
    __tablename__ = "alumni_records"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    employee_name: Mapped[str] = mapped_column(String(255), nullable=False)
    employee_email: Mapped[str] = mapped_column(String(255), nullable=False)
    personal_email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    last_role: Mapped[str] = mapped_column(String(255), nullable=False)
    department: Mapped[str] = mapped_column(String(255), nullable=False)
    tenure_months: Mapped[int] = mapped_column(Integer, nullable=False)
    last_day: Mapped[date] = mapped_column(Date, nullable=False)
    rehire_eligibility: Mapped[RehireEligibility] = mapped_column(
        Enum(RehireEligibility), default=RehireEligibility.pending_review, nullable=False
    )
    exit_interview_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, onupdate=utc_now, nullable=False
    )


# ── P1.8: Final Pay & Compliance ─────────────────────────────────────────────


class FinalPayCalculation(Base):
    __tablename__ = "final_pay_calculations"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    checklist_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("offboarding_checklists.id", ondelete="SET NULL"), nullable=True
    )
    employee_name: Mapped[str] = mapped_column(String(255), nullable=False)
    employee_email: Mapped[str] = mapped_column(String(255), nullable=False)
    last_day: Mapped[date] = mapped_column(Date, nullable=False)
    base_salary: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    unused_pto_hours: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    pto_payout_rate: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    severance_weeks: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    severance_amount: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    bonus_amount: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    deductions: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    total_final_pay: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    compliance_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, onupdate=utc_now, nullable=False
    )
