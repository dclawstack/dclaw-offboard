"""Integration Hub service — v1.3.

API-first connector orchestration for HRIS, SSO, Payroll, MDM, Communication tools.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.offboarding_v13 import (
    Integration,
    IntegrationAction,
    IntegrationCategory,
    IntegrationStatus,
)

# ── Pre-built connector catalog ──────────────────────────────────────────────

CONNECTOR_CATALOG: list[dict] = [
    # HRIS
    {"name": "Workday HRIS", "provider": "workday", "category": IntegrationCategory.hris, "auth_type": "oauth2"},
    {"name": "BambooHR", "provider": "bamboohr", "category": IntegrationCategory.hris, "auth_type": "api_key"},
    {"name": "ADP Workforce", "provider": "adp", "category": IntegrationCategory.hris, "auth_type": "oauth2"},
    # SSO / Identity
    {"name": "Okta SSO", "provider": "okta", "category": IntegrationCategory.sso, "auth_type": "oauth2"},
    {"name": "Azure AD / Entra ID", "provider": "azure_ad", "category": IntegrationCategory.sso, "auth_type": "saml"},
    {"name": "Google Workspace", "provider": "google", "category": IntegrationCategory.sso, "auth_type": "oauth2"},
    # Payroll
    {"name": "ADP Payroll", "provider": "adp_payroll", "category": IntegrationCategory.payroll, "auth_type": "oauth2"},
    {"name": "Gusto", "provider": "gusto", "category": IntegrationCategory.payroll, "auth_type": "oauth2"},
    {"name": "QuickBooks Payroll", "provider": "quickbooks", "category": IntegrationCategory.payroll, "auth_type": "oauth2"},
    {"name": "Xero", "provider": "xero", "category": IntegrationCategory.payroll, "auth_type": "oauth2"},
    # MDM
    {"name": "Jamf Pro", "provider": "jamf", "category": IntegrationCategory.mdm, "auth_type": "api_key"},
    {"name": "Microsoft Intune", "provider": "intune", "category": IntegrationCategory.mdm, "auth_type": "oauth2"},
    {"name": "Kandji", "provider": "kandji", "category": IntegrationCategory.mdm, "auth_type": "api_key"},
    # Communication
    {"name": "Slack", "provider": "slack", "category": IntegrationCategory.communication, "auth_type": "oauth2"},
    {"name": "Microsoft Teams", "provider": "teams", "category": IntegrationCategory.communication, "auth_type": "oauth2"},
    {"name": "Zoom", "provider": "zoom", "category": IntegrationCategory.communication, "auth_type": "oauth2"},
]


async def seed_default_integrations(db: AsyncSession) -> int:
    """Seed the default connector catalog into the database (idempotent)."""
    count = 0
    for connector in CONNECTOR_CATALOG:
        existing = await db.execute(
            select(Integration).where(Integration.provider == connector["provider"])
        )
        if existing.scalar_one_or_none() is None:
            integration = Integration(
                name=connector["name"],
                provider=connector["provider"],
                category=connector["category"],
                auth_type=connector["auth_type"],
                status=IntegrationStatus.pending,
            )
            db.add(integration)
            count += 1
    if count > 0:
        await db.commit()
    return count


async def get_integration_overview(db: AsyncSession) -> dict:
    """Get integration hub dashboard overview."""
    total_result = await db.execute(
        select(func.count()).select_from(Integration)
    )
    total = total_result.scalar() or 0

    connected_result = await db.execute(
        select(func.count()).select_from(Integration).where(
            Integration.status == IntegrationStatus.connected
        )
    )
    connected = connected_result.scalar() or 0

    error_result = await db.execute(
        select(func.count()).select_from(Integration).where(
            Integration.status == IntegrationStatus.error
        )
    )
    errors = error_result.scalar() or 0

    pending_result = await db.execute(
        select(func.count()).select_from(IntegrationAction).where(
            IntegrationAction.status == "pending"
        )
    )
    pending_actions = pending_result.scalar() or 0

    return {
        "total_integrations": total,
        "connected_count": connected,
        "error_count": errors,
        "pending_actions": pending_actions,
    }


async def simulate_sync(
    db: AsyncSession, integration_id: UUID
) -> dict:
    """Simulate syncing with an integration (in production: real API calls)."""
    result = await db.execute(
        select(Integration).where(Integration.id == integration_id)
    )
    integration = result.scalar_one_or_none()
    if not integration:
        return {"status": "error", "message": "Integration not found"}

    integration.status = IntegrationStatus.connected
    integration.last_sync_at = datetime.utcnow()
    integration.sync_status = "success"

    # Log a sync action
    action = IntegrationAction(
        integration_id=integration_id,
        action_type="sync",
        target=integration.provider,
        status="success",
        executed_at=datetime.utcnow(),
        duration_ms=850,
        result_detail=f"Successfully synced with {integration.name}",
    )
    db.add(action)
    await db.commit()
    await db.refresh(integration)

    return {
        "integration_id": integration_id,
        "provider": integration.provider,
        "status": "success",
        "actions_performed": 1,
        "errors": [],
        "synced_at": integration.last_sync_at,
    }


async def simulate_offboard_actions(
    db: AsyncSession, integration_id: UUID, employee_email: str
) -> list[dict]:
    """Simulate offboarding actions through a connected integration."""
    result = await db.execute(
        select(Integration).where(Integration.id == integration_id)
    )
    integration = result.scalar_one_or_none()
    if not integration:
        return [{"status": "error", "message": "Integration not found"}]

    actions_performed = []
    action_types = {
        IntegrationCategory.sso: ["revoke_sso", "deactivate_account"],
        IntegrationCategory.communication: ["deactivate_account", "suspend_access"],
        IntegrationCategory.payroll: ["calculate_final_pay", "generate_paystub"],
        IntegrationCategory.mdm: ["remote_wipe_device", "remove_device_profile"],
        IntegrationCategory.hris: ["mark_terminated", "export_records"],
    }

    for action_type in action_types.get(integration.category, ["revoke_access"]):
        action = IntegrationAction(
            integration_id=integration_id,
            action_type=action_type,
            target=employee_email,
            status="success",
            executed_at=datetime.utcnow(),
            duration_ms=350,
            result_detail=f"Successfully executed {action_type} for {employee_email}",
        )
        db.add(action)
        actions_performed.append({
            "action": action_type,
            "status": "success",
            "target": employee_email,
            "integration": integration.provider,
        })

    await db.commit()
    return actions_performed
