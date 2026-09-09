from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import (
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base


class Mission(Base):
    __tablename__ = "missions"

    id: Mapped[int] = mapped_column(primary_key=True)

    customer_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
    )

    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id"),
    )

    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(2000))

    required_skills: Mapped[list[str]] = mapped_column(
        ARRAY(String),
        default=list,
    )

    rate_per_shift: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
    )

    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[date] = mapped_column(Date)

    status: Mapped[str] = mapped_column(
        String(20),
        default="open",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
    )


class Assignment(Base):
    __tablename__ = "assignments"

    id: Mapped[int] = mapped_column(primary_key=True)

    mission_id: Mapped[int] = mapped_column(
        ForeignKey("missions.id"),
    )

    fighter_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
    )

    squad_id: Mapped[int | None] = mapped_column(
        ForeignKey("squads.id"),
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="pending",
    )

    check_in_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    check_out_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    amount_earned: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 2),
        nullable=True,
    )

    platform_fee: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        default=0,
    )