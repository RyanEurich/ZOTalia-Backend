from pydantic import BaseModel, field_serializer, field_validator
from uuid import UUID
from datetime import datetime
from typing import Optional


class BaseEmployerSchema(BaseModel):
    client_id: Optional[UUID] = None
    created_at: Optional[datetime] = None
    user_id: Optional[UUID] = None
    company_name: Optional[str] = None
    company_description: Optional[str] = None
    #don't touch, automatically calculated and updated
    company_rating: Optional[float] = None
    individual_ratings: Optional[float] = 0

    @field_serializer('client_id')
    def serialize_client_id(self, client_id: UUID) -> str:
        return str(client_id)
    
    @field_serializer('created_at')
    def serialize_created_at(self, created_at: datetime) -> str:
        return created_at.isoformat()
    
    @field_serializer('user_id')
    def serialize_user_id(self, user_id: UUID) -> str:
        return str(user_id)
    
    @field_validator('company_rating')
    def validate_company_rating(cls, value):
        if value is not None and (value < 0 or value > 5):
            raise ValueError('Company rating must be between 0 and 5')
        return value 

class CreateEmployerSchema(BaseEmployerSchema):
    created_at: datetime = None
    user_id: UUID = None
    company_name: str = None
    company_description: str = None
    company_rating: float = 0.00

class UpdateEmployerSchema(BaseEmployerSchema):
    individual_ratings: float = None

class ResponseEmployerSchema(BaseEmployerSchema):
    client_id: UUID = None
    created_at: datetime = None
    user_id: UUID = None
    company_name: str = None
    company_description: str = None
    company_rating: float = None

    
