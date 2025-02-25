from pydantic import BaseModel, field_serializer, field_validator
from uuid import UUID
from datetime import datetime
from typing import Optional
from enum import Enum

class BaseFinancialSchema(BaseModel):
    account_id: UUID = None
    created_at: datetime = None
    amount: float = 0.00
    monthly_goals: dict = {} #some json stuff
    last_updated: datetime = None
    description: str = None
    worker_id: UUID = None
    gig_id: UUID = None

    @field_serializer('account_id')
    def serialize_account_id(self, account_id: UUID) -> str:
        return str(account_id)
    
    @field_serializer('created_at')
    def serialize_created_at(self, created_at: datetime) -> str:
        return created_at.isoformat()
    
    @field_serializer('last_updated')
    def serialize_updated_at(self, last_updated: datetime) -> str:
        return last_updated.isoformat()
    
    @field_serializer('worker_id')
    def serialize_worker_id(self, worker_id: UUID) -> str:
        return str(worker_id)
    
    @field_serializer('gig_id')
    def serialize_gig_id(self, gig_id: UUID) -> str:
        return str(gig_id)
    
class CreateFinancialSchema(BaseFinancialSchema):
    account_id: Optional[UUID] = None

class UpdateFinancialSchema(BaseFinancialSchema):
    pass

class ReturnFinancialSchema(BaseFinancialSchema):
    pass