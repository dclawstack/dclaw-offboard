"""Access Revocation Automation — P0.4.

One-click revocation of system access with audit trail.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.offboarding import AccessRevocation, RevocationStatus


# ── Standard systems to revoke by role ───────────────────────────────────────

ROLE_SYSTEMS: dict[str, list[dict]] = {
    "engineering": [
        {"system_name": "GitHub Enterprise", "system_type": "saas"},
        {"system_name": "GitLab", "system_type": "saas"},
        {"system_name": "AWS IAM", "system_type": "cloud"},
        {"system_name": "GCP IAM", "system_type": "cloud"},
        {"system_name": "Docker Hub", "system_type": "saas"},
        {"system_name": "Jira / Confluence", "system_type": "saas"},
        {"system_name": "CI/CD Pipeline", "system_type": "saas"},
        {"system_name": "Google Workspace (Email)", "system_type": "email"},
        {"system_name": "Slack", "system_type": "saas"},
        {"system_name": "VPN Access", "system_type": "vpn"},
        {"system_name": "Building Access", "system_type": "physical"},
    ],
    "sales": [
        {"system_name": "Salesforce CRM", "system_type": "saas"},
        {"system_name": "Outreach.io", "system_type": "saas"},
        {"system_name": "LinkedIn Sales Navigator", "system_type": "saas"},
        {"system_name": "Google Workspace (Email)", "system_type": "email"},
        {"system_name": "Slack", "system_type": "saas"},
        {"system_name": "VPN Access", "system_type": "vpn"},
        {"system_name": "Building Access", "system_type": "physical"},
    ],
}

DEFAULT_SYSTEMS = [
    {"system_name": "Google Workspace (Email)", "system_type": "email"},
    {"system_name": "Slack / Teams", "system_type": "saas"},
    {"system_name": "VPN Access", "system_type": "vpn"},
    {"system_name": "Building Access", "system_type": "physical"},
    {"system_name": "HRIS / Payroll", "system_type": "saas"},
]


async def generate_revocation_list(
    db: AsyncSession, checklist_id: UUID, employee_role: str
) -> list[AccessRevocation]:
    """Auto-generate access revocation checklist based on role."""
    systems = ROLE_SYSTEMS.get(employee_role.lower(), DEFAULT_SYSTEMS)

    revocations = []
    for sys_info in systems:
        revocation = AccessRevocation(
            checklist_id=checklist_id,
            system_name=sys_info["system_name"],
            system_type=sys_info["system_type"],
            status=RevocationStatus.pending,
        )
        db.add(revocation)
        revocations.append(revocation)

    await db.commit()
    for r in revocations:
        await db.refresh(r)
    return revocations


async def revoke_single(
    db: AsyncSession, revocation_id: UUID, revoked_by: str
) -> Optional[AccessRevocation]:
    """Revoke a single system access."""
    result = await db.execute(
        select(AccessRevocation).where(AccessRevocation.id == revocation_id)
    )
    revocation = result.scalar_one_or_none()
    if not revocation:
        return None

    revocation.status = RevocationStatus.completed
    revocation.revoked_at = datetime.utcnow()
    revocation.revoked_by = revoked_by

    await db.commit()
    await db.refresh(revocation)
    return revocation


async def revoke_all_for_checklist(
    db: AsyncSession, checklist_id: UUID, revoked_by: str
) -> int:
    """Revoke all pending access for a checklist. Returns count of revoked."""
    result = await db.execute(
        select(AccessRevocation).where(
            AccessRevocation.checklist_id == checklist_id,
            AccessRevocation.status == RevocationStatus.pending,
        )
    )
    pending = list(result.scalars().all())

    now = datetime.utcnow()
    for r in pending:
        r.status = RevocationStatus.completed
        r.revoked_at = now
        r.revoked_by = revoked_by

    await db.commit()
    return len(pending)


async def get_pending_revocations_count(db: AsyncSession) -> int:
    """Count pending revocations across all checklists."""
    result = await db.execute(
        select(func.count()).select_from(AccessRevocation).where(
            AccessRevocation.status == RevocationStatus.pending
        )
    )
    return result.scalar() or 0


async def get_audit_trail(
    db: AsyncSession, checklist_id: UUID
) -> list[AccessRevocation]:
    """Get full audit trail of revocations for a checklist."""
    result = await db.execute(
        select(AccessRevocation).where(
            AccessRevocation.checklist_id == checklist_id
        ).order_by(AccessRevocation.revoked_at.desc())
    )
    return list(result.scalars().all())
