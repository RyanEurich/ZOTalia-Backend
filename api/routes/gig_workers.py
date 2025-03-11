from datetime import datetime
import re
import logging
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, File, HTTPException, UploadFile
from ..config import supabase
from ..models.gigWorkerSchemas import CreateGigWorkerSchema, UpdateGigWorkerSchema, ResponseGigWorkerSchema, ResponseWorkerReviewSchema

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
router = APIRouter(prefix="/gig-workers", tags=["gig-workers"])
GIGWORKER_TABLE:str = 'gig_worker'
GIGWORKER_ID:str = 'worker_id'
APPLICATION_TABLE:str = 'applications'
APPLICATION_ID:str = 'application_id'
GIG_TABLE:str = 'gig'
GIG_ID:str = 'gig_id'

@router.get("/", response_model=list[ResponseGigWorkerSchema])
async def get_gig_workers()-> list[ResponseGigWorkerSchema]:
    try:
        result = supabase.table(GIGWORKER_TABLE).select('*').execute()
        print(type(result))
        return result.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
       
@router.get("/{worker_id}", response_model=ResponseGigWorkerSchema)
async def get_gig_worker(worker_id: str) -> ResponseGigWorkerSchema:
    try:
        result = supabase.table(GIGWORKER_TABLE).select('*').eq(GIGWORKER_ID, worker_id).execute()
        return result.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=ResponseGigWorkerSchema)
async def create_gig_worker(gig_worker: CreateGigWorkerSchema) -> ResponseGigWorkerSchema:
    try:
        logger.info(gig_worker.model_dump())
        result =  supabase.table(GIGWORKER_TABLE).insert(gig_worker.model_dump(exclude_unset=True)).execute()
        logger.info(result)
        return result.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/{worker_id}", response_model=ResponseGigWorkerSchema)
async def update_gig_worker(worker_id: str, gig_worker: UpdateGigWorkerSchema) -> ResponseGigWorkerSchema:
    try:
        result = supabase.table(GIGWORKER_TABLE).update(gig_worker.model_dump(exclude_unset=True)).eq(GIGWORKER_ID, worker_id).execute()
        return result.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#not being used
@router.delete("/{worker_id}")
async def delete_gig_worker(worker_id: str):
    try:
        result = supabase.table(GIGWORKER_TABLE).delete().eq(GIGWORKER_ID, worker_id).execute()
        return {"message": "Gig Worker deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#when the employer wants to rate the gig worker
@router.get("/reviews/{worker_id}", response_model=List[ResponseWorkerReviewSchema])
async def get_gig_worker_reviews(worker_id:str) -> List[ResponseWorkerReviewSchema]:
    try:
        result = supabase.table(APPLICATION_TABLE).select('gig_id').eq(GIGWORKER_ID, worker_id).execute()
        print(result)
        result_gig_ids = [i['gig_id'] for i in result.data]
        print(result_gig_ids)
        gig_review_result = supabase.table(GIG_TABLE).select('gig_worker_review').in_('gig_id',result_gig_ids).execute().data
        print(gig_review_result)
        return gig_review_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#average rating that the employers give a gig worker
@router.get("/ratings_avg/{worker_id}", response_model=float)
async def get_gig_worker_ratings_avg(worker_id:str) -> float:
    try:
        result = supabase.table(APPLICATION_TABLE).select('gig_id').eq(GIGWORKER_ID, worker_id).execute()
        result_gig_ids = [i['gig_id'] for i in result.data]
        gig_review_result = supabase.table(GIG_TABLE).select('gig_worker_rating').in_('gig_id',result_gig_ids).execute().data
        average_rating = sum([i['gig_worker_rating'] for i in gig_review_result]) / len(gig_review_result)
        return average_rating
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#when the gig worker wants to rate the employer
@router.post("/gig/{gig_id}/leave_employer_review")
async def leave_worker_review(gig_id:str,review:str):
    try:
        result = supabase.table(GIG_TABLE).update({'company_review':review}).eq(GIG_ID, gig_id).execute()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/gig/{gig_id}/leave_employer_rating")
async def leave_worker_rating(gig_id:str,review:str):
    try:
        result = supabase.table(GIG_TABLE).update({'company_rating':review}).eq(GIG_ID, gig_id).execute()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))





