from pydoc import Helper
from fastapi import APIRouter, HTTPException
import logging
from ..config import supabase
from ..models.postInteractionsSchema import CreatePostInteractionSchema, UpdatePostInteractionSchema, ResponsePostInteractionSchema
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
router = APIRouter(prefix="/postInteractions", tags=["postInteractions"])
POST_INTERACTIONS_TABLE:str = 'post_interactions'
POST_INTERACTIONS_ID:str = 'id'

@router.get("/", response_model=list[ResponsePostInteractionSchema])
async def get_postInteractions()-> list[ResponsePostInteractionSchema]:
    try:
        result = supabase.table(POST_INTERACTIONS_TABLE).select('*').execute()
        return result.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/{post_interaction_id}", response_model=ResponsePostInteractionSchema)
async def get_postInteraction(post_interaction_id: str) -> ResponsePostInteractionSchema:
    try:
        result = supabase.table(POST_INTERACTIONS_TABLE).select('*').eq(POST_INTERACTIONS_ID, post_interaction_id).execute()
        return result.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/", response_model=ResponsePostInteractionSchema)
async def create_postInteraction(postInteraction: CreatePostInteractionSchema) -> ResponsePostInteractionSchema:
    try:
        logger.info(postInteraction.model_dump())
        result =  supabase.table(POST_INTERACTIONS_TABLE).insert(postInteraction.model_dump(exclude_unset=True)).execute()
        logger.info(result)
        return result.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/{post_interaction_id}", response_model=ResponsePostInteractionSchema)
async def update_postInteraction(post_interaction_id: str, postInteraction:  UpdatePostInteractionSchema) -> ResponsePostInteractionSchema:
    try:
        result = supabase.table(POST_INTERACTIONS_TABLE).update(postInteraction.model_dump(exclude_unset=True)).eq(POST_INTERACTIONS_ID, post_interaction_id).execute()
        return result.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.delete("/{post_interaction_id}")
async def delete_postInteraction(post_interaction_id: str):
    try:
        result = supabase.table(POST_INTERACTIONS_TABLE).delete().eq(POST_INTERACTIONS_ID, post_interaction_id).execute()
        return {"message": "Post Interaction deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))