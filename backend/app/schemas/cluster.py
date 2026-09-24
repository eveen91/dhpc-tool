from datetime import datetime
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ClusterRole(StrEnum):
    ACTIVE = "active"
    STANDBY = "standby"
    UNKNOWN = "unknown"


class ClusterMemberCreate(BaseModel):
    name: str = Field(min_length=1, max_length=128)
    management_address: str
    ssh_port: int = Field(default=22, ge=1, le=65535)
    expected_host_fingerprint: str = Field(min_length=1, max_length=512)


class ClusterMemberRead(ClusterMemberCreate):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    role: ClusterRole
    last_checked_at: datetime | None
