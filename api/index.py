from typing import Optional


# main.py
from fastapi import FastAPI, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from supabase import create_client, Client
from dotenv import load_dotenv
from . import models as m

# from .auth import auth_middleware
# from .routes import employee_routes, auth_routes
load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_ANON_KEY')
SUPABASE_JWT_SECRET = os.getenv('SUPABASE_JWT_SECRET')

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


### Create FastAPI instance with custom docs and openapi url
app = FastAPI(docs_url="/api/py/docs", openapi_url="/api/py/openapi.json")

# @app.get("/api/py/helloFastApi")
# def hello_fast_api():
#     return {"message": "Hello from FastAPI"}





@app.get("/api/py/helloFastApi")
async def hello_fast_api():
    profiles = supabase.table('profiles').select('*').execute()
    return profiles
    # return {"message": "Hello World"}

@app.get("/api/py/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

#profiles CRUD
@app.get("/api/py/profiles/")
async def get_profiles()-> m.ProfileSchema:
    profiles = supabase.table('profiles').select('*').execute()
    return profiles 

@app.get("/api/py/helloFastApi/profiles/{profile_id}")
async def get_profile(profile_id: str)-> m.ProfileSchema:
    profile = await supabase.table('profiles').select('*').eq('id', profile_id).execute()
    return profile

@app.post("/api/py/helloFastApi/profiles/")
def create_profile(profile: m.ProfileSchema):
    upload_response = supabase.table('profiles').upsert(profile.model_dump_json()).execute()
    return upload_response

#need to test this
@app.put("/api/py/helloFastApi/profiles/{profile_id}")
def update_profile(profile_id: str, profile: m.ProfileSchema):
    profile = supabase.table('profiles').update(profile).eq('id', profile_id).execute()
    return profile

@app.delete("/api/py/helloFastApi/profiles/{profile_id}")
def delete_profile(profile_id: str):
    profile = supabase.table('profiles').delete().eq('id', profile_id).execute()
    return profile