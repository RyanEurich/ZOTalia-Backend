from pydantic import BaseModel, field_serializer, field_validator, model_validator
from uuid import UUID
from datetime import datetime
from typing import Optional
from enum import Enum

class BasePostSchema(BaseModel):
    id:Optional[UUID] = None
    created_at: datetime = None
    updated_at: Optional[datetime] = None
    user_id: UUID = None
    post_title: str = None
    post_content: str = None
    images: dict = {}
    links: dict = {}

    @field_serializer('id')
    def serialize_id(self, id: UUID) -> str:
        return str(id)

    @field_serializer('user_id')
    def serialize_user_id(self, user_id: UUID) -> str:
        return str(user_id)

    @field_serializer('created_at')
    def serialize_created_at(self, created_at: datetime) -> str:
        return created_at.isoformat()
    
    @field_serializer('updated_at')
    def serialize_updated_at(self, updated_at: datetime) -> str:
        return updated_at.isoformat()
    
    @field_validator('id', mode='before')
    def check_id(cls, v):
        if v is None:
            raise ValueError('id is required')
        return v


class CreatePostSchema(BasePostSchema):
    pass
    
class UpdatePostSchema(BasePostSchema):
    @field_validator('id', mode='before')
    def check_id(cls, v):
        if v is None:
            raise ValueError('id is required')
        return v

class ResponsePostSchema(BasePostSchema):
    @field_validator('id', mode='before')
    def check_id(cls, v):
        if v is None:
            raise ValueError('id is required')
        return v
