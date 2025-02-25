from pydantic import BaseModel, field_serializer, field_validator
from uuid import UUID
from datetime import datetime
from typing import Optional
from enum import Enum

class BaseDocumentSchema(BaseModel):
    document_id: UUID = None
    created_at: datetime = None
    type: str = None
    uploaded_at: datetime = None
    application_id: UUID = None
    url: str = None
    storage_path: str = None

    @field_serializer('document_id')
    def serialize_document_id(self, document_id: UUID) -> str:
        return str(document_id)
    
    @field_serializer('created_at')
    def serialize_created_at(self, created_at: datetime) -> str:
        return created_at.isoformat()
    
    @field_serializer('uploaded_at')
    def serialize_updated_at(self, uploaded_at: datetime) -> str:
        return uploaded_at.isoformat()
    
    @field_serializer('application_id')
    def serialize_application_id(self, application_id: UUID) -> str:
        return str(application_id)
    
class CreateDocumentSchema(BaseDocumentSchema):
    pass

class UpdateDocumentSchema(BaseDocumentSchema):
    pass

class ReturnDocumentSchema(BaseDocumentSchema):
    pass
