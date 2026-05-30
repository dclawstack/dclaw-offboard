"""New industry features — v1.3 models.

Risk Assessment, Integration Hub, Team Transition, Compliance, Sentiment Early Warning.
"""

import uuid
from datetime import date, datetime
from typing import Optional

from sqlalchemy import Boolean, Date, DateTime, Enum, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.core.utils import utc_now
import enum


# ── Enums ────────────────────────────────────────────────────────────────────

class RiskLevel(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class IntegrationStatus(str, enum.Enum):
    connected = "connected"
    disconnected = "disconnected"
    error = "error"
    pending = "pending"


class IntegrationCategory(str, enum.Enum):
    hris = "hris"
    sso = "sso"
    payroll = "payroll"
    mdm = "mdm"
    communication = "communication"
    other = "other"


class CoverageStatus(str, enum.Enum):
    assigned = "assigned"
    pending = "pending"
    completed = "completed"
    expired = "expired"


class ComplianceFramework(str, enum.Enum):
    eeoc = "eeoc"
    osha = "osha"
    gdpr = "gdpr"
    ccpa = "ccpa"
    soc2 = "soc2"
    sox = "sox"
    hipaa = "hipaa"


class ReportStatus(str, enum.Enum):
    draft = "draft"
    generated = "generated"
    validated = "validated"
    submitted = "submitted"


class SentimentCategory(str, enum.Enum):
    engagement = "engagement"
    burnout = "burnout"
    satisfaction = "satisfaction"
    culture = "culture"
    management = "management"
    growth = "growth"
    compensation = "compensation"


class FlightRisk(str, enum.Enum):
    low = "low"
    moderate = "moderate"
    high = "high"
    critical = "critical"


# ── Risk Assessment & IP Protection ──────────────────────────────────────────


class RiskAssessment(Base):
    """AI-driven risk assessment for departing employees — data exfiltration, IP theft detection."""

    __tablename__ = "risk_assessments"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    employee_name: Mapped[str] = mapped_column(String(255), nullable=False)
    employee_email: Mapped[str] = mapped_column(String(255), nullable=False)
    department: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(255), nullable=False)
    last_day: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    risk_level: Mapped[RiskLevel] = mapped_column(
        Enum(RiskLevel), default=RiskLevel.low, nullable=False
    )
    risk_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)  # 0-100
    # Anomaly metrics
    unusual_file_access: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    large_downloads: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    email_forwarding_detected: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    usb_activity_detected: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    after_hours_activity: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    # Results
    anomalies: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON array of findings
    evidence_preserved: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    evidence_location: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    recommendations: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON array
    monitoring_start: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    monitoring_end: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    assessed_by: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, onupdate=utc_now, nullable=False
    )


# ── Integration Hub ──────────────────────────────────────────────────────────


class Integration(Base):
    """API-first integration connector for HRIS, SSO, Payroll, MDM, Communication tools."""

    __tablename__ = "integrations"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    provider: Mapped[str] = mapped_column(String(255), nullable=False)  # okta, workday, adp, etc.
    category: Mapped[IntegrationCategory] = mapped_column(
        Enum(IntegrationCategory), nullable=False
    )
    status: Mapped[IntegrationStatus] = mapped_column(
        Enum(IntegrationStatus), default=IntegrationStatus.pending, nullable=False
    )
    api_endpoint: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    auth_type: Mapped[str] = mapped_column(String(50), default="oauth2", nullable=False)  # oauth2, api_key, saml
    credentials_ref: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)  # K8s secret ref
    webhook_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    last_sync_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    sync_status: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # success, partial, failed
    enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    config: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    metadata_info: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, onupdate=utc_now, nullable=False
    )


class IntegrationAction(Base):
    """Audit log of actions performed through integrations."""

    __tablename__ = "integration_actions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    integration_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("integrations.id", ondelete="CASCADE"), nullable=False
    )
    action_type: Mapped[str] = mapped_column(String(100), nullable=False)  # revoke, sync, import, export
    target: Mapped[str] = mapped_column(String(255), nullable=False)  # employee email / system name
    status: Mapped[str] = mapped_column(String(50), default="pending", nullable=False)  # pending, success, failed
    result_detail: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    executed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    duration_ms: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, nullable=False)

    integration: Mapped["Integration"] = relationship("Integration", lazy="selectin")


# ── Team Transition & Coverage ───────────────────────────────────────────────


class TeamTransition(Base):
    """Manages seamless team transitions when an employee departs."""

    __tablename__ = "team_transitions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    departing_employee_name: Mapped[str] = mapped_column(String(255), nullable=False)
    departing_employee_email: Mapped[str] = mapped_column(String(255), nullable=False)
    department: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(255), nullable=False)
    last_day: Mapped[date] = mapped_column(Date, nullable=False)
    successor_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    successor_email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="pending", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, onupdate=utc_now, nullable=False
    )

    coverage_items: Mapped[list["CoverageItem"]] = relationship(
        "CoverageItem", back_populates="transition", lazy="selectin", cascade="all, delete-orphan"
    )


class CoverageItem(Base):
    """Individual coverage assignment during team transition."""

    __tablename__ = "coverage_items"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    transition_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("team_transitions.id", ondelete="CASCADE"), nullable=False
    )
    responsibility: Mapped[str] = mapped_column(String(500), nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)  # direct_reports, projects, meetings, clients, tools, other
    assigned_to_name: Mapped[str] = mapped_column(String(255), nullable=False)
    assigned_to_email: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[CoverageStatus] = mapped_column(
        Enum(CoverageStatus), default=CoverageStatus.pending, nullable=False
    )
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    is_permanent: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, onupdate=utc_now, nullable=False
    )

    transition: Mapped["TeamTransition"] = relationship("TeamTransition", back_populates="coverage_items")


# ── Compliance Automation ────────────────────────────────────────────────────


class ComplianceReport(Base):
    """Automated compliance report generation for offboarding events."""

    __tablename__ = "compliance_reports"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    framework: Mapped[ComplianceFramework] = mapped_column(
        Enum(ComplianceFramework), nullable=False
    )
    employee_name: Mapped[str] = mapped_column(String(255), nullable=False)
    employee_email: Mapped[str] = mapped_column(String(255), nullable=False)
    department: Mapped[str] = mapped_column(String(255), nullable=False)
    last_day: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[ReportStatus] = mapped_column(
        Enum(ReportStatus), default=ReportStatus.draft, nullable=False
    )
    report_data: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    ai_validated: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    validation_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    submitted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    retention_deadline: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    retention_completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, onupdate=utc_now, nullable=False
    )


class NonCompeteTracker(Base):
    """Track non-compete and NDA expiration for departed employees."""

    __tablename__ = "non_compete_trackers"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    employee_name: Mapped[str] = mapped_column(String(255), nullable=False)
    employee_email: Mapped[str] = mapped_column(String(255), nullable=False)
    agreement_type: Mapped[str] = mapped_column(String(100), nullable=False)  # non_compete, nda, non_solicit
    effective_date: Mapped[date] = mapped_column(Date, nullable=False)
    expiration_date: Mapped[date] = mapped_column(Date, nullable=False)
    restrictions_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    last_reviewed: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, onupdate=utc_now, nullable=False
    )


# ── Employee Sentiment & Early Warning ───────────────────────────────────────


class SentimentPulse(Base):
    """Anonymous pulse surveys for employee sentiment tracking."""

    __tablename__ = "sentiment_pulses"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[SentimentCategory] = mapped_column(
        Enum(SentimentCategory), nullable=False
    )
    department: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    team_size: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    responses_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    avg_score: Mapped[float] = mapped_column(Float, nullable=True)  # 1-5 scale
    sentiment_label: Mapped[str] = mapped_column(String(50), nullable=True)  # positive, neutral, negative
    key_themes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON array
    trend_direction: Mapped[str] = mapped_column(String(20), default="stable", nullable=False)  # up, down, stable
    survey_date: Mapped[date] = mapped_column(Date, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, onupdate=utc_now, nullable=False
    )


class FlightRiskAlert(Base):
    """AI-detected flight risk alerts for at-risk employees."""

    __tablename__ = "flight_risk_alerts"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    employee_name: Mapped[str] = mapped_column(String(255), nullable=False)
    employee_email: Mapped[str] = mapped_column(String(255), nullable=False)
    department: Mapped[str] = mapped_column(String(255), nullable=False)
    risk_level: Mapped[FlightRisk] = mapped_column(
        Enum(FlightRisk), nullable=False
    )
    risk_score: Mapped[float] = mapped_column(Float, nullable=False)  # 0-100
    signals: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON array of detected signals
    recommended_actions: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON array
    acknowledged: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    acknowledged_by: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    resolved: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    resolution_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    detected_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, onupdate=utc_now, nullable=False
    )
