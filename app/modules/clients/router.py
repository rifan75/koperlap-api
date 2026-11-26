from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.modules.clients.schemas import (
    ClientCreate,
    ClientResponse
)
from app.modules.clients.service import ClientService


router = APIRouter(
    prefix="/clients",
    tags=["Clients"]
)


@router.post(
    "/",
    response_model=ClientResponse,
    status_code=201
)
def create_client(
    payload: ClientCreate,
    db: Session = Depends(get_db)
):
    service = ClientService(db)

    try:
        return service.create_client(payload)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.get("/", response_model=list[ClientResponse])
def get_clients(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    service = ClientService(db)
    return service.get_clients(skip, limit)