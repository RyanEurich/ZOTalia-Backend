from pydantic import BaseModel, field_serializer, field_validator, model_validator
from uuid import UUID
from datetime import datetime
from typing import Optional
from enum import Enum

class BasePostInteractionSchema(BaseModel):
    id: Optional[UUID] = None
    created_at: datetime = None
    post_id: UUID = None
    user_id: UUID = None
    interaction_type: str = None
    interaction_details: dict = {}

    @field_serializer('id')
    def serialize_id(self, id: UUID) -> str:
        return str(id)
    
    @field_serializer('post_id')
    def serialize_post_id(self, post_id: UUID) -> str:
        return str(post_id)

    @field_serializer('user_id')
    def serialize_user_id(self, user_id: UUID) -> str:
        return str(user_id)

    @field_serializer('created_at')
    def serialize_created_at(self, created_at: datetime) -> str:
        return created_at.isoformat()
    

class CreatePostInteractionSchema(BasePostInteractionSchema):
    pass

class UpdatePostInteractionSchema(BasePostInteractionSchema):
    @field_validator('id', mode='before')
    def check_id(cls, v):
        if v is None:
            raise ValueError('id is required')
        return v
    pass

class ResponsePostInteractionSchema(BasePostInteractionSchema):
    @field_validator('id', mode='before')
    def check_id(cls, v):
        if v is None:
            raise ValueError('id is required')
        return v
