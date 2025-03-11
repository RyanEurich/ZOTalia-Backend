from enum import Enum
from pydantic import BaseModel, field_serializer, field_validator
from uuid import UUID
from datetime import datetime, date
from typing import Optional, Dict

class gigStatus(str, Enum):
    #draft and open refer to the status of the posting
    #draft means the gig poster is still working on the gig
    #open means the gig is open, same as the is_published
    draft = "draft"
    open = "open"
    #means the gig has been accepted and is in progress or completed
    in_progress = "in-progress"
    completed = "completed"
    

class baseGigSchema(BaseModel):
    gig_id: Optional[UUID] = None
    created_at: datetime = None
    title: str = None
    description: str = None
    category: str = None
    location: Dict = None
    payment_details: Dict = None
    status: gigStatus = "draft"
    start_date: date = None
    end_date: date = None
    is_published: bool = False
    notification_threashold: int = 10 #not in use anymore
    review: None = None #should be string 
    client_id: UUID = None
    company_rating: int = 0
    company_review: str = ""
    gig_worker_rating: int = 0
    gig_worker_review: str = ""


    @field_serializer('created_at')
    def serialize_worker_id(self, created_at: datetime) -> str:
        return str(created_at)
    

    
    @field_serializer('client_id')
    def serialize_client_id(self, client_id: UUID) -> str:
        return str(client_id)

    @field_serializer('start_date')
    def serialize_start_date(self, start_date: date) -> str:
        return str(start_date)
        
    @field_serializer('end_date')
    def serialize_end_date(self, end_date: date) -> str:
        return str(end_date)



class createGigSchema(baseGigSchema):
    #gig_id is auto generated by supabase
    pass

class updateGigSchema(baseGigSchema):
    gig_id: UUID = None
    @field_serializer('gig_id')
    def serialize_user_id(self, gig_id: UUID) -> str:
        return str(gig_id)
    

class responseGigSchema(baseGigSchema):
    gig_id: UUID = None
    @field_serializer('gig_id')
    def serialize_gig_id(self, gig_id: UUID) -> str:
        return str(gig_id)



