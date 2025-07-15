from fastapi import FastAPI
from app.db.connection import db_connection
from contextlib import asynccontextmanager
from app.services import common_services, geolocation, user, projects


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup code if needed
    yield
    # shutdown code
    await db_connection.dispose()

app = FastAPI(title="Reztic AI", version="1.0.0", lifespan=lifespan)

app.include_router(common_services.healthcheck.routers.router, prefix="/v1")
app.include_router(user.api.register.routers.router)
app.include_router(user.api.auth.routers.router)
app.include_router(common_services.upload.routers.router)
app.include_router(projects.api.create.routers.router)
app.include_router(projects.api.list.routers.router)
