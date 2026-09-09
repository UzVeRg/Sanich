from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.router import get_current_user
from core.database import get_db
from missions.models import Assignment, Mission
from missions.schemas import (
    AssignmentResponse,
    MissionCreate,
    MissionResponse,
)
from users.models import User


router = APIRouter(
    prefix="/missions",
    tags=["Missions"],
)


@router.post(
    "",
    response_model=MissionResponse,
)
async def create_mission(
    data: MissionCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if user.role != "customer":
        raise HTTPException(
            status_code=403,
            detail="Только заказчик может создавать миссии",
        )

    if data.end_date < data.start_date:
        raise HTTPException(
            status_code=400,
            detail="Дата окончания не может быть раньше даты начала",
        )

    mission = Mission(
        customer_id=user.id,
        project_id=data.project_id,
        title=data.title,
        description=data.description,
        required_skills=data.required_skills,
        rate_per_shift=data.rate,
        start_date=data.start_date,
        end_date=data.end_date,
        status="open",
    )

    db.add(mission)
    await db.commit()
    await db.refresh(mission)

    return mission


@router.get(
    "",
    response_model=list[MissionResponse],
)
async def get_missions(
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Mission)
        .where(Mission.status == "open")
        .order_by(Mission.created_at.desc())
    )

    return result.scalars().all()


@router.get(
    "/my",
    response_model=list[MissionResponse],
)
async def get_my_missions(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if user.role != "customer":
        raise HTTPException(
            status_code=403,
            detail="Только заказчик может просматривать свои миссии",
        )

    result = await db.execute(
        select(Mission)
        .where(Mission.customer_id == user.id)
        .order_by(Mission.created_at.desc())
    )

    return result.scalars().all()


@router.get(
    "/{mission_id}",
    response_model=MissionResponse,
)
async def get_mission(
    mission_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Mission).where(Mission.id == mission_id)
    )

    mission = result.scalar_one_or_none()

    if mission is None:
        raise HTTPException(
            status_code=404,
            detail="Миссия не найдена",
        )

    return mission


@router.post(
    "/{mission_id}/apply",
    response_model=AssignmentResponse,
)
async def apply_to_mission(
    mission_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if user.role not in {
        "fighter",
        "squad_leader",
    }:
        raise HTTPException(
            status_code=403,
            detail="Только боец или бригадир может принять миссию",
        )

    result = await db.execute(
        select(Mission).where(Mission.id == mission_id)
    )

    mission = result.scalar_one_or_none()

    if mission is None:
        raise HTTPException(
            status_code=404,
            detail="Миссия не найдена",
        )

    if mission.status != "open":
        raise HTTPException(
            status_code=400,
            detail="Миссия больше недоступна",
        )

    result = await db.execute(
        select(Assignment).where(
            Assignment.mission_id == mission_id,
            Assignment.fighter_id == user.id,
        )
    )

    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail="Вы уже откликнулись на эту миссию",
        )

    assignment = Assignment(
        mission_id=mission.id,
        fighter_id=user.id,
        status="pending",
    )

    db.add(assignment)
    await db.commit()
    await db.refresh(assignment)

    return assignment