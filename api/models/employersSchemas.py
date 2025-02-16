from pydantic import BaseModel, field_serializer
from uuid import UUID
from datetime import datetime
from typing import Optional
from jobCategoriesSchema import CategoryType

class BaseEmployerSchema(BaseModel):
    client_id: Optional[UUID] = None
    created_at: Optional[datetime] = None
    user_id: Optional[UUID] = None
    company_name: Optional[str] = None
    company_description: Optional[str] = None
    company_rating: Optional[float] = None

    @field_serializer('client_id')
    def serialize_client_id(self, client_id: UUID) -> str:
        return str(client_id)
    
    @field_serializer('created_at')
    def serialize_created_at(self, created_at: datetime) -> str:
        return created_at.isoformat()
    
    @field_serializer('user_id')
    def serialize_user_id(self, user_id: UUID) -> str:
        return str(user_id)
    


class CreateEmployerSchema(BaseEmployerSchema):
    created_at: datetime = None
    user_id: UUID = None
    company_name: str = None
    company_description: str = None
    company_rating: float = None

class UpdateEmployerSchema(BaseEmployerSchema):
    pass

class ResponseEmployerSchema(BaseEmployerSchema):
    client_id: UUID = None
    created_at: datetime = None
    user_id: UUID = None
    company_name: str = None
    company_description: str = None
    company_rating: float = None
