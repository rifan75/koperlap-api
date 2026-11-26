from uuid import uuid4

from sqlalchemy.orm import Session

from app.modules.admin.models import Admin
from app.modules.admin.repository import AdminRepository
from app.modules.admin.schemas import AdminCreate


class AdminService:

    def __init__(self, db: Session):
        self.repository = AdminRepository(db)
        self.db = db

    def create_admin(self, payload: AdminCreate):

        existing = self.repository.get_by_email(
            payload.email
        )

        if existing:
            raise ValueError("Email sudah terdaftar")

        admin = Admin(
            admin_number=f"ADM-{uuid4().hex[:10].upper()}",
            full_name=payload.full_name,
            email=payload.email,
            phone_number=payload.phone_number
        )

        try:
            self.repository.create(admin)
            self.db.commit()
            self.db.refresh(admin)

            return admin

        except Exception:
            self.db.rollback()
            raise

    def get_admins(self, skip=0, limit=20):
        return self.repository.get_all(skip, limit)