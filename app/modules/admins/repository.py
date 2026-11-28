from sqlalchemy.orm import Session

from app.modules.admins.models import Admin


class AdminRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, admin: Admin):
        self.db.add(admin)
        self.db.flush()
        return admin

    def get_by_email(self, email: str):
        return (
            self.db.query(Admin)
            .filter(Admin.email == email)
            .first()
        )

    def get_all(self, skip: int = 0, limit: int = 20):
        return (
            self.db.query(Admin)
            .offset(skip)
            .limit(limit)
            .all()
        )