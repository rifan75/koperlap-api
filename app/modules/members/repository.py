from sqlalchemy.orm import Session

from app.modules.members.models import Member


class MemberRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, member: Member):
        self.db.add(member)
        self.db.flush()
        return member

    def get_by_email(self, email: str):
        return (
            self.db.query(Member)
            .filter(Member.email == email)
            .first()
        )

    def get_all(self, skip: int = 0, limit: int = 20):
        return (
            self.db.query(Member)
            .offset(skip)
            .limit(limit)
            .all()
        )