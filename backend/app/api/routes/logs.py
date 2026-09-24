from fastapi import APIRouter

router = APIRouter()


@router.get("")
def list_logs() -> list[object]:
    return []
