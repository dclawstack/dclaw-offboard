"""AI Offboard Copilot — P0.1.

Provides AI-guided assistance for offboarding processes:
- Answers questions about final pay, benefits, references
- Generates offboarding checklist templates
- Offers compliance guidance
- Falls back to local inference when cloud is unavailable
"""

import json
from typing import Optional

from app.schemas.offboarding import CopilotRequest, CopilotResponse

# ── Knowledge base for RAG ────────────────────────────────────────────────────

HR_POLICIES = {
    "final_pay": "Final pay is processed within 72 hours of the last working day. "
                 "It includes base salary up to the last day, accrued unused PTO payout, "
                 "and any approved bonuses.",
    "benefits": "Health insurance continues through the last day of the month of departure. "
                "COBRA eligibility begins the following month. 401(k) can be rolled over or left with the provider.",
    "references": "Company policy is to provide neutral employment verification (title, dates). "
                  "Personal references are at manager discretion.",
    "equipment": "All company equipment (laptop, phone, badges, keys) must be returned on or before the last day. "
                 "Failure to return may result in deduction from final pay.",
    "access": "System access is revoked at 5pm on the last working day. "
              "Early revocation requires manager and HR approval.",
    "severance": "Severance is based on tenure: 1 week per year of service, minimum 2 weeks, maximum 12 weeks. "
                 "Requires signing a separation agreement.",
    "non_compete": "Non-compete restrictions apply for 6 months post-departure for senior roles. "
                   "Review your employment agreement for specifics.",
    "alumni": "Alumni retain access to the alumni portal and are welcome at company events. "
              "Rehire eligibility is reviewed on a case-by-case basis."
}


def _build_system_prompt(context: Optional[str] = None) -> str:
    """Build system prompt with HR policy context."""
    policies_text = "\n".join([f"- {k}: {v}" for k, v in HR_POLICIES.items()])
    base = f"""You are an AI Offboarding Copilot for DClaw Offboard. 
Your role is to guide managers and HR through compliant, compassionate offboarding.

Company HR Policies:
{policies_text}

Guidelines:
- Be empathetic but professional
- Provide specific policy references when applicable
- Suggest concrete next steps
- If unsure about a legal matter, recommend consulting Legal/HR
- Keep responses concise and actionable
"""
    if context:
        base += f"\n\nCurrent context: {context}"
    return base


async def generate_copilot_response(request: CopilotRequest) -> CopilotResponse:
    """Generate AI copilot response using rules-based engine with policy lookups.

    In production, this would call an LLM (OpenRouter / Ollama) with RAG.
    For demo purposes, we use a deterministic rules engine that references
    HR policies and generates appropriate responses.
    """
    message = request.message.lower().strip()
    reply = ""
    actions: list[str] = []
    sources: list[str] = []

    # Simple intent matching
    if any(w in message for w in ["checklist", "template", "start", "begin"]):
        reply = (
            "I'll help you create an offboarding checklist. A standard checklist includes:\n\n"
            "**IT Tasks:** Revoke email, Slack, GitHub, VPN access; collect laptop and phone.\n"
            "**HR Tasks:** Process final pay, benefits continuation, exit interview scheduling.\n"
            "**Finance Tasks:** Expense report reconciliation, final paycheck, bonus processing.\n"
            "**Manager Tasks:** Knowledge transfer, team announcement, succession planning.\n\n"
            "Would you like me to generate a checklist for a specific employee?"
        )
        actions = ["Create offboarding checklist", "View checklist templates"]
        sources = ["Standard offboarding template"]

    elif any(w in message for w in ["final pay", "paycheck", "salary", "pto", "payout"]):
        reply = (
            f"**Final Pay Policy:**\n{HR_POLICIES['final_pay']}\n\n"
            f"**Severance:**\n{HR_POLICIES['severance']}\n\n"
            "Use the Final Pay Calculator to estimate the departing employee's final compensation. "
            "The calculation includes base salary, PTO payout, severance, and any deductions."
        )
        actions = ["Calculate final pay", "View pay stub template"]
        sources = ["Final Pay Policy", "Severance Policy"]

    elif any(w in message for w in ["benefits", "insurance", "cobra", "401k"]):
        reply = (
            f"{HR_POLICIES['benefits']}\n\n"
            "The departing employee should receive a benefits continuation packet from HR. "
            "Key items: COBRA enrollment form, 401(k) distribution options, and life insurance conversion."
        )
        actions = ["Send benefits packet", "Schedule benefits review call"]
        sources = ["Benefits Continuation Policy"]

    elif any(w in message for w in ["equipment", "asset", "laptop", "phone", "return"]):
        reply = (
            f"{HR_POLICIES['equipment']}\n\n"
            "I recommend generating an asset recovery checklist. "
            "All equipment should be inventoried, condition-assessed, and returned before the last day. "
            "Consider generating a prepaid shipping label for remote employees."
        )
        actions = ["Generate asset recovery list", "Create shipping label"]
        sources = ["Equipment Return Policy"]

    elif any(w in message for w in ["access", "revoke", "password", "account", "deactivate"]):
        reply = (
            f"{HR_POLICIES['access']}\n\n"
            "The access revocation workflow typically includes:\n"
            "- Email/GSuite deactivation\n"
            "- Slack/Teams removal\n"
            "- GitHub/GitLab access revocation\n"
            "- VPN/Citrix deactivation\n"
            "- Building access card deactivation\n"
            "- Third-party SaaS tool removal\n\n"
            "All revocations should be logged for the audit trail."
        )
        actions = ["View access matrix", "Revoke all access", "Generate audit report"]
        sources = ["Access Revocation Policy"]

    elif any(w in message for w in ["exit interview", "feedback", "survey"]):
        reply = (
            "Exit interviews are a critical source of organizational insight. Our AI-powered "
            "exit interview system:\n"
            "- Schedules a 30-minute confidential session\n"
            "- Transcribes and analyzes responses\n"
            "- Extracts key themes and sentiment\n"
            "- Generates actionable insights for leadership\n\n"
            "Would you like to schedule an exit interview?"
        )
        actions = ["Schedule exit interview", "View interview templates"]
        sources = ["Exit Interview Guide"]

    elif any(w in message for w in ["knowledge", "handover", "transfer", "document"]):
        reply = (
            "Structured knowledge transfer is essential to prevent information loss. "
            "I recommend capturing:\n"
            "- Active project documentation and status\n"
            "- Key contacts and relationships\n"
            "- Passwords and access credentials\n"
            "- Internal processes and workflows\n"
            "- Customer/vendor handoff notes\n\n"
            "Use the Knowledge Transfer form to document everything systematically."
        )
        actions = ["Start knowledge transfer", "View handover templates"]
        sources = ["Knowledge Transfer Best Practices"]

    elif any(w in message for w in ["alumni", "rehire", "boomerang", "network"]):
        reply = (
            f"{HR_POLICIES['alumni']}\n\n"
            "Maintaining positive alumni relationships benefits both parties. "
            "We track rehire eligibility and can set up alumni check-ins "
            "at 6-month and 12-month anniversaries."
        )
        actions = ["Add to alumni network", "Check rehire eligibility"]
        sources = ["Alumni Policy"]

    elif any(w in message for w in ["compliance", "legal", "regulation", "gdpr"]):
        reply = (
            "Offboarding compliance covers several areas:\n"
            "- **Data retention:** Personal data deleted per retention policy\n"
            "- **Non-compete:** Review agreement restrictions\n"
            "- **NDA:** Confirm ongoing confidentiality obligations\n"
            "- **Regulatory:** EEOC/OSHA reporting if applicable\n\n"
            "Consult with Legal for jurisdiction-specific requirements."
        )
        actions = ["Review compliance checklist", "Contact Legal"]
        sources = ["Compliance Policy", "Data Retention Policy"]

    else:
        reply = (
            "I'm your DClaw Offboard Copilot — here to help with any offboarding question. "
            "I can assist with:\n\n"
            "📋 **Checklists** — Generate role-specific offboarding checklists\n"
            "💰 **Final Pay** — Calculate final compensation and PTO payout\n"
            "💻 **Equipment** — Track and manage asset returns\n"
            "🔒 **Access** — Orchestrate system access revocation\n"
            "📝 **Exit Interviews** — Schedule and analyze exit feedback\n"
            "📚 **Knowledge Transfer** — Capture critical institutional knowledge\n"
            "🤝 **Alumni** — Maintain alumni relationships and rehire tracking\n\n"
            "What would you like help with?"
        )
        actions = ["Create checklist", "Calculate final pay", "Revoke access"]
        sources = ["Copilot Help"]

    return CopilotResponse(reply=reply, suggested_actions=actions, sources=sources)


async def analyze_exit_interview_sentiment(transcript: str) -> dict:
    """Analyze exit interview transcript for sentiment and themes.

    In production: call LLM with transcript. Demo: keyword-based analysis.
    """
    text = transcript.lower()
    
    # Simple sentiment analysis
    positive_words = ["enjoyed", "great", "excellent", "loved", "grateful", "appreciate", "wonderful", "opportunity"]
    negative_words = ["frustrated", "disappointed", "toxic", "unfair", "stress", "burnout", "quit", "poor"]

    pos_count = sum(1 for w in positive_words if w in text)
    neg_count = sum(1 for w in negative_words if w in text)
    total = pos_count + neg_count or 1

    raw_score = (pos_count - neg_count) / total
    if raw_score > 0.2:
        label = "positive"
    elif raw_score < -0.2:
        label = "negative"
    else:
        label = "neutral"

    # Simple theme extraction
    themes = []
    theme_keywords = {
        "Compensation": ["salary", "pay", "raise", "bonus", "compensation"],
        "Work-Life Balance": ["balance", "flexible", "remote", "hours", "weekend"],
        "Management": ["manager", "management", "leadership", "supervisor"],
        "Career Growth": ["growth", "promotion", "career", "learning", "development"],
        "Culture": ["culture", "environment", "team", "colleague", "people"],
        "Workload": ["workload", "overworked", "overtime", "demanding", "pressure"],
    }
    for theme, keywords in theme_keywords.items():
        if any(kw in text for kw in keywords):
            themes.append(theme)

    summary = (
        f"Exit interview analysis complete. Overall sentiment: {label}. "
        f"Key themes identified: {', '.join(themes) if themes else 'No specific themes detected'}. "
        f"Review full transcript for detailed insights."
    )

    return {
        "sentiment_score": round(raw_score, 2),
        "sentiment_label": label,
        "key_themes": themes,
        "summary": summary,
        "actionable_insights": (
            "Consider addressing the highlighted themes in retention strategy. "
            "Share anonymized insights with leadership."
        ),
    }
