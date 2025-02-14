from fastapi import APIRouter, HTTPException
from ..config import supabase
from ..models.schemas import ProfileSchema

router = APIRouter(prefix="/profiles", tags=["profiles"])

@router.get("/")
async def get_profiles():
    try:
        result = supabase.table('profiles').select('*').execute()
        return result.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{profile_id}")
async def get_profile(profile_id: str):
    try:
        result = supabase.table('profiles').select('*').eq('id', profile_id).execute()
        if not result.data:
            raise HTTPException(status_code=404, detail="Profile not found")
        return result.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/")
async def create_profile(profile: ProfileSchema):
    try:
        result = supabase.table('profiles').insert(profile.dict()).execute()
        return result.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{profile_id}")
async def update_profile(profile_id: str, profile: ProfileSchema):
    try:
        result = supabase.table('profiles').update(profile.dict()).eq('id', profile_id).execute()
        if not result.data:
            raise HTTPException(status_code=404, detail="Profile not found")
        return result.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{profile_id}")
async def delete_profile(profile_id: str):
    try:
        result = supabase.table('profiles').delete().eq('id', profile_id).execute()
        if not result.data:
            raise HTTPException(status_code=404, detail="Profile not found")
        return {"message": "Profile deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))