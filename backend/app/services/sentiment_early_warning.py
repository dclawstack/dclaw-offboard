"""Employee Sentiment & Early Warning service — v1.3.

Pulse surveys, sentiment analysis, and flight risk prediction.
"""

import random
from datetime import date, datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.offboarding_v13 import (
    FlightRisk,
    FlightRiskAlert,
    SentimentCategory,
    SentimentPulse,
)

# ── Sentiment signals for flight risk ────────────────────────────────────────

FLIGHT_RISK_SIGNALS = [
    "Decreased engagement in team meetings",
    "Reduced communication frequency",
    "Decline in code commit / output volume",
    "LinkedIn profile recently updated",
    "Pattern of Monday/Friday absences",
    "Declined participation in long-term planning",
    "PTO balance approaching zero (burning leave)",
    "Removal of company from social media profiles",
    "Decreased response time to messages",
    "Opted out of team social events",
]

RETENTION_RECOMMENDATIONS = {
    "compensation": [
        "Schedule a compensation review",
        "Explore retention bonus options",
        "Review equity refresh eligibility",
    ],
    "growth": [
        "Discuss career development path",
        "Identify stretch assignment opportunities",
        "Arrange mentorship with senior leader",
    ],
    "burnout": [
        "Discuss workload redistribution",
        "Offer mental health / wellness resources",
        "Suggest temporary reduced schedule",
    ],
    "management": [
        "Facilitate skip-level 1:1 with skip manager",
        "Review team dynamics and relationships",
        "Consider team transfer options",
    ],
    "culture": [
        "Discuss team belonging and inclusion",
        "Identify cultural alignment opportunities",
        "Connect with ERG / affinity groups",
    ],
}


async def create_pulse_survey(
    db: AsyncSession,
    title: str,
    category: str,
    department: Optional[str] = None,
    team_size: Optional[int] = None,
    survey_date: Optional[date] = None,
) -> SentimentPulse:
    """Create and analyze a sentiment pulse survey.

    In production: deploys anonymous survey, collects results, runs AI analysis.
    """
    # Simulate survey results
    seed = (hash(title + (department or "")) % 50) / 100  # 0.0 - 0.5 base
    avg_score = 2.5 + seed * 5  # 2.5 - 5.0 range

    if avg_score >= 3.8:
        sentiment_label = "positive"
    elif avg_score >= 2.8:
        sentiment_label = "neutral"
    else:
        sentiment_label = "negative"

    themes = {
        SentimentCategory.engagement: ["Team collaboration", "Mission alignment", "Autonomy"],
        SentimentCategory.burnout: ["Workload balance", "Stress levels", "Recovery time"],
        SentimentCategory.satisfaction: ["Role clarity", "Tools & resources", "Recognition"],
        SentimentCategory.culture: ["Inclusion", "Psychological safety", "Values alignment"],
        SentimentCategory.management: ["Manager relationship", "Feedback quality", "Support"],
        SentimentCategory.growth: ["Learning opportunities", "Career path", "Promotion velocity"],
        SentimentCategory.compensation: ["Salary competitiveness", "Benefits satisfaction", "Equity value"],
    }

    # Determine trend
    trends = ["improving", "stable", "declining"]
    trend_weights = [0.3, 0.5, 0.2]
    if sentiment_label == "negative":
        trend_weights = [0.1, 0.3, 0.6]

    trend_direction = random.choices(trends, weights=trend_weights, k=1)[0]
    responses_count = max(5, team_size or 0) + random.randint(0, 15)

    pulse = SentimentPulse(
        title=title,
        category=SentimentCategory(category),
        department=department,
        team_size=team_size,
        responses_count=responses_count,
        avg_score=round(avg_score, 1),
        sentiment_label=sentiment_label,
        key_themes=str(themes.get(SentimentCategory(category), ["General feedback"])),
        trend_direction=trend_direction,
        survey_date=survey_date or date.today(),
    )

    db.add(pulse)
    await db.commit()
    await db.refresh(pulse)
    return pulse


async def detect_flight_risk(
    db: AsyncSession,
    employee_name: str,
    employee_email: str,
    department: str,
) -> FlightRiskAlert:
    """Run AI flight risk detection for an employee.

    In production: analyzes behavioral signals from HRIS, calendar, email, code repos.
    """
    # Simulate risk signal analysis
    seed = sum(ord(c) for c in employee_email) % 100

    # Select 2-5 signals based on risk level
    if seed > 70:
        risk_level = FlightRisk.critical
        risk_score = 80 + (seed % 20)
        signal_count = 5
    elif seed > 45:
        risk_level = FlightRisk.high
        risk_score = 55 + (seed % 25)
        signal_count = 4
    elif seed > 20:
        risk_level = FlightRisk.moderate
        risk_score = 25 + (seed % 30)
        signal_count = 3
    else:
        risk_level = FlightRisk.low
        risk_score = seed % 25
        signal_count = 2

    # Select signals and recommendations
    signals = random.sample(FLIGHT_RISK_SIGNALS, k=min(signal_count, len(FLIGHT_RISK_SIGNALS)))

    # Generate recommendations based on categories
    relevant_categories = random.sample(
        list(RETENTION_RECOMMENDATIONS.keys()),
        k=min(3, len(RETENTION_RECOMMENDATIONS)),
    )
    recommendations = []
    for cat in relevant_categories:
        recommendations.append(random.choice(RETENTION_RECOMMENDATIONS[cat]))

    alert = FlightRiskAlert(
        employee_name=employee_name,
        employee_email=employee_email,
        department=department,
        risk_level=risk_level,
        risk_score=risk_score,
        signals=str(signals),
        recommended_actions=str(recommendations),
        detected_at=datetime.utcnow(),
    )

    db.add(alert)
    await db.commit()
    await db.refresh(alert)
    return alert


async def get_sentiment_overview(db: AsyncSession) -> dict:
    """Get sentiment dashboard overview."""
    alerts_result = await db.execute(
        select(func.count()).select_from(FlightRiskAlert).where(
            FlightRiskAlert.resolved == False,  # noqa: E712
            FlightRiskAlert.acknowledged == False,  # noqa: E712
        )
    )
    active_alerts = alerts_result.scalar() or 0

    high_risk_result = await db.execute(
        select(func.count()).select_from(FlightRiskAlert).where(
            FlightRiskAlert.risk_level.in_([FlightRisk.high, FlightRisk.critical]),
            FlightRiskAlert.resolved == False,  # noqa: E712
        )
    )
    high_risk = high_risk_result.scalar() or 0

    # Average engagement from recent pulses
    avg_result = await db.execute(
        select(func.avg(SentimentPulse.avg_score)).where(
            SentimentPulse.category == SentimentCategory.engagement
        )
    )
    avg_engagement = avg_result.scalar() or 0.0

    # Trend from most recent pulse
    trend_result = await db.execute(
        select(SentimentPulse).order_by(SentimentPulse.created_at.desc()).limit(1)
    )
    trend_pulse = trend_result.scalar_one_or_none()

    return {
        "active_alerts": active_alerts,
        "high_risk_employees": high_risk,
        "avg_engagement_score": round(float(avg_engagement), 1),
        "trend_direction": trend_pulse.trend_direction if trend_pulse else "stable",
    }
