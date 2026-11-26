from sqlalchemy.orm import Session

from app.modules.clients.models import Client


class ClientRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, client: Client):
        self.db.add(client)
        self.db.flush()
        return client

    def get_by_email(self, email: str):
        return (
            self.db.query(Client)
            .filter(Client.email == email)
            .first()
        )

    def get_all(self, skip: int = 0, limit: int = 20):
        return (
            self.db.query(Client)
            .offset(skip)
            .limit(limit)
            .all()
        )