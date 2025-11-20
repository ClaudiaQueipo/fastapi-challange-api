from collections.abc import AsyncGenerator
from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.schemas import Token, UserCreate, UserLogin, UserResponse
from app.auth.services import AuthService
from app.core.db import async_session
from app.core.exceptions import AuthenticationFailedError, ResourceAlreadyExistsError
from app.core.settings import settings

router = APIRouter(prefix="/auth", tags=["auth"])


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


@router.post("/register", response_model=UserResponse, status_code=201)
async def register_user(
    user_data: UserCreate,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> UserResponse:
    auth_service = AuthService(session)
    existing_user = await auth_service.get_user_by_email(user_data.email)
    if existing_user:
        raise ResourceAlreadyExistsError("Email already registered")
    user = await auth_service.create_user(user_data)
    return UserResponse.model_validate(user)


@router.post("/login", response_model=Token)
async def login_for_access_token(
    login_data: UserLogin,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> Token:
    auth_service = AuthService(session)
    user = await auth_service.authenticate_user(login_data)
    if not user:
        raise AuthenticationFailedError("Incorrect email or password")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_service.create_access_token(
        data={"sub": str(user.entity_id)}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token)
