import uuid

from pydantic import BaseModel, EmailStr, ConfigDict


class MemberCreate(BaseModel):
    full_name: str
    email: EmailStr
    phone_number: str


class MemberResponse(BaseModel):
    id: uuid.UUID
    member_number: str
    full_name: str
    email: EmailStr
    phone_number: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)