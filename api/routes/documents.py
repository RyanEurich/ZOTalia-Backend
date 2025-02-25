from datetime import datetime
import re
import logging
from typing import Optional
from uuid import UUID
from fastapi import APIRouter, File, HTTPException, UploadFile
from ..config import supabase
from ..models.documentSchema import CreateDocumentSchema, UpdateDocumentSchema, ReturnDocumentSchema

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
router = APIRouter(prefix="/documents", tags=["documents"])
GIG_TABLE:str = 'document'
GIG_ID:str = 'document_id'

#duplicated in avatar, move to separate file later
def sanitize_filename(filename: str) -> str:
    # Replace spaces with underscores and remove special characters
    filename = re.sub(r'\s+', '_', filename)
    filename = re.sub(r'[^a-zA-Z0-9_.-]', '', filename)
    return filename

@router.post("/upload-document")
async def upload_document(file: UploadFile = File(...)):
    try:
        # Upload the file to the Supabase bucket
        file_content = await file.read()
        file_name = f"{sanitize_filename(file.filename)}"
        result =  supabase.storage.from_("documents").upload(file_name, file_content)
        print(result)
        # if result.error:
        #     raise HTTPException(status_code=500, detail=result.error.message)
        
        # Get the public URL of the uploaded file
        document_url = supabase.storage.from_("documents").get_public_url(file_name)
        print(document_url)
        return {"document_url": document_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/download-document")
async def download_document(file_name: str):
    try:
        # Get the public URL of the uploaded file
        document_url = supabase.storage.from_("documents").get_public_url(file_name)
        return {"document_url": document_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=list[ReturnDocumentSchema])
async def get_documents()-> list[ReturnDocumentSchema]:
    try:
        result = supabase.table(GIG_TABLE).select('*').execute()
        print(type(result))
        return result.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/{document_id}", response_model=ReturnDocumentSchema)
async def get_document(document_id: str) -> ReturnDocumentSchema:
    try:
        result = supabase.table(GIG_TABLE).select('*').eq(GIG_ID, document_id).execute()
        return result.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/", response_model=ReturnDocumentSchema)
async def create_document(document: CreateDocumentSchema) -> ReturnDocumentSchema:
    try:
        logger.info(document.model_dump())
        result =  supabase.table(GIG_TABLE).insert(document.model_dump(exclude_unset=True)).execute()
        logger.info(result)
        return result.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/{document_id}", response_model=ReturnDocumentSchema)
async def update_document(document_id: str, document: UpdateDocumentSchema) -> ReturnDocumentSchema:
    try:
        print(document.model_dump(exclude_unset=True,serialize_as_any=True))
        result = supabase.table(GIG_TABLE).update(document.model_dump(exclude_unset=True)).eq(GIG_ID, document_id).execute()
        return result.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.delete("/{document_id}")
async def delete_document(document_id: str):
    try:
        result = supabase.table(GIG_TABLE).delete().eq(GIG_ID, document_id).execute()
        return {"message": "Document deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
