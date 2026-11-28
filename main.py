from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.config import settings
from app.modules.members.router import router as member_router
from app.modules.clients.router import router as client_router
from app.modules.admins.router import router as admin_router
from app.core.auth.router import router as auth_router
from app.core.redis import (
    connect_redis,
    close_redis,
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_redis()

    try:
        yield
    finally:
        await close_redis()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

app.include_router(member_router,prefix=settings.API_V1_PREFIX)
app.include_router(client_router,prefix=settings.API_V1_PREFIX)
app.include_router(admin_router,prefix=settings.API_V1_PREFIX)
app.include_router(auth_router,prefix=settings.API_V1_PREFIX)

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": settings.APP_NAME
    }
