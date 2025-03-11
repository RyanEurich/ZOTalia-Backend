from datetime import datetime
import re
import logging
from typing import Any, Dict, Optional
from uuid import UUID
from fastapi import APIRouter, File, HTTPException, UploadFile
import httpx
from ..config import supabase
from ..models.financial_schema import CreateFinancialSchema, UpdateFinancialSchema, ReturnFinancialSchema  
from google import genai

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
router = APIRouter(prefix="/financials", tags=["financials"])
FINANCIAL_TABLE:str = 'financial_account'
FINANCIAL_ID:str = 'account_id'

@router.get("/", response_model=list[ReturnFinancialSchema])
async def get_financials()-> list[ReturnFinancialSchema]:
    try:
        result = supabase.table(FINANCIAL_TABLE).select('*').execute()
        return result.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/{financial_id}", response_model=ReturnFinancialSchema)
async def get_financial(financial_id: str) -> ReturnFinancialSchema:
    try:
        result = supabase.table(FINANCIAL_TABLE).select('*').eq(FINANCIAL_ID, financial_id).execute()
        return result.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/", response_model=ReturnFinancialSchema)
async def create_financial(financial: CreateFinancialSchema) -> ReturnFinancialSchema:
    try:
        logger.info(financial.model_dump())
        result =  supabase.table(FINANCIAL_TABLE).insert(financial.model_dump(exclude_unset=True)).execute()
        logger.info(result)
        return result.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/{financial_id}", response_model=ReturnFinancialSchema)
async def update_financial(financial_id: str, financial: UpdateFinancialSchema) -> ReturnFinancialSchema:
    try:
        result = supabase.table(FINANCIAL_TABLE).update(financial.model_dump(exclude_unset=True)).eq(FINANCIAL_ID, financial_id).execute()
        return result.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.delete("/{financial_id}")
async def delete_financial(financial_id: str):
    try:
        result = supabase.table(FINANCIAL_TABLE).delete().eq(FINANCIAL_ID, financial_id).execute()
        return {"message": "Financial deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/suggestions", response_model=Dict[str, Any])
async def get_finance_suggestions(financial: CreateFinancialSchema) -> Dict[str, Any]:
    try:
        # Initialize the Google Gemini API client
        client = genai.Client(api_key="AIzaSyBzbbs5b8TPZ_6QuBVDV5jvMK-a_FG1gx0")
        
        # Prepare the input for the Gemini API
        input_text = f"Provide financial suggestions based on the following data: {financial.model_dump(exclude_unset=True)}"
        
        # Call the Google Gemini API
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=input_text
        )
        # Extract the suggestions from the response
        suggestions = response.text
        
        return {"suggestions": suggestions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))