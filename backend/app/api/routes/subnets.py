from fastapi import APIRouter, HTTPException

from app.schemas.subnets import SubnetCreate

router = APIRouter()


@router.get("")
def list_subnets() -> list[object]:
    return []


@router.post("", status_code=501)
def create_subnet(payload: SubnetCreate) -> None:
    del payload
    raise HTTPException(
        status_code=501, detail="Persistence workflow is not implemented in the skeleton"
    )
