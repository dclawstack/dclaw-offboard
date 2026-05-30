"""API v1 routes — v1.3 features.

Covers:
- Risk Assessment & IP Protection
- Integration Hub
- Team Transition & Coverage
- Compliance Automation
- Employee Sentiment & Early Warning
"""

from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.offboarding_v13 import (
    ComplianceReport,
    CoverageItem,
    FlightRiskAlert,
    Integration,
    IntegrationAction,
    NonCompeteTracker,
    RiskAssessment,
    SentimentPulse,
    TeamTransition,
    ReportStatus,
    IntegrationStatus,
)
from app.repositories.base_repo import BaseRepository
from app.schemas.offboarding_v13 import (
    ComplianceReportCreate,
    ComplianceReportResponse,
    ComplianceReportUpdate,
    CoverageItemCreate,
    CoverageItemResponse,
    CoverageItemUpdate,
    FlightRiskAlertResponse,
    FlightRiskAlertUpdate,
    IntegrationCreate,
    IntegrationResponse,
    IntegrationSyncResult,
    IntegrationUpdate,
    NonCompeteTrackerCreate,
    NonCompeteTrackerResponse,
    RiskAssessmentCreate,
    RiskAssessmentResponse,
    RiskAssessmentUpdate,
    SentimentPulseCreate,
    SentimentPulseResponse,
    SentimentPulseUpdate,
    TeamTransitionCreate,
    TeamTransitionResponse,
    TeamTransitionUpdate,
)
from app.services.compliance_automation import (
    create_non_compete_tracker,
    generate_compliance_report,
)
from app.services.integration_hub import (
    get_integration_overview,
    seed_default_integrations,
    simulate_offboard_actions,
    simulate_sync,
)
from app.services.risk_assessment import get_risk_overview, run_risk_assessment
from app.services.sentiment_early_warning import (
    create_pulse_survey,
    detect_flight_risk,
    get_sentiment_overview,
)
from app.services.team_transition import create_transition_with_coverage

router = APIRouter()


# ── Helper ────────────────────────────────────────────────────────────────────

def _paginated(items: list, total: int, page: int, page_size: int) -> dict:
    return {"items": items, "total": total, "page": page, "page_size": page_size}


# ══════════════════════════════════════════════════════════════════════════════
# Risk Assessment & IP Protection
# ══════════════════════════════════════════════════════════════════════════════

@router.get("/risk-assessments", tags=["Risk Assessment"])
async def list_risk_assessments(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    repo = BaseRepository(db, RiskAssessment)
    items, total = await repo.list_all(limit=page_size, offset=(page - 1) * page_size)
    return _paginated(
        [RiskAssessmentResponse.model_validate(r) for r in items], total, page, page_size
    )


@router.post("/risk-assessments/run", response_model=RiskAssessmentResponse, status_code=201, tags=["Risk Assessment"])
async def run_assessment(data: RiskAssessmentCreate, db: AsyncSession = Depends(get_db)):
    """Run an AI-driven risk assessment for a departing employee."""
    assessment = await run_risk_assessment(
        db=db,
        employee_name=data.employee_name,
        employee_email=data.employee_email,
        department=data.department,
        role=data.role,
        last_day=data.last_day,
    )
    return RiskAssessmentResponse.model_validate(assessment)


@router.get("/risk-assessments/{assessment_id}", response_model=RiskAssessmentResponse, tags=["Risk Assessment"])
async def get_risk_assessment(assessment_id: UUID, db: AsyncSession = Depends(get_db)):
    repo = BaseRepository(db, RiskAssessment)
    item = await repo.get_by_id(assessment_id)
    if not item:
        raise HTTPException(404, "Risk assessment not found")
    return RiskAssessmentResponse.model_validate(item)


@router.put("/risk-assessments/{assessment_id}", response_model=RiskAssessmentResponse, tags=["Risk Assessment"])
async def update_risk_assessment(
    assessment_id: UUID, data: RiskAssessmentUpdate, db: AsyncSession = Depends(get_db)
):
    repo = BaseRepository(db, RiskAssessment)
    item = await repo.get_by_id(assessment_id)
    if not item:
        raise HTTPException(404, "Risk assessment not found")
    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(item, key, val)
    await db.commit()
    await db.refresh(item)
    return RiskAssessmentResponse.model_validate(item)


@router.delete("/risk-assessments/{assessment_id}", status_code=204, tags=["Risk Assessment"])
async def delete_risk_assessment(assessment_id: UUID, db: AsyncSession = Depends(get_db)):
    repo = BaseRepository(db, RiskAssessment)
    item = await repo.get_by_id(assessment_id)
    if not item:
        raise HTTPException(404, "Risk assessment not found")
    await repo.delete(item)
    return None


@router.get("/risk-assessment/overview", tags=["Risk Assessment"])
async def risk_overview(db: AsyncSession = Depends(get_db)):
    """Get risk dashboard overview."""
    return await get_risk_overview(db)


# ══════════════════════════════════════════════════════════════════════════════
# Integration Hub
# ══════════════════════════════════════════════════════════════════════════════

@router.get("/integrations", tags=["Integrations"])
async def list_integrations(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    repo = BaseRepository(db, Integration)
    items, total = await repo.list_all(limit=page_size, offset=(page - 1) * page_size)
    return _paginated(
        [IntegrationResponse.model_validate(i) for i in items], total, page, page_size
    )


@router.post("/integrations/seed", tags=["Integrations"])
async def seed_integrations(db: AsyncSession = Depends(get_db)):
    """Seed default integration connectors (idempotent)."""
    count = await seed_default_integrations(db)
    return {"seeded": count, "message": f"Seeded {count} new integration connectors"}


@router.post("/integrations", response_model=IntegrationResponse, status_code=201, tags=["Integrations"])
async def create_integration(data: IntegrationCreate, db: AsyncSession = Depends(get_db)):
    repo = BaseRepository(db, Integration)
    integration = Integration(**data.model_dump())
    integration = await repo.create(integration)
    return IntegrationResponse.model_validate(integration)


@router.put("/integrations/{integration_id}", response_model=IntegrationResponse, tags=["Integrations"])
async def update_integration(
    integration_id: UUID, data: IntegrationUpdate, db: AsyncSession = Depends(get_db)
):
    repo = BaseRepository(db, Integration)
    item = await repo.get_by_id(integration_id)
    if not item:
        raise HTTPException(404, "Integration not found")
    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(item, key, val)
    await db.commit()
    await db.refresh(item)
    return IntegrationResponse.model_validate(item)


@router.delete("/integrations/{integration_id}", status_code=204, tags=["Integrations"])
async def delete_integration(integration_id: UUID, db: AsyncSession = Depends(get_db)):
    repo = BaseRepository(db, Integration)
    item = await repo.get_by_id(integration_id)
    if not item:
        raise HTTPException(404, "Integration not found")
    await repo.delete(item)
    return None


@router.post("/integrations/{integration_id}/sync", tags=["Integrations"])
async def sync_integration(integration_id: UUID, db: AsyncSession = Depends(get_db)):
    """Sync with an integration provider."""
    result = await simulate_sync(db, integration_id)
    if result.get("status") == "error":
        raise HTTPException(404, result.get("message", "Sync failed"))
    return result


@router.post("/integrations/{integration_id}/offboard", tags=["Integrations"])
async def offboard_via_integration(
    integration_id: UUID,
    employee_email: str = Query(...),
    db: AsyncSession = Depends(get_db),
):
    """Execute offboarding actions through a connected integration."""
    results = await simulate_offboard_actions(db, integration_id, employee_email)
    return {"actions": results, "employee_email": employee_email}


@router.get("/integration/overview", tags=["Integrations"])
async def integration_overview(db: AsyncSession = Depends(get_db)):
    """Get integration hub dashboard overview."""
    return await get_integration_overview(db)


# ══════════════════════════════════════════════════════════════════════════════
# Team Transition & Coverage
# ══════════════════════════════════════════════════════════════════════════════

@router.get("/team-transitions", tags=["Team Transition"])
async def list_team_transitions(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    repo = BaseRepository(db, TeamTransition)
    items, total = await repo.list_all(limit=page_size, offset=(page - 1) * page_size)
    return _paginated(
        [TeamTransitionResponse.model_validate(t) for t in items], total, page, page_size
    )


@router.post("/team-transitions", response_model=TeamTransitionResponse, status_code=201, tags=["Team Transition"])
async def create_team_transition(data: TeamTransitionCreate, db: AsyncSession = Depends(get_db)):
    """Create a team transition plan with auto-generated coverage items."""
    transition = await create_transition_with_coverage(
        db=db,
        employee_name=data.departing_employee_name,
        employee_email=data.departing_employee_email,
        department=data.department,
        role=data.role,
        last_day=data.last_day,
        successor_name=data.successor_name,
        successor_email=data.successor_email,
    )
    return TeamTransitionResponse.model_validate(transition)


@router.get("/team-transitions/{transition_id}", response_model=TeamTransitionResponse, tags=["Team Transition"])
async def get_team_transition(transition_id: UUID, db: AsyncSession = Depends(get_db)):
    repo = BaseRepository(db, TeamTransition)
    item = await repo.get_by_id(transition_id)
    if not item:
        raise HTTPException(404, "Team transition not found")
    return TeamTransitionResponse.model_validate(item)


@router.put("/team-transitions/{transition_id}", response_model=TeamTransitionResponse, tags=["Team Transition"])
async def update_team_transition(
    transition_id: UUID, data: TeamTransitionUpdate, db: AsyncSession = Depends(get_db)
):
    repo = BaseRepository(db, TeamTransition)
    item = await repo.get_by_id(transition_id)
    if not item:
        raise HTTPException(404, "Team transition not found")
    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(item, key, val)
    await db.commit()
    await db.refresh(item)
    return TeamTransitionResponse.model_validate(item)


@router.delete("/team-transitions/{transition_id}", status_code=204, tags=["Team Transition"])
async def delete_team_transition(transition_id: UUID, db: AsyncSession = Depends(get_db)):
    repo = BaseRepository(db, TeamTransition)
    item = await repo.get_by_id(transition_id)
    if not item:
        raise HTTPException(404, "Team transition not found")
    await repo.delete(item)
    return None


# ── Coverage Items ────────────────────────────────────────────────────────────

@router.post("/coverage-items", response_model=CoverageItemResponse, status_code=201, tags=["Team Transition"])
async def create_coverage_item(data: CoverageItemCreate, db: AsyncSession = Depends(get_db)):
    repo = BaseRepository(db, CoverageItem)
    item = CoverageItem(**data.model_dump())
    item = await repo.create(item)
    return CoverageItemResponse.model_validate(item)


@router.put("/coverage-items/{item_id}", response_model=CoverageItemResponse, tags=["Team Transition"])
async def update_coverage_item(
    item_id: UUID, data: CoverageItemUpdate, db: AsyncSession = Depends(get_db)
):
    repo = BaseRepository(db, CoverageItem)
    item = await repo.get_by_id(item_id)
    if not item:
        raise HTTPException(404, "Coverage item not found")
    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(item, key, val)
    await db.commit()
    await db.refresh(item)
    return CoverageItemResponse.model_validate(item)


@router.delete("/coverage-items/{item_id}", status_code=204, tags=["Team Transition"])
async def delete_coverage_item(item_id: UUID, db: AsyncSession = Depends(get_db)):
    repo = BaseRepository(db, CoverageItem)
    item = await repo.get_by_id(item_id)
    if not item:
        raise HTTPException(404, "Coverage item not found")
    await repo.delete(item)
    return None


# ══════════════════════════════════════════════════════════════════════════════
# Compliance Automation
# ══════════════════════════════════════════════════════════════════════════════

@router.get("/compliance-reports", tags=["Compliance"])
async def list_compliance_reports(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    repo = BaseRepository(db, ComplianceReport)
    items, total = await repo.list_all(limit=page_size, offset=(page - 1) * page_size)
    return _paginated(
        [ComplianceReportResponse.model_validate(c) for c in items], total, page, page_size
    )


@router.post("/compliance-reports/generate", response_model=ComplianceReportResponse, status_code=201, tags=["Compliance"])
async def create_compliance_report(data: ComplianceReportCreate, db: AsyncSession = Depends(get_db)):
    """Generate an AI-validated compliance report."""
    report = await generate_compliance_report(
        db=db,
        framework=data.framework,
        employee_name=data.employee_name,
        employee_email=data.employee_email,
        department=data.department,
        last_day=data.last_day,
    )
    return ComplianceReportResponse.model_validate(report)


@router.put("/compliance-reports/{report_id}", response_model=ComplianceReportResponse, tags=["Compliance"])
async def update_compliance_report(
    report_id: UUID, data: ComplianceReportUpdate, db: AsyncSession = Depends(get_db)
):
    repo = BaseRepository(db, ComplianceReport)
    item = await repo.get_by_id(report_id)
    if not item:
        raise HTTPException(404, "Compliance report not found")
    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(item, key, val)
    await db.commit()
    await db.refresh(item)
    return ComplianceReportResponse.model_validate(item)


@router.post("/compliance-reports/{report_id}/submit", tags=["Compliance"])
async def submit_compliance_report(report_id: UUID, db: AsyncSession = Depends(get_db)):
    """Submit a compliance report (marks as submitted)."""
    repo = BaseRepository(db, ComplianceReport)
    item = await repo.get_by_id(report_id)
    if not item:
        raise HTTPException(404, "Compliance report not found")
    item.status = ReportStatus.submitted
    item.submitted_at = __import__("datetime").datetime.utcnow()
    await db.commit()
    await db.refresh(item)
    return ComplianceReportResponse.model_validate(item)


@router.get("/non-compete-trackers", tags=["Compliance"])
async def list_non_compete_trackers(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    repo = BaseRepository(db, NonCompeteTracker)
    items, total = await repo.list_all(limit=page_size, offset=(page - 1) * page_size)
    return _paginated(
        [NonCompeteTrackerResponse.model_validate(n) for n in items], total, page, page_size
    )


@router.post("/non-compete-trackers", response_model=NonCompeteTrackerResponse, status_code=201, tags=["Compliance"])
async def create_non_compete(data: NonCompeteTrackerCreate, db: AsyncSession = Depends(get_db)):
    """Track a non-compete or NDA agreement."""
    tracker = await create_non_compete_tracker(
        db=db,
        employee_name=data.employee_name,
        employee_email=data.employee_email,
        agreement_type=data.agreement_type,
        effective_date=data.effective_date,
        expiration_date=data.expiration_date,
        restrictions_summary=data.restrictions_summary,
    )
    return NonCompeteTrackerResponse.model_validate(tracker)


@router.delete("/non-compete-trackers/{tracker_id}", status_code=204, tags=["Compliance"])
async def delete_non_compete(tracker_id: UUID, db: AsyncSession = Depends(get_db)):
    repo = BaseRepository(db, NonCompeteTracker)
    item = await repo.get_by_id(tracker_id)
    if not item:
        raise HTTPException(404, "Non-compete tracker not found")
    await repo.delete(item)
    return None


# ══════════════════════════════════════════════════════════════════════════════
# Employee Sentiment & Early Warning
# ══════════════════════════════════════════════════════════════════════════════

@router.get("/sentiment-pulses", tags=["Sentiment"])
async def list_sentiment_pulses(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    repo = BaseRepository(db, SentimentPulse)
    items, total = await repo.list_all(limit=page_size, offset=(page - 1) * page_size)
    return _paginated(
        [SentimentPulseResponse.model_validate(s) for s in items], total, page, page_size
    )


@router.post("/sentiment-pulses", response_model=SentimentPulseResponse, status_code=201, tags=["Sentiment"])
async def create_pulse(data: SentimentPulseCreate, db: AsyncSession = Depends(get_db)):
    """Create and analyze a sentiment pulse survey."""
    pulse = await create_pulse_survey(
        db=db,
        title=data.title,
        category=data.category,
        department=data.department,
        team_size=data.team_size,
        survey_date=data.survey_date,
    )
    return SentimentPulseResponse.model_validate(pulse)


@router.put("/sentiment-pulses/{pulse_id}", response_model=SentimentPulseResponse, tags=["Sentiment"])
async def update_pulse(
    pulse_id: UUID, data: SentimentPulseUpdate, db: AsyncSession = Depends(get_db)
):
    repo = BaseRepository(db, SentimentPulse)
    item = await repo.get_by_id(pulse_id)
    if not item:
        raise HTTPException(404, "Sentiment pulse not found")
    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(item, key, val)
    await db.commit()
    await db.refresh(item)
    return SentimentPulseResponse.model_validate(item)


@router.delete("/sentiment-pulses/{pulse_id}", status_code=204, tags=["Sentiment"])
async def delete_pulse(pulse_id: UUID, db: AsyncSession = Depends(get_db)):
    repo = BaseRepository(db, SentimentPulse)
    item = await repo.get_by_id(pulse_id)
    if not item:
        raise HTTPException(404, "Sentiment pulse not found")
    await repo.delete(item)
    return None


@router.get("/flight-risk-alerts", tags=["Sentiment"])
async def list_flight_risk_alerts(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    repo = BaseRepository(db, FlightRiskAlert)
    items, total = await repo.list_all(limit=page_size, offset=(page - 1) * page_size)
    return _paginated(
        [FlightRiskAlertResponse.model_validate(f) for f in items], total, page, page_size
    )


@router.post("/flight-risk-alerts/detect", response_model=FlightRiskAlertResponse, status_code=201, tags=["Sentiment"])
async def run_flight_risk_detection(
    employee_name: str = Query(...),
    employee_email: str = Query(...),
    department: str = Query(...),
    db: AsyncSession = Depends(get_db),
):
    """Run AI flight risk detection for an employee."""
    alert = await detect_flight_risk(
        db=db,
        employee_name=employee_name,
        employee_email=employee_email,
        department=department,
    )
    return FlightRiskAlertResponse.model_validate(alert)


@router.put("/flight-risk-alerts/{alert_id}", response_model=FlightRiskAlertResponse, tags=["Sentiment"])
async def update_flight_risk_alert(
    alert_id: UUID, data: FlightRiskAlertUpdate, db: AsyncSession = Depends(get_db)
):
    """Acknowledge or resolve a flight risk alert."""
    repo = BaseRepository(db, FlightRiskAlert)
    item = await repo.get_by_id(alert_id)
    if not item:
        raise HTTPException(404, "Flight risk alert not found")
    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(item, key, val)
    await db.commit()
    await db.refresh(item)
    return FlightRiskAlertResponse.model_validate(item)


@router.delete("/flight-risk-alerts/{alert_id}", status_code=204, tags=["Sentiment"])
async def delete_flight_risk_alert(alert_id: UUID, db: AsyncSession = Depends(get_db)):
    repo = BaseRepository(db, FlightRiskAlert)
    item = await repo.get_by_id(alert_id)
    if not item:
        raise HTTPException(404, "Flight risk alert not found")
    await repo.delete(item)
    return None


@router.get("/sentiment/overview", tags=["Sentiment"])
async def sentiment_overview(db: AsyncSession = Depends(get_db)):
    """Get sentiment and early warning dashboard overview."""
    return await get_sentiment_overview(db)
