from datetime import datetime
import re
import logging
from typing import Optional
from uuid import UUID
from fastapi import APIRouter, File, HTTPException, UploadFile
from ..config import supabase
from ..models.financial_schema import CreateFinancialSchema, UpdateFinancialSchema, ReturnFinancialSchema  

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
    
