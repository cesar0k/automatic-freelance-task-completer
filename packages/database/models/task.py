from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from packages.database.base import Base
from packages.database.enums import ReviewStatus, TaskStatus, pg_enum


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"), nullable=False
    )
    version: Mapped[int] = mapped_column(nullable=False, default=1, server_default="1")
    status: Mapped[TaskStatus] = mapped_column(
        pg_enum(TaskStatus, name="task_status"),
        nullable=False,
        default=TaskStatus.QUEUED,
        server_default="QUEUED",
    )
    archive_path: Mapped[str | None] = mapped_column(Text)
    checksum: Mapped[str | None] = mapped_column(String(64))
    agent_model: Mapped[str | None] = mapped_column(String(64))
    review_status: Mapped[ReviewStatus] = mapped_column(
        pg_enum(ReviewStatus, name="review_status"),
        nullable=False,
        default=ReviewStatus.PENDING,
        server_default="PENDING",
    )
    reviewed_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    review_notes: Mapped[str | None] = mapped_column(Text)
    error_message: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    __table_args__ = (
        UniqueConstraint("order_id", "version", name="uq_tasks_version"),
        Index("idx_tasks_order", "order_id"),
        Index("idx_tasks_status", "status"),
    )
