from app.infrastructure.firewall.adapter import (
    FirewallAdapter,
    FirewallOperationResult,
    FirewallStatus,
)


class SshFirewallAdapter(FirewallAdapter):
    """Extension point for a future pinned-host-key SSH/SFTP implementation.

    This class deliberately cannot execute arbitrary commands and makes no network calls yet.
    It may only implement the fixed wrapper contract after Gaia lab validation.
    """

    def status(self, member_name: str) -> FirewallStatus:
        raise NotImplementedError("SSH integration requires validated Gaia wrapper commands")

    def validate_configuration(
        self, member_name: str, content: str, sha256: str
    ) -> FirewallOperationResult:
        raise NotImplementedError("SSH integration requires validated Gaia wrapper commands")

    def install_configuration(
        self, member_name: str, content: str, sha256: str, deployment_id: str
    ) -> FirewallOperationResult:
        raise NotImplementedError("Real deployment is explicitly out of scope")

    def rollback(self, member_name: str, backup_id: str) -> FirewallOperationResult:
        raise NotImplementedError("Real rollback is explicitly out of scope")
