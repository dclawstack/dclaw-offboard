from pydantic import BaseModel
from datetime import datetime
from typing import List

class OffboardingChecklist(BaseModel):
    id: str
    employee_name: str
    last_day: str
    access_revocations: list[str]
    asset_returns: list[str]
    knowledge_transfer_status: str
    exit_interview_scheduled: bool
    created_at: datetime

class ChecklistCreate(BaseModel):
    employee_name: str
    last_day: str
