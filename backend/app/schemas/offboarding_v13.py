"""Pydantic v2 schemas for v1.3 features.

Risk Assessment, Integration Hub, Team Transition, Compliance, Sentiment.
"""

from datetime import date, datetime
from uuid import UUID
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


# ── Risk Assessment ──────────────────────────────────────────────────────────

class RiskAssessmentBase(BaseModel):
    employee_name: str
    employee_email: str
    department: str
    role: str
    last_day: Optional[date] = None


class RiskAssessmentCreate(RiskAssessmentBase):
    pass


class RiskAssessmentUpdate(BaseModel):
    risk_level: Optional[str] = None
    risk_score: Optional[float] = None
    anomalies: Optional[str] = None
    evidence_preserved: Optional[bool] = None
    evidence_location: Optional[str] = None
    recommendations: Optional[str] = None
    notes: Optional[str] = None


class RiskAssessmentResponse(RiskAssessmentBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    risk_level: str
    risk_score: float
    unusual_file_access: int
    large_downloads: int
    email_forwarding_detected: bool
    usb_activity_detected: bool
    after_hours_activity: int
    anomalies: Optional[str] = None
    evidence_preserved: bool
    evidence_location: Optional[str] = None
    recommendations: Optional[str] = None
    monitoring_start: Optional[datetime] = None
    monitoring_end: Optional[datetime] = None
    assessed_by: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime


# ── Integration Hub ──────────────────────────────────────────────────────────

class IntegrationBase(BaseModel):
    name: str
    provider: str
    category: str
    api_endpoint: Optional[str] = None
    auth_type: str = "oauth2"
    credentials_ref: Optional[str] = None
    webhook_url: Optional[str] = None
    config: Optional[dict] = None
    metadata_info: Optional[dict] = None


class IntegrationCreate(IntegrationBase):
    pass


class IntegrationUpdate(BaseModel):
    name: Optional[str] = None
    api_endpoint: Optional[str] = None
    credentials_ref: Optional[str] = None
    webhook_url: Optional[str] = None
    enabled: Optional[bool] = None
    config: Optional[dict] = None
    metadata_info: Optional[dict] = None


class IntegrationResponse(IntegrationBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    status: str
    last_sync_at: Optional[datetime] = None
    sync_status: Optional[str] = None
    enabled: bool
    created_at: datetime
    updated_at: datetime


class IntegrationActionBase(BaseModel):
    integration_id: UUID
    action_type: str
    target: str


class IntegrationActionResponse(IntegrationActionBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    status: str
    result_detail: Optional[str] = None
    executed_at: Optional[datetime] = None
    duration_ms: Optional[int] = None
    created_at: datetime


class IntegrationSyncResult(BaseModel):
    integration_id: UUID
    provider: str
    status: str
    actions_performed: int
    errors: list[str] = []
    synced_at: Optional[datetime] = None


# ── Team Transition ──────────────────────────────────────────────────────────

class CoverageItemBase(BaseModel):
    responsibility: str
    category: str
    assigned_to_name: str
    assigned_to_email: str
    start_date: date
    end_date: Optional[date] = None
    is_permanent: bool = False
    notes: Optional[str] = None


class CoverageItemCreate(CoverageItemBase):
    transition_id: UUID


class CoverageItemUpdate(BaseModel):
    responsibility: Optional[str] = None
    assigned_to_name: Optional[str] = None
    assigned_to_email: Optional[str] = None
    status: Optional[str] = None
    end_date: Optional[date] = None
    is_permanent: Optional[bool] = None
    notes: Optional[str] = None


class CoverageItemResponse(CoverageItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    transition_id: UUID
    status: str
    created_at: datetime
    updated_at: datetime


class TeamTransitionBase(BaseModel):
    departing_employee_name: str
    departing_employee_email: str
    department: str
    role: str
    last_day: date
    successor_name: Optional[str] = None
    successor_email: Optional[str] = None


class TeamTransitionCreate(TeamTransitionBase):
    pass


class TeamTransitionUpdate(BaseModel):
    successor_name: Optional[str] = None
    successor_email: Optional[str] = None
    status: Optional[str] = None


class TeamTransitionResponse(TeamTransitionBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    status: str
    coverage_items: list[CoverageItemResponse] = []
    created_at: datetime
    updated_at: datetime


# ── Compliance ───────────────────────────────────────────────────────────────

class ComplianceReportBase(BaseModel):
    framework: str
    employee_name: str
    employee_email: str
    department: str
    last_day: date


class ComplianceReportCreate(ComplianceReportBase):
    pass


class ComplianceReportUpdate(BaseModel):
    status: Optional[str] = None
    report_data: Optional[dict] = None
    ai_validated: Optional[bool] = None
    validation_notes: Optional[str] = None
    retention_deadline: Optional[date] = None
    retention_completed: Optional[bool] = None


class ComplianceReportResponse(ComplianceReportBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    status: str
    report_data: Optional[dict] = None
    ai_validated: bool
    validation_notes: Optional[str] = None
    submitted_at: Optional[datetime] = None
    retention_deadline: Optional[date] = None
    retention_completed: bool
    created_at: datetime
    updated_at: datetime


class NonCompeteTrackerBase(BaseModel):
    employee_name: str
    employee_email: str
    agreement_type: str
    effective_date: date
    expiration_date: date
    restrictions_summary: Optional[str] = None


class NonCompeteTrackerCreate(NonCompeteTrackerBase):
    pass


class NonCompeteTrackerResponse(NonCompeteTrackerBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    is_active: bool
    last_reviewed: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


# ── Sentiment & Early Warning ────────────────────────────────────────────────

class SentimentPulseBase(BaseModel):
    title: str
    category: str
    department: Optional[str] = None
    team_size: Optional[int] = None
    survey_date: date


class SentimentPulseCreate(SentimentPulseBase):
    pass


class SentimentPulseUpdate(BaseModel):
    responses_count: Optional[int] = None
    avg_score: Optional[float] = None
    sentiment_label: Optional[str] = None
    key_themes: Optional[str] = None
    trend_direction: Optional[str] = None


class SentimentPulseResponse(SentimentPulseBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    responses_count: int
    avg_score: Optional[float] = None
    sentiment_label: Optional[str] = None
    key_themes: Optional[str] = None
    trend_direction: str
    created_at: datetime
    updated_at: datetime


class FlightRiskAlertBase(BaseModel):
    employee_name: str
    employee_email: str
    department: str
    risk_level: str
    risk_score: float
    signals: Optional[str] = None
    recommended_actions: Optional[str] = None


class FlightRiskAlertUpdate(BaseModel):
    acknowledged: Optional[bool] = None
    acknowledged_by: Optional[str] = None
    resolved: Optional[bool] = None
    resolution_notes: Optional[str] = None


class FlightRiskAlertResponse(FlightRiskAlertBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    acknowledged: bool
    acknowledged_by: Optional[str] = None
    resolved: bool
    resolution_notes: Optional[str] = None
    detected_at: datetime
    created_at: datetime
    updated_at: datetime


# ── Aggregated Dashboard (updated for v1.3) ──────────────────────────────────

class RiskOverview(BaseModel):
    total_assessments: int = 0
    critical_risks: int = 0
    high_risks: int = 0
    evidence_preserved_count: int = 0


class IntegrationOverview(BaseModel):
    total_integrations: int = 0
    connected_count: int = 0
    error_count: int = 0
    pending_actions: int = 0


class SentimentOverview(BaseModel):
    active_alerts: int = 0
    high_risk_employees: int = 0
    avg_engagement_score: float = 0.0
    trend_direction: str = "stable"


class DashboardStatsV13(BaseModel):
    total_checklists: int = 0
    active_checklists: int = 0
    completed_checklists: int = 0
    total_assets_pending: int = 0
    total_revocations_pending: int = 0
    pending_interviews: int = 0
    alumni_count: int = 0
    risk_overview: RiskOverview = RiskOverview()
    integration_overview: IntegrationOverview = IntegrationOverview()
    sentiment_overview: SentimentOverview = SentimentOverview()
    recent_checklists: list = []
