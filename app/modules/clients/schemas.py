import uuid

from pydantic import BaseModel, EmailStr, ConfigDict


class ClientCreate(BaseModel):
    full_name: str
    email: EmailStr
    phone_number: str


class ClientResponse(BaseModel):
    id: int
    client_number: str
    full_name: str
    email: EmailStr
    phone_number: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)