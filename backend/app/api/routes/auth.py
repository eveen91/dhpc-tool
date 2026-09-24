from fastapi import APIRouter, HTTPException, status

router = APIRouter()


@router.post("/login")
def login() -> None:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Authentication is provider-neutral and not configured in this skeleton",
    )


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout() -> None:
    return None
