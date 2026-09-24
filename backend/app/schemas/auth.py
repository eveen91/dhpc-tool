from datetime import datetime
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class Role(StrEnum):
    VIEWER = "viewer"
    OPERATOR = "operator"
    APPROVER = "approver"
    ADMINISTRATOR = "administrator"


class AuthenticatedUser(BaseModel):
    """Identity contract populated by a future OIDC/LDAP/local provider."""

    subject: str
    login: str
    display_name: str
    roles: set[Role] = Field(default_factory=set)


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    login: str
    display_name: str
    auth_source: str
    roles: list[Role]
    is_active: bool
    last_login_at: datetime | None
