from fastapi import APIRouter, HTTPException, status

from app.schemas.hosts import HostCreate

router = APIRouter()


@router.get("")
def list_hosts() -> list[object]:
    return []


@router.post("", status_code=status.HTTP_501_NOT_IMPLEMENTED)
def create_host(payload: HostCreate) -> None:
    del payload
    raise HTTPException(
        status_code=501, detail="Persistence workflow is not implemented in the skeleton"
    )


@router.get("/{host_id}", status_code=status.HTTP_501_NOT_IMPLEMENTED)
def get_host(host_id: str) -> None:
    del host_id
    raise HTTPException(status_code=501, detail="Host retrieval is not implemented")
