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
from app.models.offboarding_v13 import (  # noqa: F401 — v1.3 features
    ComplianceReport,
    CoverageItem,
    FlightRiskAlert,
    Integration,
    IntegrationAction,
    NonCompeteTracker,
    RiskAssessment,
    SentimentPulse,
    TeamTransition,
)

__all__ = ["Base"]
