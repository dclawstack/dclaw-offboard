"""Risk Assessment & IP Protection service — v1.3.

AI-driven anomaly detection and risk scoring for departing employees.
"""

import random
from datetime import date, datetime, timedelta
from typing import Optional
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.offboarding_v13 import RiskAssessment, RiskLevel


def _simulate_anomaly_detection(employee_email: str, department: str, role: str) -> dict:
    """Simulate AI anomaly detection for a departing employee.

    In production, this queries SIEM/DLP/EDR systems for real data.
    """
    # Deterministic-ish seed from email for reproducible demo
    seed = sum(ord(c) for c in employee_email) % 100
    dept_factor = {
        "engineering": 1.5,
        "research": 1.7,
        "product": 1.2,
        "sales": 0.8,
        "hr": 0.5,
        "finance": 1.0,
    }.get(department.lower(), 1.0)

    # Generate anomaly metrics
    unusual_files = max(0, int(seed * dept_factor / 10))
    downloads = max(0, int(seed * dept_factor / 15))
    email_fwd = seed > 60 and department.lower() in ("engineering", "research")
    usb_activity = seed > 75
    after_hours = max(0, int(seed * dept_factor / 5))

    # Calculate risk score (0-100)
    raw_score = (
        unusual_files * 5
        + downloads * 8
        + (15 if email_fwd else 0)
        + (20 if usb_activity else 0)
        + after_hours * 2
    )
    risk_score = min(100, raw_score)

    # Determine risk level
    if risk_score >= 75:
        risk_level = RiskLevel.critical
    elif risk_score >= 50:
        risk_level = RiskLevel.high
    elif risk_score >= 25:
        risk_level = RiskLevel.medium
    else:
        risk_level = RiskLevel.low

    # Generate anomalies list
    anomaly_list = []
    if unusual_files > 3:
        anomaly_list.append(f"Unusual file access pattern: {unusual_files} atypical file accesses detected")
    if downloads > 2:
        anomaly_list.append(f"Large data downloads: {downloads} bulk download events")
    if email_fwd:
        anomaly_list.append("External email forwarding detected — possible data exfiltration")
    if usb_activity:
        anomaly_list.append("USB mass storage device connected — potential data transfer")
    if after_hours > 3:
        anomaly_list.append(f"After-hours system activity: {after_hours} sessions outside business hours")

    # Recommendations
    recommendations = []
    if risk_level in (RiskLevel.high, RiskLevel.critical):
        recommendations.append("Preserve forensic evidence immediately")
        recommendations.append("Involve Legal and InfoSec teams")
        recommendations.append("Disable external sharing / USB ports")
    if risk_level == RiskLevel.medium:
        recommendations.append("Increase monitoring frequency")
        recommendations.append("Review recent access logs manually")
    if risk_level == RiskLevel.low:
        recommendations.append("Continue standard monitoring")
        recommendations.append("Document findings for audit trail")

    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "unusual_file_access": unusual_files,
        "large_downloads": downloads,
        "email_forwarding_detected": email_fwd,
        "usb_activity_detected": usb_activity,
        "after_hours_activity": after_hours,
        "anomalies": anomaly_list,
        "recommendations": recommendations,
    }


async def run_risk_assessment(
    db: AsyncSession,
    employee_name: str,
    employee_email: str,
    department: str,
    role: str,
    last_day: Optional[date] = None,
) -> RiskAssessment:
    """Run a full AI-driven risk assessment for a departing employee."""
    findings = _simulate_anomaly_detection(employee_email, department, role)

    assessment = RiskAssessment(
        employee_name=employee_name,
        employee_email=employee_email,
        department=department,
        role=role,
        last_day=last_day,
        risk_level=findings["risk_level"],
        risk_score=findings["risk_score"],
        unusual_file_access=findings["unusual_file_access"],
        large_downloads=findings["large_downloads"],
        email_forwarding_detected=findings["email_forwarding_detected"],
        usb_activity_detected=findings["usb_activity_detected"],
        after_hours_activity=findings["after_hours_activity"],
        anomalies=str(findings["anomalies"]),
        evidence_preserved=findings["risk_level"] in (RiskLevel.high, RiskLevel.critical),
        evidence_location="/secure/forensics/" + employee_email.split("@")[0] if findings["risk_level"] in (RiskLevel.high, RiskLevel.critical) else None,
        recommendations=str(findings["recommendations"]),
        monitoring_start=datetime.utcnow() - timedelta(days=90) if last_day else datetime.utcnow() - timedelta(days=30),
        monitoring_end=datetime.utcnow(),
        assessed_by="AI Risk Engine v1.3",
    )

    db.add(assessment)
    await db.commit()
    await db.refresh(assessment)
    return assessment


async def get_risk_overview(db: AsyncSession) -> dict:
    """Get risk dashboard overview stats."""
    total_result = await db.execute(
        select(func.count()).select_from(RiskAssessment)
    )
    total = total_result.scalar() or 0

    critical_result = await db.execute(
        select(func.count()).select_from(RiskAssessment).where(
            RiskAssessment.risk_level == RiskLevel.critical
        )
    )
    critical = critical_result.scalar() or 0

    high_result = await db.execute(
        select(func.count()).select_from(RiskAssessment).where(
            RiskAssessment.risk_level == RiskLevel.high
        )
    )
    high = high_result.scalar() or 0

    evidence_result = await db.execute(
        select(func.count()).select_from(RiskAssessment).where(
            RiskAssessment.evidence_preserved == True  # noqa: E712
        )
    )
    evidence = evidence_result.scalar() or 0

    return {
        "total_assessments": total,
        "critical_risks": critical,
        "high_risks": high,
        "evidence_preserved_count": evidence,
    }
