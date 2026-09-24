from fastapi import APIRouter

router = APIRouter()


@router.get("/status")
def cluster_status() -> dict[str, object]:
    return {"members": [], "state": "not_configured", "deployment_execution_enabled": False}


@router.get("/drift")
def configuration_drift() -> dict[str, object]:
    return {"state": "unknown", "reason": "Firewall access is not configured"}
