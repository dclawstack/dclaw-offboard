"""Offboarding Workflow Engine — P0.2.

Handles structured offboarding journeys with role-based task assignments.
"""

from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.offboarding import (
    ChecklistStatus,
    OffboardingChecklist,
    OffboardingTask,
    TaskCategory,
    TaskStatus,
)
from app.schemas.offboarding import ChecklistCreate

# ── Default task templates by department ─────────────────────────────────────

DEPARTMENT_TEMPLATES: dict[str, list[dict]] = {
    "engineering": [
        {"title": "Revoke GitHub / GitLab access", "category": "it", "sort": 1},
        {"title": "Revoke CI/CD pipeline access", "category": "it", "sort": 2},
        {"title": "Collect laptop and peripherals", "category": "it", "sort": 3},
        {"title": "Revoke cloud provider access (AWS/GCP/Azure)", "category": "it", "sort": 4},
        {"title": "Document active projects and status", "category": "manager", "sort": 5},
        {"title": "Transfer code ownership and repos", "category": "manager", "sort": 6},
        {"title": "Knowledge transfer session with successor", "category": "manager", "sort": 7},
        {"title": "Revoke Slack / Teams access", "category": "it", "sort": 8},
        {"title": "Process final expense reports", "category": "finance", "sort": 9},
        {"title": "Schedule exit interview", "category": "hr", "sort": 10},
    ],
    "sales": [
        {"title": "Revoke CRM access", "category": "it", "sort": 1},
        {"title": "Transfer accounts to new owner", "category": "manager", "sort": 2},
        {"title": "Notify key clients of transition", "category": "manager", "sort": 3},
        {"title": "Collect laptop and phone", "category": "it", "sort": 4},
        {"title": "Revoke email and calendar access", "category": "it", "sort": 5},
        {"title": "Calculate outstanding commissions", "category": "finance", "sort": 6},
        {"title": "Revoke Slack / Teams access", "category": "it", "sort": 7},
        {"title": "Schedule exit interview", "category": "hr", "sort": 8},
    ],
    "hr": [
        {"title": "Revoke HRIS access", "category": "it", "sort": 1},
        {"title": "Revoke payroll system access", "category": "it", "sort": 2},
        {"title": "Transfer employee relations cases", "category": "manager", "sort": 3},
        {"title": "Collect laptop and assets", "category": "it", "sort": 4},
        {"title": "Revoke email access", "category": "it", "sort": 5},
        {"title": "Revoke Slack / Teams access", "category": "it", "sort": 6},
        {"title": "Schedule exit interview", "category": "hr", "sort": 7},
    ],
}

DEFAULT_TEMPLATE = [
    {"title": "Revoke email access", "category": "it", "sort": 1},
    {"title": "Revoke Slack / Teams access", "category": "it", "sort": 2},
    {"title": "Collect laptop and phone", "category": "it", "sort": 3},
    {"title": "Collect building access card", "category": "facilities", "sort": 4},
    {"title": "Revoke VPN access", "category": "it", "sort": 5},
    {"title": "Process final expense reports", "category": "finance", "sort": 6},
    {"title": "Calculate final pay and PTO payout", "category": "finance", "sort": 7},
    {"title": "Benefits continuation packet", "category": "hr", "sort": 8},
    {"title": "Schedule exit interview", "category": "hr", "sort": 9},
    {"title": "Knowledge transfer documentation", "category": "manager", "sort": 10},
    {"title": "Team announcement and comms", "category": "manager", "sort": 11},
]


async def create_checklist_with_tasks(
    db: AsyncSession, data: ChecklistCreate
) -> OffboardingChecklist:
    """Create an offboarding checklist with auto-generated tasks based on department."""
    checklist = OffboardingChecklist(
        employee_name=data.employee_name,
        employee_email=data.employee_email,
        employee_role=data.employee_role,
        department=data.department,
        last_day=data.last_day,
        status=ChecklistStatus.in_progress,
        notes=data.notes,
    )
    db.add(checklist)
    await db.flush()

    template = DEPARTMENT_TEMPLATES.get(
        data.department.lower(), DEFAULT_TEMPLATE
    )

    for task_data in template:
        task = OffboardingTask(
            checklist_id=checklist.id,
            title=task_data["title"],
            category=TaskCategory(task_data["category"]),
            sort_order=task_data["sort"],
            status=TaskStatus.pending,
        )
        db.add(task)

    await db.commit()
    await db.refresh(checklist)
    return checklist
