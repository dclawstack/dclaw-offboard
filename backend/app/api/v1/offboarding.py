"""API v1 routes — Offboarding domain.

Covers all P0 and P1 features:
- Checklists & Tasks (P0.2)
- Asset Recovery (P0.3)
- Access Revocation (P0.4)
- AI Copilot (P0.1)
- Exit Interviews (P1.5)
- Knowledge Transfer (P1.6)
- Alumni Network (P1.7)
- Final Pay (P1.8)
- Dashboard (summary)
"""

from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.offboarding import (
    AlumniRepository,
    AssetRepository,
    AssetReturnRepository,
    ChecklistRepository,
    ExitInterviewRepository,
    FinalPayRepository,
    KnowledgeTransferRepository,
    RevocationRepository,
    TaskRepository,
)
from app.schemas.offboarding import (
    AlumniCreate,
    AlumniResponse,
    AlumniUpdate,
    AssetCreate,
    AssetResponse,
    AssetReturnCreate,
    AssetReturnResponse,
    AssetReturnUpdate,
    AssetUpdate,
    ChecklistCreate,
    ChecklistResponse,
    ChecklistUpdate,
    CopilotRequest,
    CopilotResponse,
    DashboardStats,
    ExitInterviewCreate,
    ExitInterviewResponse,
    ExitInterviewUpdate,
    FinalPayCreate,
    FinalPayResponse,
    FinalPayUpdate,
    KnowledgeTransferCreate,
    KnowledgeTransferResponse,
    KnowledgeTransferUpdate,
    PaginatedResponse,
    RevocationCreate,
    RevocationResponse,
    RevocationUpdate,
    TaskCreate,
    TaskResponse,
    TaskUpdate,
)
from app.services.access_control import (
    generate_revocation_list,
    get_audit_trail,
    get_pending_revocations_count,
    revoke_all_for_checklist,
    revoke_single,
)
from app.services.asset_recovery import (
    generate_recovery_list,
    get_pending_returns_count,
    mark_returned,
)
from app.services.offboard_ai import (
    analyze_exit_interview_sentiment,
    generate_copilot_response,
)
from app.services.offboard_workflow import create_checklist_with_tasks

router = APIRouter()


# ── Helper ────────────────────────────────────────────────────────────────────

def _paginated(items: list, total: int, page: int, page_size: int) -> dict:
    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
    }


# ══════════════════════════════════════════════════════════════════════════════
# P0.1: AI Copilot
# ══════════════════════════════════════════════════════════════════════════════

@router.post("/ai/offboard-chat", response_model=CopilotResponse, tags=["AI"])
async def copilot_chat(request: CopilotRequest):
    """Chat with the AI Offboard Copilot."""
    return await generate_copilot_response(request)


@router.post("/ai/analyze-interview/{interview_id}", tags=["AI"])
async def analyze_interview(
    interview_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Run AI sentiment analysis on an exit interview transcript."""
    repo = ExitInterviewRepository(db)
    interview = await repo.get_by_id(interview_id)
    if not interview or not interview.transcript:
        raise HTTPException(404, "Interview not found or has no transcript")

    result = await analyze_exit_interview_sentiment(interview.transcript)
    interview.sentiment_score = result["sentiment_score"]
    interview.sentiment_label = result["sentiment_label"]
    interview.key_themes = str(result["key_themes"])
    interview.summary = result["summary"]
    interview.actionable_insights = result["actionable_insights"]

    await db.commit()
    await db.refresh(interview)
    return ExitInterviewResponse.model_validate(interview)


# ══════════════════════════════════════════════════════════════════════════════
# P0.2: Offboarding Checklists & Workflow
# ══════════════════════════════════════════════════════════════════════════════

@router.get("/checklists", tags=["Checklists"])
async def list_checklists(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """List all offboarding checklists with pagination."""
    repo = ChecklistRepository(db)
    items, total = await repo.list_all(limit=page_size, offset=(page - 1) * page_size)
    return _paginated(
        [ChecklistResponse.model_validate(c) for c in items], total, page, page_size
    )


@router.post("/checklists", response_model=ChecklistResponse, status_code=201, tags=["Checklists"])
async def create_checklist(
    data: ChecklistCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a new offboarding checklist with auto-generated tasks."""
    checklist = await create_checklist_with_tasks(db, data)
    return ChecklistResponse.model_validate(checklist)


@router.get("/checklists/{checklist_id}", response_model=ChecklistResponse, tags=["Checklists"])
async def get_checklist(
    checklist_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Get a single offboarding checklist with tasks."""
    repo = ChecklistRepository(db)
    checklist = await repo.get_with_all(checklist_id)
    if not checklist:
        raise HTTPException(404, "Checklist not found")
    resp = ChecklistResponse.model_validate(checklist)
    resp.completion_percent = await repo.get_completion_percent(checklist_id)
    return resp


@router.put("/checklists/{checklist_id}", response_model=ChecklistResponse, tags=["Checklists"])
async def update_checklist(
    checklist_id: UUID,
    data: ChecklistUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update an offboarding checklist."""
    repo = ChecklistRepository(db)
    checklist = await repo.get_by_id(checklist_id)
    if not checklist:
        raise HTTPException(404, "Checklist not found")
    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(checklist, key, val)
    await db.commit()
    await db.refresh(checklist)
    return ChecklistResponse.model_validate(checklist)


@router.delete("/checklists/{checklist_id}", status_code=204, tags=["Checklists"])
async def delete_checklist(
    checklist_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Delete an offboarding checklist."""
    repo = ChecklistRepository(db)
    checklist = await repo.get_by_id(checklist_id)
    if not checklist:
        raise HTTPException(404, "Checklist not found")
    await repo.delete(checklist)
    return None


# ── Tasks ─────────────────────────────────────────────────────────────────────

@router.get("/checklists/{checklist_id}/tasks", response_model=list[TaskResponse], tags=["Tasks"])
async def list_tasks(
    checklist_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """List all tasks for a checklist."""
    repo = TaskRepository(db)
    tasks = await repo.list_by_checklist(checklist_id)
    return [TaskResponse.model_validate(t) for t in tasks]


@router.post("/tasks", response_model=TaskResponse, status_code=201, tags=["Tasks"])
async def create_task(
    data: TaskCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a task on a checklist."""
    from app.models.offboarding import OffboardingTask
    task = OffboardingTask(**data.model_dump())
    repo = TaskRepository(db)
    task = await repo.create(task)
    return TaskResponse.model_validate(task)


@router.put("/tasks/{task_id}", response_model=TaskResponse, tags=["Tasks"])
async def update_task(
    task_id: UUID,
    data: TaskUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update a task (e.g., mark complete)."""
    repo = TaskRepository(db)
    task = await repo.get_by_id(task_id)
    if not task:
        raise HTTPException(404, "Task not found")
    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(task, key, val)
    await db.commit()
    await db.refresh(task)
    return TaskResponse.model_validate(task)


@router.delete("/tasks/{task_id}", status_code=204, tags=["Tasks"])
async def delete_task(
    task_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Delete a task."""
    repo = TaskRepository(db)
    task = await repo.get_by_id(task_id)
    if not task:
        raise HTTPException(404, "Task not found")
    await repo.delete(task)
    return None


# ══════════════════════════════════════════════════════════════════════════════
# P0.3: Asset Recovery & Inventory
# ══════════════════════════════════════════════════════════════════════════════

@router.get("/assets", tags=["Assets"])
async def list_assets(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """List all company assets."""
    repo = AssetRepository(db)
    items, total = await repo.list_all(limit=page_size, offset=(page - 1) * page_size)
    return _paginated(
        [AssetResponse.model_validate(a) for a in items], total, page, page_size
    )


@router.post("/assets", response_model=AssetResponse, status_code=201, tags=["Assets"])
async def create_asset(
    data: AssetCreate,
    db: AsyncSession = Depends(get_db),
):
    """Register a new company asset."""
    from app.models.offboarding import Asset as AssetModel
    repo = AssetRepository(db)
    asset = AssetModel(**data.model_dump())
    asset = await repo.create(asset)
    return AssetResponse.model_validate(asset)


@router.put("/assets/{asset_id}", response_model=AssetResponse, tags=["Assets"])
async def update_asset(
    asset_id: UUID,
    data: AssetUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update an asset."""
    repo = AssetRepository(db)
    asset = await repo.get_by_id(asset_id)
    if not asset:
        raise HTTPException(404, "Asset not found")
    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(asset, key, val)
    await db.commit()
    await db.refresh(asset)
    return AssetResponse.model_validate(asset)


@router.delete("/assets/{asset_id}", status_code=204, tags=["Assets"])
async def delete_asset(
    asset_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Delete an asset."""
    repo = AssetRepository(db)
    asset = await repo.get_by_id(asset_id)
    if not asset:
        raise HTTPException(404, "Asset not found")
    await repo.delete(asset)
    return None


# ── Asset Returns ─────────────────────────────────────────────────────────────

@router.post("/asset-returns/generate/{checklist_id}", tags=["Assets"])
async def generate_asset_returns(
    checklist_id: UUID,
    role: str = Query("general"),
    name: str = Query("Employee"),
    db: AsyncSession = Depends(get_db),
):
    """Auto-generate asset return list for a checklist based on employee role."""
    items = await generate_recovery_list(db, checklist_id, role, name)
    return [AssetReturnResponse.model_validate(i) for i in items]


@router.get("/checklists/{checklist_id}/asset-returns", tags=["Assets"])
async def list_asset_returns(
    checklist_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """List asset returns for a checklist."""
    repo = AssetReturnRepository(db)
    items = await repo.list_by_checklist(checklist_id)
    return [AssetReturnResponse.model_validate(i) for i in items]


@router.put("/asset-returns/{return_id}/mark-returned", tags=["Assets"])
async def mark_asset_returned(
    return_id: UUID,
    condition: str | None = None,
    notes: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    """Mark an asset as returned."""
    result = await mark_returned(db, return_id, condition, notes)
    if not result:
        raise HTTPException(404, "Asset return record not found")
    return AssetReturnResponse.model_validate(result)


# ══════════════════════════════════════════════════════════════════════════════
# P0.4: Access Revocation
# ══════════════════════════════════════════════════════════════════════════════

@router.post("/access-revocations/generate/{checklist_id}", tags=["Access"])
async def generate_revocations(
    checklist_id: UUID,
    role: str = Query("general"),
    db: AsyncSession = Depends(get_db),
):
    """Auto-generate access revocation list for a checklist."""
    items = await generate_revocation_list(db, checklist_id, role)
    return [RevocationResponse.model_validate(r) for r in items]


@router.get("/checklists/{checklist_id}/revocations", tags=["Access"])
async def list_revocations(
    checklist_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """List access revocations for a checklist."""
    repo = RevocationRepository(db)
    items = await repo.list_by_checklist(checklist_id)
    return [RevocationResponse.model_validate(r) for r in items]


@router.post("/access-revocations/{revocation_id}/revoke", tags=["Access"])
async def revoke_access(
    revocation_id: UUID,
    revoked_by: str = Query("system"),
    db: AsyncSession = Depends(get_db),
):
    """Revoke a single system access."""
    result = await revoke_single(db, revocation_id, revoked_by)
    if not result:
        raise HTTPException(404, "Revocation record not found")
    return RevocationResponse.model_validate(result)


@router.post("/checklists/{checklist_id}/revoke-all", tags=["Access"])
async def revoke_all_access(
    checklist_id: UUID,
    revoked_by: str = Query("system"),
    db: AsyncSession = Depends(get_db),
):
    """Revoke all pending access for a checklist."""
    count = await revoke_all_for_checklist(db, checklist_id, revoked_by)
    return {"revoked_count": count, "revoked_by": revoked_by}


@router.get("/checklists/{checklist_id}/audit-trail", tags=["Access"])
async def get_revocation_audit(
    checklist_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Get audit trail of all revocations for a checklist."""
    items = await get_audit_trail(db, checklist_id)
    return [RevocationResponse.model_validate(r) for r in items]


# ══════════════════════════════════════════════════════════════════════════════
# P1.5: Exit Interviews
# ══════════════════════════════════════════════════════════════════════════════

@router.get("/exit-interviews", tags=["Exit Interviews"])
async def list_exit_interviews(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """List all exit interviews."""
    repo = ExitInterviewRepository(db)
    items, total = await repo.list_all(limit=page_size, offset=(page - 1) * page_size)
    return _paginated(
        [ExitInterviewResponse.model_validate(i) for i in items], total, page, page_size
    )


@router.post("/exit-interviews", response_model=ExitInterviewResponse, status_code=201, tags=["Exit Interviews"])
async def create_exit_interview(
    data: ExitInterviewCreate,
    db: AsyncSession = Depends(get_db),
):
    """Schedule a new exit interview."""
    from app.models.offboarding import ExitInterview
    repo = ExitInterviewRepository(db)
    interview = ExitInterview(**data.model_dump())
    interview = await repo.create(interview)
    return ExitInterviewResponse.model_validate(interview)


@router.put("/exit-interviews/{interview_id}", response_model=ExitInterviewResponse, tags=["Exit Interviews"])
async def update_exit_interview(
    interview_id: UUID,
    data: ExitInterviewUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update an exit interview (add transcript, change status)."""
    repo = ExitInterviewRepository(db)
    interview = await repo.get_by_id(interview_id)
    if not interview:
        raise HTTPException(404, "Interview not found")
    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(interview, key, val)
    await db.commit()
    await db.refresh(interview)
    return ExitInterviewResponse.model_validate(interview)


@router.delete("/exit-interviews/{interview_id}", status_code=204, tags=["Exit Interviews"])
async def delete_exit_interview(
    interview_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Delete an exit interview."""
    repo = ExitInterviewRepository(db)
    interview = await repo.get_by_id(interview_id)
    if not interview:
        raise HTTPException(404, "Interview not found")
    await repo.delete(interview)
    return None


# ══════════════════════════════════════════════════════════════════════════════
# P1.6: Knowledge Transfer
# ══════════════════════════════════════════════════════════════════════════════

@router.get("/knowledge-transfers", tags=["Knowledge Transfer"])
async def list_knowledge_transfers(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """List all knowledge transfer records."""
    repo = KnowledgeTransferRepository(db)
    items, total = await repo.list_all(limit=page_size, offset=(page - 1) * page_size)
    return _paginated(
        [KnowledgeTransferResponse.model_validate(k) for k in items], total, page, page_size
    )


@router.post("/knowledge-transfers", response_model=KnowledgeTransferResponse, status_code=201, tags=["Knowledge Transfer"])
async def create_knowledge_transfer(
    data: KnowledgeTransferCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a knowledge transfer / handover document."""
    from app.models.offboarding import KnowledgeTransfer
    repo = KnowledgeTransferRepository(db)
    transfer = KnowledgeTransfer(**data.model_dump())
    transfer = await repo.create(transfer)
    return KnowledgeTransferResponse.model_validate(transfer)


@router.put("/knowledge-transfers/{transfer_id}", response_model=KnowledgeTransferResponse, tags=["Knowledge Transfer"])
async def update_knowledge_transfer(
    transfer_id: UUID,
    data: KnowledgeTransferUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update a knowledge transfer record."""
    repo = KnowledgeTransferRepository(db)
    transfer = await repo.get_by_id(transfer_id)
    if not transfer:
        raise HTTPException(404, "Knowledge transfer not found")
    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(transfer, key, val)
    await db.commit()
    await db.refresh(transfer)
    return KnowledgeTransferResponse.model_validate(transfer)


@router.delete("/knowledge-transfers/{transfer_id}", status_code=204, tags=["Knowledge Transfer"])
async def delete_knowledge_transfer(
    transfer_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Delete a knowledge transfer record."""
    repo = KnowledgeTransferRepository(db)
    transfer = await repo.get_by_id(transfer_id)
    if not transfer:
        raise HTTPException(404, "Knowledge transfer not found")
    await repo.delete(transfer)
    return None


# ══════════════════════════════════════════════════════════════════════════════
# P1.7: Alumni Network
# ══════════════════════════════════════════════════════════════════════════════

@router.get("/alumni", tags=["Alumni"])
async def list_alumni(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """List all alumni records."""
    repo = AlumniRepository(db)
    items, total = await repo.list_all(limit=page_size, offset=(page - 1) * page_size)
    return _paginated(
        [AlumniResponse.model_validate(a) for a in items], total, page, page_size
    )


@router.post("/alumni", response_model=AlumniResponse, status_code=201, tags=["Alumni"])
async def create_alumni(
    data: AlumniCreate,
    db: AsyncSession = Depends(get_db),
):
    """Add an employee to the alumni network."""
    from app.models.offboarding import AlumniRecord
    repo = AlumniRepository(db)
    alumni = AlumniRecord(**data.model_dump())
    alumni = await repo.create(alumni)
    return AlumniResponse.model_validate(alumni)


@router.put("/alumni/{alumni_id}", response_model=AlumniResponse, tags=["Alumni"])
async def update_alumni(
    alumni_id: UUID,
    data: AlumniUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update an alumni record."""
    repo = AlumniRepository(db)
    alumni = await repo.get_by_id(alumni_id)
    if not alumni:
        raise HTTPException(404, "Alumni record not found")
    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(alumni, key, val)
    await db.commit()
    await db.refresh(alumni)
    return AlumniResponse.model_validate(alumni)


@router.delete("/alumni/{alumni_id}", status_code=204, tags=["Alumni"])
async def delete_alumni(
    alumni_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Delete an alumni record."""
    repo = AlumniRepository(db)
    alumni = await repo.get_by_id(alumni_id)
    if not alumni:
        raise HTTPException(404, "Alumni record not found")
    await repo.delete(alumni)
    return None


# ══════════════════════════════════════════════════════════════════════════════
# P1.8: Final Pay Calculator
# ══════════════════════════════════════════════════════════════════════════════

@router.get("/final-pay", tags=["Final Pay"])
async def list_final_pay(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """List all final pay calculations."""
    repo = FinalPayRepository(db)
    items, total = await repo.list_all(limit=page_size, offset=(page - 1) * page_size)
    return _paginated(
        [FinalPayResponse.model_validate(f) for f in items], total, page, page_size
    )


@router.post("/final-pay", response_model=FinalPayResponse, status_code=201, tags=["Final Pay"])
async def create_final_pay(
    data: FinalPayCreate,
    db: AsyncSession = Depends(get_db),
):
    """Calculate and store final pay for an employee."""
    from app.models.offboarding import FinalPayCalculation

    # Calculate components
    weekly_salary = data.base_salary / 52.0 if data.base_salary > 0 else 0
    severance = weekly_salary * data.severance_weeks
    pto_payout = data.unused_pto_hours * data.pto_payout_rate
    total = pto_payout + severance + data.bonus_amount - data.deductions

    calc = FinalPayCalculation(
        employee_name=data.employee_name,
        employee_email=data.employee_email,
        last_day=data.last_day,
        base_salary=data.base_salary,
        unused_pto_hours=data.unused_pto_hours,
        pto_payout_rate=data.pto_payout_rate,
        severance_weeks=data.severance_weeks,
        severance_amount=round(severance, 2),
        bonus_amount=data.bonus_amount,
        deductions=data.deductions,
        total_final_pay=round(max(total, 0), 2),
        checklist_id=data.checklist_id,
    )
    repo = FinalPayRepository(db)
    calc = await repo.create(calc)
    return FinalPayResponse.model_validate(calc)


@router.put("/final-pay/{pay_id}", response_model=FinalPayResponse, tags=["Final Pay"])
async def update_final_pay(
    pay_id: UUID,
    data: FinalPayUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Recalculate and update a final pay record."""
    repo = FinalPayRepository(db)
    calc = await repo.get_by_id(pay_id)
    if not calc:
        raise HTTPException(404, "Final pay calculation not found")

    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(calc, key, val)

    # Recalculate
    weekly_salary = calc.base_salary / 52.0 if calc.base_salary > 0 else 0
    calc.severance_amount = round(weekly_salary * calc.severance_weeks, 2)
    pto_payout = calc.unused_pto_hours * calc.pto_payout_rate
    calc.total_final_pay = round(
        max(pto_payout + calc.severance_amount + calc.bonus_amount - calc.deductions, 0), 2
    )

    await db.commit()
    await db.refresh(calc)
    return FinalPayResponse.model_validate(calc)


@router.delete("/final-pay/{pay_id}", status_code=204, tags=["Final Pay"])
async def delete_final_pay(
    pay_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Delete a final pay calculation."""
    repo = FinalPayRepository(db)
    calc = await repo.get_by_id(pay_id)
    if not calc:
        raise HTTPException(404, "Final pay record not found")
    await repo.delete(calc)
    return None


# ══════════════════════════════════════════════════════════════════════════════
# Dashboard
# ══════════════════════════════════════════════════════════════════════════════

@router.get("/dashboard", response_model=DashboardStats, tags=["Dashboard"])
async def get_dashboard(
    db: AsyncSession = Depends(get_db),
):
    """Get dashboard summary stats."""
    checklist_repo = ChecklistRepository(db)
    alumni_repo = AlumniRepository(db)

    all_checklists, total_checklists = await checklist_repo.list_all(limit=1000, offset=0)

    active = sum(1 for c in all_checklists if c.status.value in ("pending", "in_progress"))
    completed = sum(1 for c in all_checklists if c.status.value == "completed")

    recent = sorted(all_checklists, key=lambda c: c.created_at, reverse=True)[:5]

    return DashboardStats(
        total_checklists=total_checklists,
        active_checklists=active,
        completed_checklists=completed,
        total_assets_pending=await get_pending_returns_count(db),
        total_revocations_pending=await get_pending_revocations_count(db),
        pending_interviews=0,  # simplified
        alumni_count=await alumni_repo.count(),
        recent_checklists=[ChecklistResponse.model_validate(c) for c in recent],
    )
