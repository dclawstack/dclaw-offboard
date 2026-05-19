"""Repository layer for all offboarding domain models."""

from uuid import UUID

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.offboarding import (
    AccessRevocation,
    AlumniRecord,
    Asset,
    AssetReturn,
    ExitInterview,
    FinalPayCalculation,
    KnowledgeTransfer,
    OffboardingChecklist,
    OffboardingTask,
)
from app.repositories.base_repo import BaseRepository


# ── Checklists ───────────────────────────────────────────────────────────────

class ChecklistRepository(BaseRepository[OffboardingChecklist]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, OffboardingChecklist)

    async def list_with_tasks(self, limit: int = 20, offset: int = 0) -> tuple[list[OffboardingChecklist], int]:
        result = await self.db.execute(
            select(OffboardingChecklist).limit(limit).offset(offset)
        )
        items = list(result.scalars().all())
        count_result = await self.db.execute(
            select(func.count()).select_from(OffboardingChecklist)
        )
        return items, count_result.scalar() or 0

    async def get_with_all(self, checklist_id: UUID) -> OffboardingChecklist | None:
        result = await self.db.execute(
            select(OffboardingChecklist).where(OffboardingChecklist.id == checklist_id)
        )
        return result.scalar_one_or_none()

    async def get_completion_percent(self, checklist_id: UUID) -> float:
        total_result = await self.db.execute(
            select(func.count()).select_from(OffboardingTask).where(
                OffboardingTask.checklist_id == checklist_id
            )
        )
        total = total_result.scalar() or 0
        if total == 0:
            return 0.0
        completed_result = await self.db.execute(
            select(func.count()).select_from(OffboardingTask).where(
                OffboardingTask.checklist_id == checklist_id,
                OffboardingTask.status == "completed",
            )
        )
        completed = completed_result.scalar() or 0
        return round((completed / total) * 100, 1)


# ── Tasks ────────────────────────────────────────────────────────────────────

class TaskRepository(BaseRepository[OffboardingTask]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, OffboardingTask)

    async def list_by_checklist(self, checklist_id: UUID) -> list[OffboardingTask]:
        result = await self.db.execute(
            select(OffboardingTask)
            .where(OffboardingTask.checklist_id == checklist_id)
            .order_by(OffboardingTask.sort_order)
        )
        return list(result.scalars().all())


# ── Assets ───────────────────────────────────────────────────────────────────

class AssetRepository(BaseRepository[Asset]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Asset)


class AssetReturnRepository(BaseRepository[AssetReturn]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, AssetReturn)

    async def list_by_checklist(self, checklist_id: UUID) -> list[AssetReturn]:
        result = await self.db.execute(
            select(AssetReturn).where(AssetReturn.checklist_id == checklist_id)
        )
        return list(result.scalars().all())


# ── Access Revocations ───────────────────────────────────────────────────────

class RevocationRepository(BaseRepository[AccessRevocation]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, AccessRevocation)

    async def list_by_checklist(self, checklist_id: UUID) -> list[AccessRevocation]:
        result = await self.db.execute(
            select(AccessRevocation).where(AccessRevocation.checklist_id == checklist_id)
        )
        return list(result.scalars().all())


# ── Exit Interviews ──────────────────────────────────────────────────────────

class ExitInterviewRepository(BaseRepository[ExitInterview]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, ExitInterview)


# ── Knowledge Transfer ───────────────────────────────────────────────────────

class KnowledgeTransferRepository(BaseRepository[KnowledgeTransfer]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, KnowledgeTransfer)


# ── Alumni ───────────────────────────────────────────────────────────────────

class AlumniRepository(BaseRepository[AlumniRecord]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, AlumniRecord)


# ── Final Pay ────────────────────────────────────────────────────────────────

class FinalPayRepository(BaseRepository[FinalPayCalculation]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, FinalPayCalculation)
