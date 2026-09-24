from ipaddress import IPv4Address, IPv4Network
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class SubnetCreate(BaseModel):
    name: str = Field(min_length=1, max_length=128)
    network: IPv4Network
    gateway: IPv4Address | None = None
    dns_servers: list[IPv4Address] = Field(default_factory=list)
    dns_domain: str | None = Field(default=None, max_length=253)
    interface_name: str | None = Field(default=None, max_length=128)
    excluded_addresses: list[IPv4Address] = Field(default_factory=list)
    is_active: bool = True
    additional_options: dict[str, str] = Field(default_factory=dict)

    @field_validator("network", mode="before")
    @classmethod
    def strict_network(cls, value: object) -> object:
        return value


class SubnetRead(SubnetCreate):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
