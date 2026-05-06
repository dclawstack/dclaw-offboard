from fastapi import APIRouter
from datetime import datetime
from uuid import uuid4
from dclaw_offboard.models import OffboardingChecklist, ChecklistCreate

router = APIRouter()

@router.post("/checklists", response_model=OffboardingChecklist)
async def create_item(payload: ChecklistCreate):
    return OffboardingChecklist(
        id=str(uuid4()),
        employee_name=payload.employee_name,
        last_day=payload.last_day,
        access_revocations=["VPN", "GitHub", "Slack"],
        asset_returns=["Laptop", "Badge"],
        knowledge_transfer_status="in_progress",
        exit_interview_scheduled=True,
        created_at=datetime.utcnow(),
    )

@router.get("/checklists/{checklist_id}/status")
async def get_item(checklist_id: str):
    return {"checklist_id": checklist_id, "completion_percent": 42}
