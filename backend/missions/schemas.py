from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class MissionCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str = Field(min_length=1, max_length=2000)
    project_id: int
    required_skills: list[str] = []
    rate: Decimal = Field(gt=0)
    start_date: date
    end_date: date


class MissionResponse(BaseModel):
    id: int
    customer_id: int
    project_id: int
    title: str
    description: str
    required_skills: list[str]
    rate: Decimal
    start_date: date
    end_date: date
    status: str
    created_at: datetime


class AssignmentResponse(BaseModel):
    id: int
    mission_id: int
    fighter_id: int
    squad_id: int | None
    status: str