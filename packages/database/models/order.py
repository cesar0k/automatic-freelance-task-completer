from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    CHAR,
    DateTime,
    ForeignKey,
    Index,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from packages.database.base import Base
from packages.database.enums import OrderStatus, pg_enum


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    source: Mapped[str] = mapped_column(String(32), nullable=False)
    external_id: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    url: Mapped[str | None] = mapped_column(Text)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    budget: Mapped[Decimal | None] = mapped_column(Numeric(10, 2))
    currency: Mapped[str] = mapped_column(
        CHAR(3), nullable=False, default="RUB", server_default="RUB"
    )
    category: Mapped[str | None] = mapped_column(String(64))
    priority_score: Mapped[int] = mapped_column(nullable=False, default=0, server_default="0")
    prompt: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[OrderStatus] = mapped_column(
        pg_enum(OrderStatus, name="order_status"),
        nullable=False,
        default=OrderStatus.NEW,
        server_default="NEW",
    )
    raw_order: Mapped[dict] = mapped_column(
        JSONB, nullable=False, default=dict, server_default=text("'{}'::jsonb")
    )
    assigned_manager_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    assigned_reviewer_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )

    __table_args__ = (
        UniqueConstraint("source", "external_id", name="uq_orders_source_ext"),
        Index("idx_orders_status", "status"),
        Index("idx_orders_fresh", "published_at", postgresql_ops={"published_at": "DESC"}),
        Index("idx_orders_raw_gin", "raw_order", postgresql_using="gin"),
    )
