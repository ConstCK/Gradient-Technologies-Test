from contextlib import asynccontextmanager

import uvicorn
from fastapi import APIRouter, FastAPI

from core.config.settings import get_settings, setup_logging
from core.database import Base, engine
from controllers.health_controller import router as health_router
from controllers.link_controller import router as link_router
import models.link  # noqa: F401 — регистрация модели в Base.metadata


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    setup_logging(settings.log_level)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    pass


app = FastAPI(
    title=get_settings().app_name,
    lifespan=lifespan,
)

main_router = APIRouter()
main_router.include_router(health_router)
main_router.include_router(link_router)
app.include_router(main_router, prefix='/api/v1')


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
