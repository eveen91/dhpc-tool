from app.infrastructure.firewall.adapter import (
    FirewallAdapter,
    FirewallOperationResult,
    FirewallRole,
    FirewallStatus,
)


class FakeFirewallAdapter(FirewallAdapter):
    """Deterministic test adapter; it never opens network connections."""

    def status(self, member_name: str) -> FirewallStatus:
        role = FirewallRole.ACTIVE if member_name.endswith("a") else FirewallRole.STANDBY
        return FirewallStatus(reachable=True, role=role, dhcp_healthy=True, checksum=None)

    def validate_configuration(
        self, member_name: str, content: str, sha256: str
    ) -> FirewallOperationResult:
        return FirewallOperationResult(
            succeeded="range" not in content.lower(), message="validation simulated"
        )

    def install_configuration(
        self, member_name: str, content: str, sha256: str, deployment_id: str
    ) -> FirewallOperationResult:
        return FirewallOperationResult(
            succeeded=False,
            message="Real installations are disabled in this project skeleton",
        )

    def rollback(self, member_name: str, backup_id: str) -> FirewallOperationResult:
        return FirewallOperationResult(succeeded=False, message="Real rollback is not implemented")
