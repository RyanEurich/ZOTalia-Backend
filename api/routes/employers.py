from fastapi import APIRouter, HTTPException
from ..config import supabase
from ..models.schemas import ProfileSchema

router = APIRouter(prefix="/employers", tags=["employers"])

@router.get("/")
async def get_profiles():
    try:
        result = supabase.table('profiles').select('*').execute()
        return result.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))