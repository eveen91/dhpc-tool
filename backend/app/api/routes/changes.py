from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("")
def list_changes() -> list[object]:
    return []


@router.post("/{change_id}/validate", status_code=501)
def validate_change(change_id: str) -> None:
    del change_id
    raise HTTPException(status_code=501, detail="Change workflow is not implemented")


@router.post("/{change_id}/approve", status_code=501)
def approve_change(change_id: str) -> None:
    del change_id
    raise HTTPException(status_code=501, detail="Approval workflow is not implemented")


@router.post("/{change_id}/deploy", status_code=501)
def deploy_change(change_id: str) -> None:
    del change_id
    raise HTTPException(status_code=501, detail="Real deployment is disabled")
