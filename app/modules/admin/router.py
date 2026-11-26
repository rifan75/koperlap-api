from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.modules.admin.schemas import (
    AdminCreate,
    AdminResponse
)
from app.modules.admin.service import AdminService


router = APIRouter(
    prefix="/admins",
    tags=["Admins"]
)


@router.post(
    "/",
    response_model=AdminResponse,
    status_code=201
)
def create_admin(
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
    db: Session = Depends(get_db)
):
    service = AdminService(db)
    return service.get_admins(skip, limit)