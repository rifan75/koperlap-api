from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Response,
    Request,
)
from pydantic import BaseModel
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.dependencies import get_db
from app.core.redis import get_redis
from app.config import settings

from app.core.auth.authorization import (
    authorize,
    refresh_authorization,
)

class AuthorizeRequest(BaseModel):
    code: str
    code_verifier: str

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


def set_refresh_cookie(
    response: Response,
    refresh_token: str,
):
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="None",
        path="/auth",
        max_age=(
            settings.REFRESH_TOKEN_EXPIRE_DAYS * 86400
        ),
    )


def clear_refresh_cookie(response: Response):
    response.delete_cookie(
        key="refresh_token",
        path="/auth",
        httponly=True,
        secure=True,
        samesite="None",
    )


# =========================
# AUTHORIZE
# =========================

@router.post("/authorize")
async def authorize_endpoint(
    data: AuthorizeRequest,
    response: Response,
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis),
):

    result = await authorize(
        redis=redis,
        db=db,
        code=data.code,
        verifier=data.code_verifier,
    )

    # Store refresh token in HttpOnly cookie
    set_refresh_cookie(
        response,
        result["refresh_token"],
    )

    # Never return refresh token in JSON
    return {
        "access_token": result["access_token"],
        "token_type": result["token_type"],
        "expires_in": result["expires_in"],
        "user": result["user"],
    }


# =========================
# REFRESH
# =========================

@router.post("/refresh")
async def refresh_endpoint(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db),
):

    refresh_token = request.cookies.get(
        "refresh_token"
    )

    if not refresh_token:
        raise HTTPException(
            status_code=401,
            detail="Refresh token missing",
        )

    result = await refresh_authorization(
        db=db,
        refresh_token=refresh_token,
    )

    # Rotate cookie
    set_refresh_cookie(
        response,
        result["refresh_token"],
    )

    # Return access token only
    return {
        "access_token": result["access_token"],
        "token_type": "bearer",
        "expires_in": result["expires_in"],
        "user": result["user"],
    }
