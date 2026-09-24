from collections.abc import Callable
from functools import wraps

from fastapi import HTTPException, status

from app.schemas.auth import AuthenticatedUser, Role


def require_roles(*allowed_roles: Role) -> Callable[..., object]:
    """Provider-neutral RBAC guard. Authentication provider will supply the user later."""

    def decorator(function: Callable[..., object]) -> Callable[..., object]:
        @wraps(function)
        def wrapper(*args: object, current_user: AuthenticatedUser, **kwargs: object) -> object:
            if not set(current_user.roles).intersection(allowed_roles):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions",
                )
            return function(*args, current_user=current_user, **kwargs)

        return wrapper

    return decorator
