from pydantic import BaseModel, field_serializer, field_validator, model_validator
from uuid import UUID
from datetime import datetime
from typing import Optional
from enum import Enum

class BaseFollowSchema(BaseModel):
    followed_id: UUID = None
    follower_id: UUID = None

    @field_serializer('followed_id')
    def serialize_following_id(self, followed_id: UUID) -> str:
        return str(followed_id)
    
    @field_serializer('follower_id')
    def serialize_follower_id(self, follower_id: UUID) -> str:
        return str(follower_id)

class CreateFollowSchema(BaseFollowSchema):
    pass

class UpdateFollowSchema(BaseFollowSchema):
    pass

class ReturnFollowSchema(BaseFollowSchema):
    pass

class FollowerCountSchema(BaseModel):
    follower_id: UUID = None
    follower_count: int = 0

    @field_serializer('follower_id')
    def serialize_follower_id(self, follower_id: UUID) -> str:
        return str(follower_id)
    
class FollowedCountSchema(BaseModel):
    followed_id: UUID = None
    followed_count: int = 0

    @field_serializer('followed_id')
    def serialize_follower_id(self, followed_id: UUID) -> str:
        return str(followed_id)
