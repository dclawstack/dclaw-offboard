# DClaw Offboard — v1.2 Feature Roadmap

> Based on: Y Combinator vertical SaaS principles, trending GitHub repos (offboarding-tools), AI product research (Culture Amp, Peakon, ExitPro)

## Pre-Flight Checklist

- [ ] `frontend/package-lock.json` committed after any `npm install` / dependency change
- [ ] `frontend/next-env.d.ts` exists and is committed
- [ ] `docker-compose.yml` healthchecks correct
- [ ] `frontend/Dockerfile` declares `ARG NEXT_PUBLIC_API_URL` before `RUN npm run build`

## v1.0 Feature Inventory (Current)

- [ ] Offboarding checklist templates
- [ ] Asset recovery tracking
- [ ] Access revocation workflow
- [ ] Exit interview scheduling
- [ ] Real backend CRUD (no mocks)
- [ ] Docker + Helm deployment
- [ ] Alembic migrations
- [ ] Backend tests

---

## v1.2 Roadmap

### P0 — Must Have (Ship in v1.0, demo-ready)

#### 1. AI Offboard Copilot (Exit Guide)
**Description:** AI assistant that guides departing employees through offboarding steps, answers questions about final pay, benefits continuation, and reference policies.
- **AI Angle:** RAG over HR policies + offboarding FAQs. Personalized based on tenure/role.
- **Backend:** `/api/v1/ai/offboard-chat` endpoint.
- **Frontend:** Chat widget in offboarding portal.
- **Files:** `backend/app/services/offboard_ai.py`, `frontend/src/components/offboard-copilot.tsx`

#### 2. Offboarding Checklist & Workflow
**Description:** Structured offboarding journeys with IT, HR, finance, and manager tasks. Dependencies and deadlines.
- **Backend:** Workflow engine with role-based assignments.
- **Frontend:** Progress tracker. Task assignment board.
- **Files:** `backend/app/services/offboard_workflow.py`

#### 3. Asset Recovery & Inventory
**Description:** Track company assets (laptop, phone, keys, cards). Auto-generate recovery list.
- **Backend:** Asset inventory integration. Recovery status tracking.
- **Frontend:** Asset checklist with condition notes. Shipping label generation.
- **Files:** `backend/app/services/asset_recovery.py`

#### 4. Access Revocation Automation
**Description:** One-click revocation of system access, email, Slack, VPN. Audit trail.
- **Backend:** Identity provider integrations (Okta, Azure AD). Revocation API.
- **Frontend:** Access matrix with revoke buttons. Revocation confirmation workflow.
- **Files:** `backend/app/integrations/access_control.py`

### P1 — Should Have (v1.1–1.2)

#### 5. AI Exit Interview Analysis
**Description:** Conduct exit interviews (async or live). AI extracts themes, sentiment, and actionable insights.
- **AI Angle:** Transcript analysis + sentiment extraction + theme clustering.
- **Backend:** Interview recording + processing pipeline.
- **Frontend:** Interview scheduler. Insights dashboard with trend charts.

#### 6. Knowledge Transfer & Handover
**Description:** Structured knowledge capture: project docs, contacts, passwords, process docs.
- **Backend:** Handover template engine. Document generation.
- **Frontend:** Handover form with validation. Knowledge base auto-population.

#### 7. Alumni Network & Rehire Eligibility
**Description:** Maintain alumni database. Track rehire eligibility. Send anniversary check-ins.
- **Backend:** Alumni CRM. Rehire flag management.
- **Frontend:** Alumni directory. Rehire pipeline view.

#### 8. Final Pay & Compliance Calculator
**Description:** Calculate final pay, unused PTO payout, severance. Generate compliance reports.
- **Backend:** Payroll calculation engine. Compliance report generation.
- **Frontend:** Pay estimator. Compliance checklist.

### P2 — Could Have (v1.3+)

#### 9. Predictive Flight Risk Alerts
**Description:** Integrate with HR data to flag employees showing pre-resignation signals.

#### 10. Offboarding Analytics & Retention Insights
**Description:** Dashboard showing offboarding trends, top reasons, department analysis.

#### 11. Boomerang Re-engagement Campaigns
**Description:** Automated nurture campaigns for alumni (job alerts, company news, referral asks).

#### 12. Regulatory Compliance Automation (GDPR/SOC2)
**Description:** Auto-delete personal data post-retention period. Compliance audit trails.

---

## Implementation Priority

1. **Week 1–2:** AI Offboard Copilot (P0.1) + Offboarding Workflow (P0.2)
2. **Week 3–4:** Asset Recovery (P0.3) + Access Revocation (P0.4)
3. **Week 5–6:** Exit Interview AI (P1.5) + Knowledge Transfer (P1.6)
4. **Week 7–8:** Alumni Network (P1.7) + Final Pay Calculator (P1.8)
