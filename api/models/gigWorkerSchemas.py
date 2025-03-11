from pydantic import BaseModel, field_serializer
from uuid import UUID
from datetime import datetime
from typing import Dict, Optional
from .jobCategoriesSchema import CategoryType

class BaseGigWorkerSchema(BaseModel):
    worker_id: Optional[UUID] = None
    created_at: Optional[datetime] = None
    user_id: UUID = None
    specialties: Optional[CategoryType] = None
    #need to figure out this json
    work_preferences: Optional[Dict[str, Dict[str, bool]]] = None
    rating: Optional[float] = None
    main_job_specialty: Optional[CategoryType] = None
    first_alternative_specialty: Optional[CategoryType] = None
    secondary_job_specialty: Optional[CategoryType] = None
    work_duration_singleDay: Optional[bool] = None
    work_duration_shortTerm: Optional[bool] = None
    work_duration_hourly: Optional[bool] = None
    job_is_remote: Optional[bool] = None
    pay_rate_total: Optional[int] = None
    pay_rate_hourly: Optional[int] = None    


class CreateGigWorkerSchema(BaseGigWorkerSchema):
    #worker_id is auto generated
    created_at: datetime = None
    user_id: UUID = None
    specialties: CategoryType = None
    #need to figure out this json
    work_preferences: list[str] = None
    rating: float = None
    main_job_specaialty: CategoryType = None
    first_alternative_specialty: CategoryType = None
    secondary_job_specialty: CategoryType = None
    work_duration_singleDay: bool = None
    work_duration_shortTerm: bool = None
    work_duration_hourly: bool = None
    job_is_remote: bool = None
    pay_rate_total: float = None
    pay_rate_hourly: float = None    

    @field_serializer('created_at')
    def serialize_worker_id(self, created_at: datetime) -> str:
        return str(created_at)
    
    @field_serializer('user_id')
    def serialize_user_id(self, user_id: UUID) -> str:
        return str(user_id)
    




class UpdateGigWorkerSchema(BaseGigWorkerSchema):
    worker_id: UUID = None

    @field_serializer('worker_id')
    def serialize_worker_id(self, worker_id: UUID) -> str:
        return str(worker_id)




class ResponseGigWorkerSchema(BaseGigWorkerSchema):
    worker_id: UUID = None

    
class ResponseWorkerReviewSchema(BaseModel):
    gig_worker_review:str = ""

