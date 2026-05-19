"""Asset Recovery & Inventory — P0.3.

Tracks company assets and manages the recovery process during offboarding.
"""

from typing import Optional
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.offboarding import Asset, AssetCondition, AssetReturn


# ── Standard asset catalog by role ───────────────────────────────────────────

ROLE_ASSET_CATALOG: dict[str, list[dict]] = {
    "engineering": [
        {"name": "MacBook Pro 16\"", "asset_type": "laptop"},
        {"name": "External Monitor", "asset_type": "peripheral"},
        {"name": "YubiKey", "asset_type": "security_key"},
        {"name": "iPhone (Corporate)", "asset_type": "phone"},
    ],
    "sales": [
        {"name": "MacBook Air", "asset_type": "laptop"},
        {"name": "iPhone (Corporate)", "asset_type": "phone"},
        {"name": "Corporate Credit Card", "asset_type": "card"},
    ],
    "hr": [
        {"name": "ThinkPad Laptop", "asset_type": "laptop"},
        {"name": "Building Access Card", "asset_type": "card"},
    ],
}

DEFAULT_ASSETS = [
    {"name": "Company Laptop", "asset_type": "laptop"},
    {"name": "Building Access Card", "asset_type": "card"},
]


async def generate_recovery_list(
    db: AsyncSession, checklist_id: UUID, employee_role: str, employee_name: str
) -> list[AssetReturn]:
    """Auto-generate asset recovery list based on employee role."""
    catalog = ROLE_ASSET_CATALOG.get(employee_role.lower(), DEFAULT_ASSETS)

    returns = []
    for item in catalog:
        asset_return = AssetReturn(
            checklist_id=checklist_id,
            asset_name=item["name"],
            asset_type=item["asset_type"],
            returned=False,
        )
        db.add(asset_return)
        returns.append(asset_return)

    await db.commit()
    for r in returns:
        await db.refresh(r)
    return returns


async def get_pending_returns_count(db: AsyncSession) -> int:
    """Count assets still pending return across all checklists."""
    result = await db.execute(
        select(func.count()).select_from(AssetReturn).where(
            AssetReturn.returned == False  # noqa: E712
        )
    )
    return result.scalar() or 0


async def mark_returned(
    db: AsyncSession, return_id: UUID, condition: Optional[str] = None, notes: Optional[str] = None
) -> Optional[AssetReturn]:
    """Mark an asset as returned with condition assessment."""
    result = await db.execute(
        select(AssetReturn).where(AssetReturn.id == return_id)
    )
    asset_return = result.scalar_one_or_none()
    if not asset_return:
        return None

    asset_return.returned = True
    if condition:
        asset_return.condition = AssetCondition(condition)
    if notes:
        asset_return.notes = notes
    asset_return.return_date = __import__("datetime").date.today()

    await db.commit()
    await db.refresh(asset_return)
    return asset_return
