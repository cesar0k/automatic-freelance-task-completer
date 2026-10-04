from enum import Enum, StrEnum

from sqlalchemy import Enum as SAEnum


def pg_enum[E: Enum](enum_cls: type[E], *, name: str) -> SAEnum:
    return SAEnum(
        enum_cls,
        name=name,
        native_enum=True,
        create_type=False,
        values_callable=lambda obj: [e.value for e in obj],
    )


class UserRole(StrEnum):
    ADMIN = "admin"
    DEV = "dev"
    SALES = "sales"


class OrderStatus(StrEnum):
    NEW = "NEW"
    CLAIMED = "CLAIMED"
    IN_PROGRESS = "IN_PROGRESS"
    IN_REVIEW = "IN_REVIEW"
    REJECTED = "REJECTED"
    COMPLETED = "COMPLETED"
    READY_FOR_DELIVERY = "READY_FOR_DELIVERY"


class TaskStatus(StrEnum):
    QUEUED = "QUEUED"
    PROCESSING = "PROCESSING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"


class ReviewStatus(StrEnum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
