from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI

from core.config.settings import get_settings, setup_logging
from controllers.health_controller import router as health_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    setup_logging(settings.log_level)
    yield
    pass


app = FastAPI(
    title=get_settings().app_name,
    lifespan=lifespan,
)
app.include_router(health_router)


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
