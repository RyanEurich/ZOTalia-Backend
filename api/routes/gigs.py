from datetime import datetime
import re
import logging
from typing import Optional
from uuid import UUID
from fastapi import APIRouter, File, HTTPException, UploadFile
from ..config import supabase
from ..models.gigSchema import createGigSchema, updateGigSchema, responseGigSchema

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
router = APIRouter(prefix="/gigs", tags=["gigs"])
GIG_TABLE:str = 'gig'
GIG_ID:str = 'gig_id'

@router.get("/", response_model=list[responseGigSchema])
async def get_gigs()-> list[responseGigSchema]:
    try:
        result = supabase.table(GIG_TABLE).select('*').execute()
        print(type(result))
        return result.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/{gig_id}", response_model=responseGigSchema)
async def get_gig(gig_id: str) -> responseGigSchema:
    try:
        result = supabase.table(GIG_TABLE).select('*').eq(GIG_ID, gig_id).execute()
        return result.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=responseGigSchema)
async def create_gig(gig: createGigSchema) -> responseGigSchema:
    try:
        logger.info(gig.model_dump())
        result =  supabase.table(GIG_TABLE).insert(gig.model_dump(exclude_unset=True)).execute()
        logger.info(result)
        return result.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{gig_id}", response_model=responseGigSchema)
async def update_gig(gig_id: str, gig: updateGigSchema) -> responseGigSchema:
    try:
        print(gig.model_dump(exclude_unset=True,serialize_as_any=True))
        result = supabase.table(GIG_TABLE).update(gig.model_dump(exclude_unset=True)).eq(GIG_ID, gig_id).execute()
        return result.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.delete("/{gig_id}")
async def delete_gig(gig_id: str):
    try:
        result = supabase.table(GIG_TABLE).delete().eq(GIG_ID, gig_id).execute()
        return {"message": "Gig deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))