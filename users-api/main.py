from functools import lru_cache
from typing import Annotated
import fastapi as FastAPI
from fastapi.params import Depends
from fastapi.responses import JSONResponse

from src.api import users
from src.middlewares import error_handler
import config
import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s"
)

app = FastAPI.FastAPI()
app.include_router(users.router)
app.add_middleware(error_handler.ErrorHandlerMiddleware)
error_handler.setup_exception_handlers(app)

@lru_cache
def get_settings():
    return config.Settings()

@app.get("/info")
async def info(settings: Annotated[config.Settings,
Depends(get_settings)]):
    return {
        "application_version": settings.APPLICATION_VERSION,
        "test_mode": settings.TEST_MODE
    }

tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users.",
    }
]

app = FastAPI.FastAPI(title="Users Api",
                        description="Api for user management",
                        version="0.0.0",
                        contact={
                            "name": "Timur Tkachenko",
                            "email": "tymur.tkachenko@student.karazin.ua",
                        },
                        openapi_tags=tags_metadata)

from fastapi import FastAPI
from contextlib import asynccontextmanager
@asynccontextmanager
async def lifespan(app: FastAPI):
 print("Running startup logic before the service starts...")
 yield
 print("Running cleanup logic before shutting down...")
app = FastAPI(lifespan=lifespan)
@app.get("/")
async def read_root():
 return {"message": "FastAPI is running!"}


@app.get("/") 
async def read_root(): 
    return {"message": "FastAPI is running!"} 


async def startup_event():
   print("FastAPI is starting up...")

async def shutdown_event():
   print("FastAPI is shutting down...")
@app.get("/")
async def read_root():
 return {"message": "FastAPI is running!"}

app.include_router(users.router)