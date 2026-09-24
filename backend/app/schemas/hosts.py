import re
from datetime import datetime
from ipaddress import IPv4Address
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

_HOSTNAME = re.compile(r"^(?=.{1,63}$)[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?$")
_MAC = re.compile(r"^[0-9a-fA-F]{2}([:-]?[0-9a-fA-F]{2}){5}$")


class HostCreate(BaseModel):
    hostname: str
    mac_address: str
    ipv4_address: IPv4Address
    subnet_name: str = Field(min_length=1, max_length=128)
    description: str | None = Field(default=None, max_length=500)
    is_active: bool = True
    additional_options: dict[str, str] = Field(default_factory=dict)

    @field_validator("hostname")
    @classmethod
    def validate_hostname(cls, value: str) -> str:
        if not _HOSTNAME.fullmatch(value):
            raise ValueError("hostname must be a valid DHCP host identifier")
        return value.lower()

    @field_validator("mac_address")
    @classmethod
    def normalize_mac(cls, value: str) -> str:
        if not _MAC.fullmatch(value):
            raise ValueError("mac_address must contain six hexadecimal octets")
        octets = re.findall(r"[0-9a-fA-F]{2}", value)
        return ":".join(octet.lower() for octet in octets)


class HostRead(HostCreate):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime
