from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    AuthenticationFailedError,
    PermissionDeniedError,
    ResourceAlreadyExistsError,
    ResourceNotFoundError,
)


def resource_not_found_handler(_request: Request, exc: ResourceNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND, content={"detail": exc.message}
    )


def resource_exists_handler(_request: Request, exc: ResourceAlreadyExistsError):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT, content={"detail": exc.message}
    )


def permission_denied_handler(_request: Request, _exc: PermissionDeniedError):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"detail": "You are not allowed to perform this action."},
    )


def auth_failed_handler(_request: Request, exc: AuthenticationFailedError):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": exc.message},
        headers={"WWW-Authenticate": "Bearer"},
    )


def global_exception_handler(_request: Request, _exc: Exception):
    # TODO: Add a log here when the logger instance is configured

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error."},
    )
