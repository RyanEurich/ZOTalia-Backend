from pydantic import BaseModel, field_serializer
from uuid import UUID
from datetime import datetime
from typing import Optional

class BaseProfileSchema(BaseModel):
    id: Optional[UUID] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    website: Optional[str] = None
    is_employer: Optional[bool] = None
    expo_notifcation_token: Optional[str] = None
    age: Optional[int] = None
    phone_number: Optional[str] = None
    profile_email: Optional[str] = None

    @field_serializer('updated_at')
    def serialize_updated_at(self, dt: datetime) -> str:
        return dt.isoformat()

class CreateProfileSchema(BaseProfileSchema):
    id: UUID
    updated_at: datetime
    username: str = None
    full_name: str = None
    avatar_url: str = None
    website: str = None
    is_employer: Optional[bool] = None
    expo_notifcation_token: Optional[str] = None
    age: Optional[int] = None
    phone_number: Optional[str] = None
    profile_email: Optional[str] = None
    @field_serializer('id')
    def serialize_id(self, id: UUID) -> str:
        return str(id)

class UpdateProfileSchema(BaseProfileSchema):
    updated_at: Optional[datetime] = None

class ResponseProfileSchema(BaseProfileSchema):
    id: Optional[UUID] = None
