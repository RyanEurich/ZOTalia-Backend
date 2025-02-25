from pydoc import Helper
from fastapi import APIRouter, HTTPException
import logging
from ..config import supabase
from ..models.postsSchema import CreatePostSchema, UpdatePostSchema, ResponsePostSchema
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
router = APIRouter(prefix="/posts", tags=["posts"])
APPPLICATION_TABLE:str = 'user_posts'
APPLICATION_ID:str = 'id'

@router.get("/", response_model=list[ResponsePostSchema])
async def get_posts()-> list[ResponsePostSchema]:
    try:
        result = supabase.table(APPPLICATION_TABLE).select('*').execute()
        return result.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/{post_id}", response_model=ResponsePostSchema)
async def get_post(post_id: str) -> ResponsePostSchema:
    try:
        result = supabase.table(APPPLICATION_TABLE).select('*').eq(APPLICATION_ID, post_id).execute()
        return result.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/", response_model=ResponsePostSchema)
async def create_post(post: CreatePostSchema) -> ResponsePostSchema:
    try:
        logger.info(post.model_dump())
        result =  supabase.table(APPPLICATION_TABLE).insert(post.model_dump(exclude_unset=True)).execute()
        logger.info(result)
        return result.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/{post_id}", response_model=ResponsePostSchema)
async def update_post(post_id: str, post:  UpdatePostSchema) -> ResponsePostSchema:
    try:
        result = supabase.table(APPPLICATION_TABLE).update(post.model_dump(exclude_unset=True)).eq(APPLICATION_ID, post_id).execute()
        return result.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{post_id}")
async def delete_post(post_id: str):
    try:
        result = supabase.table(APPPLICATION_TABLE).delete().eq(APPLICATION_ID, post_id).execute()
        return {"message": "Post deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  
