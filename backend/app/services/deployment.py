from dataclasses import dataclass
from uuid import UUID

from app.infrastructure.firewall.adapter import FirewallAdapter


@dataclass(frozen=True)
class DeploymentRequest:
    deployment_id: UUID
    configuration: str
    sha256: str


class DeploymentService:
    """Workflow boundary only. The real ClusterXL sequence is deferred pending lab validation."""

    def __init__(self, adapter: FirewallAdapter) -> None:
        self.adapter = adapter

    def run(self, request: DeploymentRequest) -> str:
        return "blocked: real firewall deployments are disabled in the skeleton"
