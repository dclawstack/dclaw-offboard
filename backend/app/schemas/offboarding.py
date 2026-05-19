"""Pydantic v2 schemas for all offboarding domain models."""

from datetime import date, datetime
from uuid import UUID
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


# ── Shared ────────────────────────────────────────────────────────────────────

class PaginatedResponse(BaseModel):
    items: list
    total: int
    page: int = 1
    page_size: int = 20


# ── Offboarding Tasks ─────────────────────────────────────────────────────────

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: str
    assigned_to: Optional[str] = None
    due_date: Optional[date] = None
    sort_order: int = 0


class TaskCreate(TaskBase):
    checklist_id: UUID


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    assigned_to: Optional[str] = None
    status: Optional[str] = None
    due_date: Optional[date] = None
    sort_order: Optional[int] = None


class TaskResponse(TaskBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    checklist_id: UUID
    status: str
    created_at: datetime
    updated_at: datetime


# ── Offboarding Checklists ────────────────────────────────────────────────────

class ChecklistBase(BaseModel):
    employee_name: str
    employee_email: str
    employee_role: str
    department: str
    last_day: date
    notes: Optional[str] = None


class ChecklistCreate(ChecklistBase):
    pass


class ChecklistUpdate(BaseModel):
    employee_name: Optional[str] = None
    employee_email: Optional[str] = None
    employee_role: Optional[str] = None
    department: Optional[str] = None
    last_day: Optional[date] = None
    status: Optional[str] = None
    notes: Optional[str] = None


class ChecklistResponse(ChecklistBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    status: str
    created_at: datetime
    updated_at: datetime
    tasks: list[TaskResponse] = []
    completion_percent: float = 0.0


# ── Assets ────────────────────────────────────────────────────────────────────

class AssetBase(BaseModel):
    name: str
    asset_type: str
    serial_number: Optional[str] = None
    assigned_to: Optional[str] = None
    assigned_to_email: Optional[str] = None
    value: Optional[float] = None
    notes: Optional[str] = None


class AssetCreate(AssetBase):
    pass


class AssetUpdate(BaseModel):
    name: Optional[str] = None
    asset_type: Optional[str] = None
    serial_number: Optional[str] = None
    assigned_to: Optional[str] = None
    assigned_to_email: Optional[str] = None
    status: Optional[str] = None
    value: Optional[float] = None
    notes: Optional[str] = None


class AssetResponse(AssetBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    status: str
    created_at: datetime
    updated_at: datetime


class AssetReturnBase(BaseModel):
    checklist_id: UUID
    asset_name: str
    asset_type: str
    serial_number: Optional[str] = None
    condition: Optional[str] = None
    notes: Optional[str] = None


class AssetReturnCreate(AssetReturnBase):
    pass


class AssetReturnUpdate(BaseModel):
    asset_name: Optional[str] = None
    asset_type: Optional[str] = None
    serial_number: Optional[str] = None
    condition: Optional[str] = None
    returned: Optional[bool] = None
    return_date: Optional[date] = None
    notes: Optional[str] = None


class AssetReturnResponse(AssetReturnBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    returned: bool
    return_date: Optional[date] = None
    created_at: datetime
    updated_at: datetime


# ── Access Revocations ────────────────────────────────────────────────────────

class RevocationBase(BaseModel):
    checklist_id: UUID
    system_name: str
    system_type: str
    notes: Optional[str] = None


class RevocationCreate(RevocationBase):
    pass


class RevocationUpdate(BaseModel):
    system_name: Optional[str] = None
    system_type: Optional[str] = None
    status: Optional[str] = None
    revoked_by: Optional[str] = None
    notes: Optional[str] = None


class RevocationResponse(RevocationBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    status: str
    revoked_at: Optional[datetime] = None
    revoked_by: Optional[str] = None
    created_at: datetime
    updated_at: datetime


# ── Exit Interviews ───────────────────────────────────────────────────────────

class ExitInterviewBase(BaseModel):
    employee_name: str
    employee_email: str
    scheduled_at: Optional[datetime] = None
    checklist_id: Optional[UUID] = None


class ExitInterviewCreate(ExitInterviewBase):
    pass


class ExitInterviewUpdate(BaseModel):
    scheduled_at: Optional[datetime] = None
    status: Optional[str] = None
    transcript: Optional[str] = None


class ExitInterviewResponse(ExitInterviewBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    status: str
    transcript: Optional[str] = None
    sentiment_score: Optional[float] = None
    sentiment_label: Optional[str] = None
    key_themes: Optional[str] = None
    summary: Optional[str] = None
    actionable_insights: Optional[str] = None
    created_at: datetime
    updated_at: datetime


# ── Knowledge Transfer ────────────────────────────────────────────────────────

class KnowledgeTransferBase(BaseModel):
    employee_name: str
    title: str
    content_type: str
    content: str
    attachments: Optional[str] = None
    successor_name: Optional[str] = None
    successor_email: Optional[str] = None
    checklist_id: Optional[UUID] = None


class KnowledgeTransferCreate(KnowledgeTransferBase):
    pass


class KnowledgeTransferUpdate(BaseModel):
    title: Optional[str] = None
    content_type: Optional[str] = None
    content: Optional[str] = None
    attachments: Optional[str] = None
    successor_name: Optional[str] = None
    successor_email: Optional[str] = None
    validated: Optional[bool] = None
    validated_by: Optional[str] = None


class KnowledgeTransferResponse(KnowledgeTransferBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    validated: bool
    validated_by: Optional[str] = None
    created_at: datetime
    updated_at: datetime


# ── Alumni ────────────────────────────────────────────────────────────────────

class AlumniBase(BaseModel):
    employee_name: str
    employee_email: str
    personal_email: Optional[str] = None
    phone: Optional[str] = None
    last_role: str
    department: str
    tenure_months: int
    last_day: date
    notes: Optional[str] = None


class AlumniCreate(AlumniBase):
    pass


class AlumniUpdate(BaseModel):
    employee_name: Optional[str] = None
    personal_email: Optional[str] = None
    phone: Optional[str] = None
    rehire_eligibility: Optional[str] = None
    exit_interview_summary: Optional[str] = None
    notes: Optional[str] = None


class AlumniResponse(AlumniBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    rehire_eligibility: str
    exit_interview_summary: Optional[str] = None
    created_at: datetime
    updated_at: datetime


# ── Final Pay ─────────────────────────────────────────────────────────────────

class FinalPayBase(BaseModel):
    employee_name: str
    employee_email: str
    last_day: date
    base_salary: float = 0.0
    unused_pto_hours: float = 0.0
    pto_payout_rate: float = 0.0
    severance_weeks: float = 0.0
    bonus_amount: float = 0.0
    deductions: float = 0.0
    checklist_id: Optional[UUID] = None


class FinalPayCreate(FinalPayBase):
    pass


class FinalPayUpdate(BaseModel):
    base_salary: Optional[float] = None
    unused_pto_hours: Optional[float] = None
    pto_payout_rate: Optional[float] = None
    severance_weeks: Optional[float] = None
    bonus_amount: Optional[float] = None
    deductions: Optional[float] = None
    compliance_notes: Optional[str] = None


class FinalPayResponse(FinalPayBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    severance_amount: float
    total_final_pay: float
    compliance_notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime


# ── Dashboard ─────────────────────────────────────────────────────────────────

class DashboardStats(BaseModel):
    total_checklists: int = 0
    active_checklists: int = 0
    completed_checklists: int = 0
    total_assets_pending: int = 0
    total_revocations_pending: int = 0
    pending_interviews: int = 0
    alumni_count: int = 0
    recent_checklists: list[ChecklistResponse] = []


# ── AI Copilot ────────────────────────────────────────────────────────────────

class CopilotRequest(BaseModel):
    message: str
    context: Optional[str] = None  # JSON with checklist_id, role, etc.


class CopilotResponse(BaseModel):
    reply: str
    suggested_actions: list[str] = []
    sources: list[str] = []
