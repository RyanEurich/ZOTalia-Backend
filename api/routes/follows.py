from datetime import datetime
import re
import logging
from typing import Optional
from uuid import UUID
from fastapi import APIRouter, File, HTTPException, UploadFile
from ..config import supabase
from ..models.followsSchema import CreateFollowSchema, UpdateFollowSchema, ReturnFollowSchema, FollowedCountSchema, FollowerCountSchema

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
router = APIRouter(prefix="/follows", tags=["follows"])
FOLLOWS_TABLE:str = 'follows'
FOLLOWER_ID:str = 'follower_id'
FOLLOWED_ID:str = 'followed_id'
PROFILE_ID:str = 'id'

@router.get("/{Profile_Id}/followed", response_model=list[ReturnFollowSchema])
async def get_followers(Profile_Id)-> list[ReturnFollowSchema]:
    try:
        result = supabase.table(FOLLOWS_TABLE).select('*').eq(FOLLOWED_ID,Profile_Id).execute()
        print(type(result))
        return result.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{Profile_Id}/followed/count", response_model=FollowedCountSchema)
async def get_countOf_followers(Profile_Id)-> FollowedCountSchema:
    try:
        result = supabase.table(FOLLOWS_TABLE).select('*', count="exact").eq(FOLLOWED_ID,Profile_Id).execute()
        return {"followed_id": Profile_Id,"followed_count": result.count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/{Profile_Id}/following", response_model=list[ReturnFollowSchema])
async def get_following(Profile_Id)-> list[ReturnFollowSchema]:
    try:
        result = supabase.table(FOLLOWS_TABLE).select('*').eq(FOLLOWER_ID,Profile_Id).execute()
        print(type(result))
        return result.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/{Profile_Id}/followers/count", response_model=FollowerCountSchema)
async def get_countOf_following(Profile_Id)-> FollowerCountSchema:
    try:
        result = supabase.table(FOLLOWS_TABLE).select('*', count="exact").eq(FOLLOWER_ID,Profile_Id).execute()
        print(type(result))
        return {"follower_id": Profile_Id,"follower_count": result.count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/", response_model=ReturnFollowSchema)
async def create_follow(follow: CreateFollowSchema) -> ReturnFollowSchema:
    try:
        logger.info(follow.model_dump())
        result =  supabase.table(FOLLOWS_TABLE).insert(follow.model_dump(exclude_unset=True)).execute()
        logger.info(result)
        return result.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.delete("/{Profile_Id}/unfollow/{Profile_Id2}")
async def delete_follow(Profile_Id: str, Profile_Id2: str):
    try:
        result = supabase.table(FOLLOWS_TABLE).delete().eq(FOLLOWER_ID, Profile_Id).eq(FOLLOWED_ID, Profile_Id2).execute()
        return {"message": "Follow deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/{Profile_Id}/isFollowing/{Profile_Id2}", response_model=bool)
async def isFollowing(Profile_Id: str, Profile_Id2: str):
    try:
        result = supabase.table(FOLLOWS_TABLE).select('*').eq(FOLLOWER_ID, Profile_Id).eq(FOLLOWED_ID, Profile_Id2).execute()
        return len(result.data) > 0
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/{Profile_Id}/isFollowed/{Profile_Id2}", response_model=bool)
async def isFollowed(Profile_Id: str, Profile_Id2: str):
    try:
        result = supabase.table(FOLLOWS_TABLE).select('*').eq(FOLLOWER_ID, Profile_Id2).eq(FOLLOWED_ID, Profile_Id).execute()
        return len(result.data) > 0
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

