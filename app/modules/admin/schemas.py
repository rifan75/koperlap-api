from pydantic import BaseModel, EmailStr, ConfigDict


class AdminCreate(BaseModel):
    full_name: str
    email: EmailStr
    phone_number: str


class AdminResponse(BaseModel):
    id: int
    admin_number: str
    full_name: str
    email: EmailStr
    phone_number: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)