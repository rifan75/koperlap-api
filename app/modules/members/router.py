from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.modules.members.schemas import (
    MemberCreate,
    MemberResponse
)
from app.modules.members.service import MemberService


router = APIRouter(
    prefix="/members",
    tags=["Members"]
)


@router.post(
    "/",
    response_model=MemberResponse,
    status_code=201
)
def create_member(
    payload: MemberCreate,
    db: Session = Depends(get_db)
):
    service = MemberService(db)

    try:
        return service.create_member(payload)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.get("/", response_model=list[MemberResponse])
def get_members(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    service = MemberService(db)
    return service.get_members(skip, limit)