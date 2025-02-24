from datetime import datetime
import re
import logging
from typing import Optional
from uuid import UUID
from fastapi import APIRouter, File, HTTPException, UploadFile
from ..config import supabase
from ..models.gigWorkerSchemas import CreateGigWorkerSchema, UpdateGigWorkerSchema, ResponseGigWorkerSchema

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
router = APIRouter(prefix="/gig-workers", tags=["gig-workers"])
GIGWORKER_TABLE:str = 'gig_worker'
GIGWORKER_ID:str = 'worker_id'

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
    




