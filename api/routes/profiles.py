from datetime import datetime
import re
import logging
from typing import Optional
from uuid import UUID
from fastapi import APIRouter, File, HTTPException, UploadFile
from ..config import supabase
from ..models.profileSchemas import CreateProfileSchema, UpdateProfileSchema, ResponseProfileSchema

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
router = APIRouter(prefix="/profiles", tags=["profiles"])

def sanitize_filename(filename: str) -> str:
    # Replace spaces with underscores and remove special characters
    filename = re.sub(r'\s+', '_', filename)
    filename = re.sub(r'[^a-zA-Z0-9_.-]', '', filename)
    return filename
#for profile picture uplaod
@router.post("/upload-avatar")
async def upload_avatar(file: UploadFile = File(...)):
    try:
        # Upload the file to the Supabase bucket
        file_content = await file.read()
        file_name = f"avatars/{sanitize_filename(file.filename)}"
        result = supabase.storage.from_("avatars").upload(file_name, file_content)
        print(result)
        if result.error:
            raise HTTPException(status_code=500, detail=result.error.message)
        
        # Get the public URL of the uploaded file
        avatar_url = supabase.storage.from_("avatars").get_public_url(file_name)
        return {"avatar_url": avatar_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/download-avatar")    
async def download_avatar(file_name: str):
    try:
        # Get the public URL of the uploaded file
        avatar_url = supabase.storage.from_("avatars").get_public_url(file_name)
        return {"avatar_url": avatar_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#untested
@router.get("/filters")
async def get_profiles_filters(
    limit: int = 10,
    offset: int = 0,
    search: Optional[str] = None,
    sort: Optional[str] = "created_at",
    order: Optional[str] = "desc",
    is_employer: Optional[bool] = None,
    age: Optional[int] = None,
    min_age: Optional[int] = None,
    max_age: Optional[int] = None,
) -> list[ResponseProfileSchema]:

    try:
        query = supabase.table('profiles').select('*')

        if search: query = query.ilike('username', f'%{search}%')
        if is_employer: query = query.eq('is_employer', is_employer)
        if age: query = query.eq('age', age)
        if age:
            query = query.eq('age', age)
        else:
            # Only apply range filters if exact age is not provided
            if min_age:
                query = query.gte('age', min_age)
            if max_age:
                query = query.lte('age', max_age)
        if sort and order: query = query.order(sort, order=order)

        query = query.range(offset, offset + limit - 1)

        result = query.execute()

        return result.data or []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
async def get_profiles():
    try:
        result = supabase.table('profiles').select('*').execute()
        return result.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{profile_id}")
async def get_profile(profile_id: str) -> ResponseProfileSchema:
    try:
        result = supabase.table('profiles').select('*').eq('id', profile_id).execute()
        if not result.data:
            raise HTTPException(status_code=404, detail="Profile not found")
        return result.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/")
async def create_profile(profile: CreateProfileSchema):
    try:
        logger.info(profile.model_dump())
        #not sure why the config isn't converting to strings
        print(profile.model_dump())
        result = supabase.table('profiles').insert(profile.model_dump()).execute()
        logger.info(result)
        return result.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{profile_id}")
async def update_profile(profile_id: str, profile: UpdateProfileSchema) -> ResponseProfileSchema:
    try:
        result = supabase.table('profiles').update(profile.model_dump(exclude_unset=True)).eq('id', profile_id).execute()
        if not result.data:
            raise HTTPException(status_code=404, detail="Profile not found")
        return result.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#not being used
@router.delete("/{profile_id}")
async def delete_profile(profile_id: str):
    try:
        result = supabase.table('profiles').delete().eq('id', profile_id).execute()
        if not result.data:
            raise HTTPException(status_code=404, detail="Profile not found")
        return {"message": "Profile deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
