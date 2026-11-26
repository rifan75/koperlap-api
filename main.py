from fastapi import FastAPI
from app.config import settings
from app.modules.members.router import router as member_router
from app.modules.clients.router import router as client_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION
)

app.include_router(member_router,prefix=settings.API_V1_PREFIX)
app.include_router(client_router,prefix=settings.API_V1_PREFIX)

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": settings.APP_NAME
    }
