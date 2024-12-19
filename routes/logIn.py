from fastapi import FastAPI, APIRouter, HTTPException, status
from fastapi_utils.inferring_router import InferringRouter
from pydantic import BaseModel
from models.account import user_log_in , UserCreate
from services.commonService import createUser , get_access_token ,get_refresh_token ,get_user_info ,user_token

router = InferringRouter()

@router.post("/logIn")
async def logIn(res:user_log_in):
    try:
        statusCode = await user_token(res)
        return statusCode
        
    except HTTPException as e:
        raise e

@router.post("/signUp")
async def signUp(res:UserCreate):
    statusCode =await createUser(res)
    return statusCode

@router.post("/token")
async def get_token():
    try:
        token = await get_access_token() 
        return {"access_token": token}
    
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.post("/refresh_token")
async def refresh_token(ref_token : str | None):
    try:
        new_tokne = await get_refresh_token(ref_token)
        return {"access_token":new_tokne}

    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/get_user_name")
async def get_user_details():
    try:
        status = await get_user_info("shubhamtest4")
        return status    
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code,detail=e.detail)
