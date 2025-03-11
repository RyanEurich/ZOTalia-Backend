from pydoc import Helper
from typing import List
from fastapi import APIRouter, HTTPException
import logging
from ..config import supabase
from ..models.applicationsSchema import CreateApplicationSchema, UpdateApplicationSchema, ResponseApplicationSchema
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
router = APIRouter(prefix="/applications", tags=["applications"])
APPPLICATION_TABLE:str = 'applications'
APPLICATION_ID:str = 'application_id'
WORKER_ID:str = 'worker_id'
GIG_TABLE:str = 'gig'

@router.get("/", response_model=list[ResponseApplicationSchema])
async def get_applications()-> list[ResponseApplicationSchema]:
    try:
        result = supabase.table(APPPLICATION_TABLE).select('*').execute()
        return result.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/{applications_id}", response_model=ResponseApplicationSchema)
async def get_application(applications_id: str) -> ResponseApplicationSchema:
    try:
        result = supabase.table(APPPLICATION_TABLE).select('*').eq(APPLICATION_ID, applications_id).execute()
        return result.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
#to get the gig worker gig reviews 
@router.get("/worker/{worker_id}", response_model=float)
async def get_worker_gigs(worker_id: str) -> float:
    try:
        print(worker_id)
        result = supabase.table(APPPLICATION_TABLE).select('gig_id').eq(WORKER_ID, worker_id).execute()
        result_gig_ids = [i['gig_id'] for i in result.data]
        gig_review_result = supabase.table(GIG_TABLE).select('review').in_('gig_id',result_gig_ids).execute().data
        average_rating = sum([float(i['review']) for i in gig_review_result]) / len(gig_review_result)
        return average_rating
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/", response_model=ResponseApplicationSchema)
async def create_application(application: CreateApplicationSchema) -> ResponseApplicationSchema:
    try:
        logger.info(application.model_dump())
        result =  supabase.table(APPPLICATION_TABLE).insert(application.model_dump(exclude_unset=True)).execute()
        logger.info(result)
        return result.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/{applications_id}", response_model=ResponseApplicationSchema)
async def update_application(applications_id: str, application:  UpdateApplicationSchema) -> ResponseApplicationSchema:
    try:
        result = supabase.table(APPPLICATION_TABLE).update(application.model_dump(exclude_unset=True)).eq(APPLICATION_ID, applications_id).execute()
        return result.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#not in use
@router.delete("/{applications_id}")
async def delete_application(applications_id: str):
    try:
        result = supabase.table(APPPLICATION_TABLE).delete().eq(APPLICATION_ID, applications_id).execute()
        return {"message": "Application deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


    


