import logging
from functools import lru_cache
from typing import Annotated
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from src.api import users
from src.middlewares import error_handler
from src.models.user import UserService, User
import config

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("api")

@lru_cache
def get_settings():
    return config.Settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    logger.info(f"service started, test mode: {settings.TEST_MODE}")
    
    if settings.TEST_MODE:
        service = UserService()
        service.create_user(User(
            firstName="Test", 
            lastName="User", 
            birthday="2000-01-01"
        ))
        logger.info("test data loaded")
        
    yield
    logger.info("service shutdown")

app = FastAPI(
    title="Users Api",
    description="api for user management",
    version="1.0.1",
    contact={
        "name": "Timur Tkachenko",
        "email": "tymur.tkachenko@student.karazin.ua",
    },
    lifespan=lifespan
)

app.include_router(users.router)
app.add_middleware(error_handler.ErrorHandlerMiddleware)
error_handler.setup_exception_handlers(app)

@app.get("/info", tags=["system"])
async def info(settings: Annotated[config.Settings, Depends(get_settings)]):
    return {
        "application_version": settings.APPLICATION_VERSION,
        "test_mode": settings.TEST_MODE
    }