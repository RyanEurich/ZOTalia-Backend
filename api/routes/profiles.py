from datetime import datetime
from typing import Optional
from uuid import UUID
from fastapi import APIRouter, HTTPException
from ..config import supabase
from ..models.profileSchemas import CreateProfileSchema, UpdateProfileSchema, ResponseProfileSchema


router = APIRouter(prefix="/profiles", tags=["profiles"])

@router.get("/")
async def get_profiles(
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
        #not sure why the config isn't converting to strings
        print(profile.model_dump())
        result = supabase.table('profiles').insert(profile.model_dump()).execute()
        return result
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
    
