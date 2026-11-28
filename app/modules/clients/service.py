from uuid import uuid4

from sqlalchemy.orm import Session

from app.modules.clients.models import Client
from app.modules.clients.repository import ClientRepository
from app.modules.clients.schemas import ClientCreate
from app.core.security import hash_password


class ClientService:

    def __init__(self, db: Session):
        self.repository = ClientRepository(db)
        self.db = db

    def create_client(self, payload: ClientCreate):

        existing = self.repository.get_by_email(
            payload.email
        )

        if existing:
            raise ValueError("Email sudah terdaftar")

        client = Client(
            client_number=f"CLI-{uuid4().hex[:10].upper()}",
            full_name=payload.full_name,
            email=payload.email,
            password=hash_password(payload.password),
            phone_number=payload.phone_number
        )

        try:
            self.repository.create(client)
            self.db.commit()
            self.db.refresh(client)

            return client

        except Exception:
            self.db.rollback()
            raise

    def get_clients(self, skip=0, limit=20):
        return self.repository.get_all(skip, limit)