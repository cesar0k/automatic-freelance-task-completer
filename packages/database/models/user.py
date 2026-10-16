from datetime import datetime

from sqlalchemy import BigInteger, Boolean, DateTime, String, text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from packages.database.base import Base
from packages.database.enums import UserRole, pg_enum


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str | None] = mapped_column(String(64), unique=True)
    full_name: Mapped[str | None] = mapped_column(String(128))
    telegram_id: Mapped[int | None] = mapped_column(BigInteger, unique=True)
    role: Mapped[UserRole] = mapped_column(pg_enum(UserRole, name="user_role"), nullable=False)
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default=text("true")
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
