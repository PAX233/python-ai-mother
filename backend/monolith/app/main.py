from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import get_settings
from app.core.exception_handlers import register_exception_handlers

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
)

register_exception_handlers(app)
app.include_router(api_router, prefix=settings.api_prefix)

