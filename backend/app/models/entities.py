import uuid
from datetime import datetime

from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, Index, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class TimestampedModel:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class User(TimestampedModel, Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    login: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    display_name: Mapped[str] = mapped_column(String(256))
    auth_source: Mapped[str] = mapped_column(String(64), default="external")
    roles: Mapped[list[str]] = mapped_column(JSON, default=list)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class Subnet(TimestampedModel, Base):
    __tablename__ = "subnets"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(128), unique=True)
    network: Mapped[str] = mapped_column(String(43), unique=True)
    gateway: Mapped[str | None] = mapped_column(String(15))
    dns_servers: Mapped[list[str]] = mapped_column(JSON, default=list)
    dns_domain: Mapped[str | None] = mapped_column(String(253))
    interface_name: Mapped[str | None] = mapped_column(String(128))
    excluded_addresses: Mapped[list[str]] = mapped_column(JSON, default=list)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    additional_options: Mapped[dict[str, str]] = mapped_column(JSON, default=dict)


class StaticHost(TimestampedModel, Base):
    __tablename__ = "static_hosts"
    __table_args__ = (Index("ix_static_hosts_subnet_active", "subnet_id", "is_active"),)

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    hostname: Mapped[str] = mapped_column(String(63), unique=True)
    mac_address: Mapped[str] = mapped_column(String(17), unique=True, index=True)
    ipv4_address: Mapped[str] = mapped_column(String(15), unique=True, index=True)
    subnet_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("subnets.id"), index=True)
    description: Mapped[str | None] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    additional_options: Mapped[dict[str, str]] = mapped_column(JSON, default=dict)


class ClusterMember(TimestampedModel, Base):
    __tablename__ = "cluster_members"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(128), unique=True)
    management_address: Mapped[str] = mapped_column(String(255), unique=True)
    ssh_port: Mapped[int] = mapped_column(Integer, default=22)
    expected_host_fingerprint: Mapped[str] = mapped_column(String(512))
    role: Mapped[str] = mapped_column(String(16), default="unknown")
    last_checked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class Change(TimestampedModel, Base):
    __tablename__ = "changes"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    status: Mapped[str] = mapped_column(String(32), default="draft", index=True)
    author_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"))
    approver_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"))
    operations: Mapped[list[dict[str, object]]] = mapped_column(JSON, default=list)
    generated_configuration: Mapped[str | None] = mapped_column(Text)
    diff: Mapped[str | None] = mapped_column(Text)
    sha256: Mapped[str | None] = mapped_column(String(64), index=True)


class Deployment(TimestampedModel, Base):
    __tablename__ = "deployments"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    change_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("changes.id"), unique=True)
    status: Mapped[str] = mapped_column(String(32), default="queued", index=True)
    member_results: Mapped[dict[str, object]] = mapped_column(JSON, default=dict)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class DhcpLog(Base):
    __tablename__ = "dhcp_logs"
    __table_args__ = (
        Index("ix_dhcp_logs_occurred_mac", "occurred_at", "mac_address"),
        Index("ix_dhcp_logs_occurred_ip", "occurred_at", "ipv4_address"),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    member_name: Mapped[str] = mapped_column(String(128), index=True)
    event_type: Mapped[str] = mapped_column(String(32), index=True)
    mac_address: Mapped[str | None] = mapped_column(String(17), index=True)
    ipv4_address: Mapped[str | None] = mapped_column(String(15), index=True)
    hostname: Mapped[str | None] = mapped_column(String(255), index=True)
    raw_message: Mapped[str] = mapped_column(Text)


class AuditEvent(Base):
    __tablename__ = "audit_events"
    __table_args__ = (Index("ix_audit_events_created_action", "created_at", "action"),)

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    actor_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"), index=True)
    source_ip: Mapped[str | None] = mapped_column(String(64))
    action: Mapped[str] = mapped_column(String(128))
    object_type: Mapped[str] = mapped_column(String(64))
    object_id: Mapped[str] = mapped_column(String(64))
    before_value: Mapped[dict[str, object] | None] = mapped_column(JSON)
    after_value: Mapped[dict[str, object] | None] = mapped_column(JSON)
    result: Mapped[str] = mapped_column(String(32))
    correlation_id: Mapped[str] = mapped_column(String(64), index=True)
