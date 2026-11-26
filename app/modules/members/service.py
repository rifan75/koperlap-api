from uuid import uuid4

from sqlalchemy.orm import Session

from app.modules.members.models import Member
from app.modules.members.schemas import MemberCreate
from app.modules.members.repository import MemberRepository


class MemberService:

    def __init__(self, db: Session):
        self.repository = MemberRepository(db)
        self.db = db

    def create_member(self, payload: MemberCreate):

        existing = self.repository.get_by_email(
            payload.email
        )

        if existing:
            raise ValueError("Email sudah terdaftar")

        member = Member(
            member_number=f"MBR-{uuid4().hex[:10].upper()}",
            full_name=payload.full_name,
            email=payload.email,
            phone_number=payload.phone_number
        )

        try:
            self.repository.create(member)
            self.db.commit()
            self.db.refresh(member)

            return member

        except Exception:
            self.db.rollback()
            raise

    def get_members(self, skip=0, limit=20):
        return self.repository.get_all(skip, limit)