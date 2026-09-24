from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/{deployment_id}", status_code=501)
def get_deployment(deployment_id: str) -> None:
    del deployment_id
    raise HTTPException(status_code=501, detail="Deployment tracking is not implemented")


@router.post("/{deployment_id}/rollback", status_code=501)
def rollback_deployment(deployment_id: str) -> None:
    del deployment_id
    raise HTTPException(status_code=501, detail="Real rollback is disabled")
