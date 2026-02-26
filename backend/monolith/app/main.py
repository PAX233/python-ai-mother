from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import get_settings
from app.core.exception_handlers import register_exception_handlers
from app.core.logging_config import configure_logging
from app.core.middleware import register_middlewares
from app.core.resources import ResourceManager

settings = get_settings()
resources = ResourceManager(settings)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await resources.start()
    app.state.resources = resources
    try:
        yield
    finally:
        await resources.stop()


def create_app() -> FastAPI:
    configure_logging(settings.log_level)
    fastapi_app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
        lifespan=lifespan,
    )
    register_middlewares(fastapi_app, settings)
    register_exception_handlers(fastapi_app)
    fastapi_app.include_router(api_router, prefix=settings.api_prefix)
    return fastapi_app


app = create_app()
