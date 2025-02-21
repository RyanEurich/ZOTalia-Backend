from pydoc import Helper
from fastapi import APIRouter, HTTPException
import logging
from ..config import supabase
from ..models.employersSchemas import CreateEmployerSchema, UpdateEmployerSchema, ResponseEmployerSchema
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
router = APIRouter(prefix="/employers", tags=["employers"])
CLIENT_TABLE:str = 'client'
CLIENT_ID:str = 'client_id'

@router.get("/", response_model=list[ResponseEmployerSchema])
async def get_employers()-> list[ResponseEmployerSchema]:
    try:
        result = supabase.table(CLIENT_TABLE).select('*').execute()
        return result.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/{client_id}", response_model=ResponseEmployerSchema)
async def get_employer(client_id: str) -> ResponseEmployerSchema:
    try:
        result = supabase.table(CLIENT_TABLE).select('*').eq(CLIENT_ID, client_id).execute()
        return result.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=ResponseEmployerSchema)
async def create_employer(employer: CreateEmployerSchema) -> ResponseEmployerSchema:
    try:
        logger.info(employer.model_dump())
        result =  supabase.table(CLIENT_TABLE).insert(employer.model_dump(exclude_unset=True)).execute()
        logger.info(result)
        return result.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{client_id}", response_model=ResponseEmployerSchema)
async def update_employer(client_id: str, employer: UpdateEmployerSchema) -> ResponseEmployerSchema:
    try:
        new_count,new_rating=update_company_rating(client_id,employer)
        employer.company_rating=new_rating
        employer.individual_ratings=new_count

        result = supabase.table(CLIENT_TABLE).update(employer.model_dump(exclude_unset=True)).eq(CLIENT_ID, client_id).execute()
        return result.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#helper method to average company ratings
def update_company_rating(client_id: str, employer: UpdateEmployerSchema):
    
    updated_rating_count = supabase.table(CLIENT_TABLE) \
    .select('*') \
    .eq('client_id', client_id) \
    .execute()
        #then calcuating new rating average
    print(updated_rating_count)
    print(updated_rating_count.data[0]['individual_ratings'])
    if updated_rating_count.data[0]['individual_ratings']==None:
        current_count=1
        print('in first if')
    else:
        current_count= updated_rating_count.data[0]['individual_ratings']
    if updated_rating_count.data[0]['company_rating']==None:
        current_average=0
    else:
        current_average=updated_rating_count.data[0]['company_rating']

        # Formula: new_avg = (old_avg * old_count + new_rating) / (old_count + 1)
    new_count = current_count + 1
    new_average = ((current_average * current_count) + employer.company_rating) / new_count

        # Update both the count and average
    return new_count,new_average