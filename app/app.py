from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth.routes import router as auth_router
from app.core.exception_handlers import (
    auth_failed_handler,
    global_exception_handler,
    permission_denied_handler,
    resource_exists_handler,
    resource_not_found_handler,
)
from app.core.exceptions import (
    AuthenticationFailedError,
    PermissionDeniedError,
    ResourceAlreadyExistsError,
    ResourceNotFoundError,
)
from app.core.settings import settings
from app.posts.routes import router as posts_router
from app.tags.routes import router as tags_router


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        debug=settings.DEBUG,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_exception_handler(ResourceNotFoundError, resource_not_found_handler)
    app.add_exception_handler(ResourceAlreadyExistsError, resource_exists_handler)
    app.add_exception_handler(PermissionDeniedError, permission_denied_handler)
    app.add_exception_handler(AuthenticationFailedError, auth_failed_handler)
    app.add_exception_handler(Exception, global_exception_handler)

    app.include_router(auth_router, prefix=settings.API_V1_PREFIX)
    app.include_router(posts_router, prefix=settings.API_V1_PREFIX)
    app.include_router(tags_router, prefix=settings.API_V1_PREFIX)

    @app.get("/")
    async def root():
        return {
            "message": "Welcome to FastAPI Challenge API",
            "version": settings.APP_VERSION,
            "environment": settings.ENVIRONMENT,
        }

    @app.get("/health")
    async def health_check():
        return {"status": "healthy"}

    return app


app = create_app()
