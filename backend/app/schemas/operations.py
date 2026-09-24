from datetime import datetime
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ChangeStatus(StrEnum):
    DRAFT = "draft"
    VALIDATING = "validating"
    VALIDATED = "validated"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    DEPLOYING_STANDBY = "deploying_standby"
    VERIFYING_STANDBY = "verifying_standby"
    DEPLOYING_ACTIVE = "deploying_active"
    VERIFYING_ACTIVE = "verifying_active"
    VERIFIED = "verified"
    COMPLETED = "completed"
    FAILED_VALIDATION = "failed_validation"
    FAILED_STANDBY = "failed_standby"
    FAILED_ACTIVE = "failed_active"
    CLUSTER_ROLE_CHANGED = "cluster_role_changed"
    ROLLBACK_REQUIRED = "rollback_required"
    ROLLING_BACK = "rolling_back"
    ROLLED_BACK = "rolled_back"
    ROLLBACK_FAILED = "rollback_failed"
    INCONSISTENT = "inconsistent"


class DeploymentStatus(StrEnum):
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"


class ChangeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    status: ChangeStatus
    sha256: str | None
    created_at: datetime


class DeploymentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    change_id: UUID
    status: DeploymentStatus
    started_at: datetime | None
    finished_at: datetime | None
