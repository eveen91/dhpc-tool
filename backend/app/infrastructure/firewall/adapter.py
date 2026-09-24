from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import StrEnum


class FirewallRole(StrEnum):
    ACTIVE = "active"
    STANDBY = "standby"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class FirewallStatus:
    reachable: bool
    role: FirewallRole
    dhcp_healthy: bool
    checksum: str | None


@dataclass(frozen=True)
class FirewallOperationResult:
    succeeded: bool
    message: str
    backup_id: str | None = None


class FirewallAdapter(ABC):
    """Restricted firewall integration. Arbitrary commands and paths are intentionally absent."""

    @abstractmethod
    def status(self, member_name: str) -> FirewallStatus: ...

    @abstractmethod
    def validate_configuration(
        self, member_name: str, content: str, sha256: str
    ) -> FirewallOperationResult: ...

    @abstractmethod
    def install_configuration(
        self, member_name: str, content: str, sha256: str, deployment_id: str
    ) -> FirewallOperationResult: ...

    @abstractmethod
    def rollback(self, member_name: str, backup_id: str) -> FirewallOperationResult: ...
