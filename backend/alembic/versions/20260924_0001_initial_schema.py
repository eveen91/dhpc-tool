"""Initial DHCP Manager schema skeleton.

Revision ID: 20260924_0001
Revises:
Create Date: 2026-09-24
"""

import sqlalchemy as sa

from alembic import op

revision = "20260924_0001"
down_revision = None
branch_labels = None
depends_on = None


def _uuid_column() -> sa.Column[sa.UUID]:
    return sa.Column("id", sa.Uuid(), primary_key=True, nullable=False)


def upgrade() -> None:
    op.create_table(
        "users",
        _uuid_column(),
        sa.Column("login", sa.String(length=128), nullable=False),
        sa.Column("display_name", sa.String(length=256), nullable=False),
        sa.Column("auth_source", sa.String(length=64), nullable=False),
        sa.Column("roles", sa.JSON(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("last_login_at", sa.DateTime(timezone=True)),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.UniqueConstraint("login"),
    )
    op.create_index("ix_users_login", "users", ["login"])
    op.create_table(
        "subnets",
        _uuid_column(),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("network", sa.String(length=43), nullable=False),
        sa.Column("gateway", sa.String(length=15)),
        sa.Column("dns_servers", sa.JSON(), nullable=False),
        sa.Column("dns_domain", sa.String(length=253)),
        sa.Column("interface_name", sa.String(length=128)),
        sa.Column("excluded_addresses", sa.JSON(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("additional_options", sa.JSON(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.UniqueConstraint("name"),
        sa.UniqueConstraint("network"),
    )
    op.create_table(
        "static_hosts",
        _uuid_column(),
        sa.Column("hostname", sa.String(length=63), nullable=False),
        sa.Column("mac_address", sa.String(length=17), nullable=False),
        sa.Column("ipv4_address", sa.String(length=15), nullable=False),
        sa.Column("subnet_id", sa.Uuid(), sa.ForeignKey("subnets.id"), nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("additional_options", sa.JSON(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.UniqueConstraint("hostname"),
        sa.UniqueConstraint("mac_address"),
        sa.UniqueConstraint("ipv4_address"),
    )
    op.create_index("ix_static_hosts_subnet_active", "static_hosts", ["subnet_id", "is_active"])
    op.create_table(
        "cluster_members",
        _uuid_column(),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("management_address", sa.String(length=255), nullable=False),
        sa.Column("ssh_port", sa.Integer(), nullable=False),
        sa.Column("expected_host_fingerprint", sa.String(length=512), nullable=False),
        sa.Column("role", sa.String(length=16), nullable=False),
        sa.Column("last_checked_at", sa.DateTime(timezone=True)),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.UniqueConstraint("name"),
        sa.UniqueConstraint("management_address"),
    )
    op.create_table(
        "changes",
        _uuid_column(),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("author_id", sa.Uuid(), sa.ForeignKey("users.id")),
        sa.Column("approver_id", sa.Uuid(), sa.ForeignKey("users.id")),
        sa.Column("operations", sa.JSON(), nullable=False),
        sa.Column("generated_configuration", sa.Text()),
        sa.Column("diff", sa.Text()),
        sa.Column("sha256", sa.String(length=64)),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
    )
    op.create_table(
        "deployments",
        _uuid_column(),
        sa.Column("change_id", sa.Uuid(), sa.ForeignKey("changes.id"), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("member_results", sa.JSON(), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True)),
        sa.Column("finished_at", sa.DateTime(timezone=True)),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.UniqueConstraint("change_id"),
    )
    op.create_table(
        "dhcp_logs",
        _uuid_column(),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("member_name", sa.String(length=128), nullable=False),
        sa.Column("event_type", sa.String(length=32), nullable=False),
        sa.Column("mac_address", sa.String(length=17)),
        sa.Column("ipv4_address", sa.String(length=15)),
        sa.Column("hostname", sa.String(length=255)),
        sa.Column("raw_message", sa.Text(), nullable=False),
    )
    op.create_index("ix_dhcp_logs_occurred_mac", "dhcp_logs", ["occurred_at", "mac_address"])
    op.create_index("ix_dhcp_logs_occurred_ip", "dhcp_logs", ["occurred_at", "ipv4_address"])
    op.create_table(
        "audit_events",
        _uuid_column(),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column("actor_id", sa.Uuid(), sa.ForeignKey("users.id")),
        sa.Column("source_ip", sa.String(length=64)),
        sa.Column("action", sa.String(length=128), nullable=False),
        sa.Column("object_type", sa.String(length=64), nullable=False),
        sa.Column("object_id", sa.String(length=64), nullable=False),
        sa.Column("before_value", sa.JSON()),
        sa.Column("after_value", sa.JSON()),
        sa.Column("result", sa.String(length=32), nullable=False),
        sa.Column("correlation_id", sa.String(length=64), nullable=False),
    )
    op.create_index("ix_audit_events_created_action", "audit_events", ["created_at", "action"])


def downgrade() -> None:
    for table in (
        "audit_events",
        "dhcp_logs",
        "deployments",
        "changes",
        "cluster_members",
        "static_hosts",
        "subnets",
        "users",
    ):
        op.drop_table(table)
