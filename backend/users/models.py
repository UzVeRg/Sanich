from datetime import datetime

from sqlalchemy import DateTime, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    phone: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        index=True,
    )

    full_name: Mapped[str] = mapped_column(
        String(255),
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
    )

    role: Mapped[str] = mapped_column(
        String(20),
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="pending",
    )

    rating: Mapped[float] = mapped_column(
        Numeric(3, 2),
        default=5.0,
    )

    exp: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
    )


class Device(Base):
    __tablename__ = "devices"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column()

    device_id: Mapped[str] = mapped_column(
        String(255),
        unique=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
    )


class Squad(Base):
    __tablename__ = "squads"

    id: Mapped[int] = mapped_column(primary_key=True)

    leader_id: Mapped[int] = mapped_column()

    name: Mapped[str] = mapped_column(
        String(100),
    )

    rating: Mapped[float] = mapped_column(
        Numeric(3, 2),
        default=5.0,
    )


class SquadMember(Base):
    __tablename__ = "squad_members"

    squad_id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    user_id: Mapped[int] = mapped_column(
        primary_key=True,
    )