from datetime import datetime
from enum import StrEnum
from ipaddress import IPv4Address
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class DhcpEventType(StrEnum):
    DISCOVER = "discover"
    OFFER = "offer"
    REQUEST = "request"
    ACK = "ack"
    NAK = "nak"
    RELEASE = "release"
    DECLINE = "decline"
    UNKNOWN = "unknown"


class DhcpLogRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    occurred_at: datetime
    member_name: str
    event_type: DhcpEventType
    mac_address: str | None
    ipv4_address: IPv4Address | None
    hostname: str | None
    raw_message: str
