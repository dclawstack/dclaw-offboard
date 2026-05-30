"""Team Transition & Coverage service — v1.3.

Seamless team transitions, auto-reassignment, and coverage planning.
"""

from datetime import date
from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.offboarding_v13 import (
    CoverageItem,
    CoverageStatus,
    TeamTransition,
)


# ── Default coverage templates by department ─────────────────────────────────

DEPARTMENT_COVERAGE_TEMPLATES: dict[str, list[dict]] = {
    "engineering": [
        {"responsibility": "Code review responsibilities", "category": "projects"},
        {"responsibility": "On-call rotation coverage", "category": "projects"},
        {"responsibility": "Sprint planning participation", "category": "meetings"},
        {"responsibility": "Architecture decision records", "category": "projects"},
        {"responsibility": "CI/CD pipeline ownership", "category": "tools"},
    ],
    "sales": [
        {"responsibility": "Active deal pipeline transfer", "category": "projects"},
        {"responsibility": "Key account relationship handoff", "category": "clients"},
        {"responsibility": "CRM ownership transfer", "category": "tools"},
        {"responsibility": "Sales forecast updates", "category": "meetings"},
    ],
    "hr": [
        {"responsibility": "Active employee relations cases", "category": "projects"},
        {"responsibility": "Benefits administration", "category": "projects"},
        {"responsibility": "Onboarding session facilitation", "category": "meetings"},
        {"responsibility": "Compliance audit preparation", "category": "projects"},
    ],
}

DEFAULT_COVERAGE = [
    {"responsibility": "Direct report management", "category": "direct_reports"},
    {"responsibility": "Active project ownership", "category": "projects"},
    {"responsibility": "Recurring meeting attendance", "category": "meetings"},
    {"responsibility": "Vendor/partner relationships", "category": "clients"},
    {"responsibility": "Tool and system administration", "category": "tools"},
]


async def create_transition_with_coverage(
    db: AsyncSession,
    employee_name: str,
    employee_email: str,
    department: str,
    role: str,
    last_day: date,
    successor_name: Optional[str] = None,
    successor_email: Optional[str] = None,
) -> TeamTransition:
    """Create a team transition plan with auto-generated coverage items."""
    transition = TeamTransition(
        departing_employee_name=employee_name,
        departing_employee_email=employee_email,
        department=department,
        role=role,
        last_day=last_day,
        successor_name=successor_name,
        successor_email=successor_email,
        status="in_progress",
    )
    db.add(transition)
    await db.flush()

    template = DEPARTMENT_COVERAGE_TEMPLATES.get(
        department.lower(), DEFAULT_COVERAGE
    )

    for item in template:
        coverage = CoverageItem(
            transition_id=transition.id,
            responsibility=item["responsibility"],
            category=item["category"],
            assigned_to_name=successor_name or "TBD",
            assigned_to_email=successor_email or "pending@company.com",
            start_date=last_day,
            status=CoverageStatus.pending,
            is_permanent=True,
        )
        db.add(coverage)

    await db.commit()
    await db.refresh(transition)
    return transition
