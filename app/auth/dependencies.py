from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.auth.models import User
from app.auth.services import AuthService
from app.core.db import async_session
from app.core.exceptions import AuthenticationFailedError

bearer_scheme = HTTPBearer()


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
) -> User:
    token = credentials.credentials
    try:
        import jwt

        from app.core.settings import settings

        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise AuthenticationFailedError("Could not validate credentials")
        from uuid import UUID

        user_uuid = UUID(user_id)
    except jwt.PyJWTError:
        raise AuthenticationFailedError("Could not validate credentials") from None

    async with async_session() as session:
        auth_service = AuthService(session)
        user = await auth_service.get_user_by_id(user_uuid)
        if user is None:
            raise AuthenticationFailedError("Could not validate credentials")
    return user
