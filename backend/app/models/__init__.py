"""Models package — imports all domain models for alembic auto-detection."""

from app.models.base import Base
from app.models.offboarding import (  # noqa: F401 — required for alembic
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

__all__ = ["Base"]
