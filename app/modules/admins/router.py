from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.principal import Principal

from app.core.dependencies import (
    get_current_principal,
    require_permission,
)

from app.database.dependencies import get_db
from app.modules.admins.schemas import (
    AdminCreate,
    AdminResponse
)
from app.modules.admins.service import AdminService
from app.modules.admins.auth.router import router as auth_router


router = APIRouter(
    prefix="/admins",
    tags=["Admins"],
    # dependencies=[
    #     Depends(require_permission("users.read"))
    # ],
)

router.include_router(auth_router)


@router.post(
    "/",
    response_model=AdminResponse,
    status_code=201
)
def create_admin(
    # payload: AdminCreate = Depends(
    #     require_permission("users.write")
    # ),
    payload: AdminCreate,
    db: Session = Depends(get_db)
):
    service = AdminService(db)

    try:
        return service.create_admin(payload)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.get("/", response_model=list[AdminResponse])
def get_admins(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    _: dict = Depends(
        require_permission("users.read")
    ),
):
    service = AdminService(db)
    return service.get_admins(skip, limit)


