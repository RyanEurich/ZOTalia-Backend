from datetime import datetime, timedelta
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .config import supabase
from .routes import profiles, employers
from .models.authSchemaas import UserCredentials
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI(docs_url="/api/docs", openapi_url="/api/openapi.json")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")


def get_current_user(token: str = Depends(oauth2_scheme)):
    #implement this later
    try:
        user = supabase.auth.get_user(token)
        print(user)
        if user:
            return user
        else:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

@app.post("/api/signup")
async def sign_up(credentials: UserCredentials):
    try:
        user = supabase.auth.sign_up({"email": credentials.email, "password": credentials.password})
        return {"message": "User signed up successfully", "user": user}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        user = supabase.auth.sign_in_with_password({"email": form_data.username, "password": form_data.password})
        # print(user)
        access_token = user.session.access_token
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/signout")
async def sign_out(token: str = Depends(oauth2_scheme)):
    try:
        supabase.auth.sign_out()
        return {"message": "User signed out successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    #doesn't actually remove the token. need to implement refresh jwt
    

# Include routers
app.include_router(profiles.router, prefix="/api", dependencies=[Depends(get_current_user)])
app.include_router(employers.router, prefix="/api", dependencies=[Depends(get_current_user)])
# app.include_router(users.router, prefix="/api")
# app.include_router(items.router, prefix="/api")
# Required for Vercel
module_app = app