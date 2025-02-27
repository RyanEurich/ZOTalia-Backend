from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .config import supabase
from .routes import profiles, employers, gig_workers, gigs, applications, documents, financial, posts, postInteractions, follows
from .models.authSchemaas import UserCredentials
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# Import messaging module
from .routes.messaging import router as messaging_router, Message, get_topics, get_topic_messages, send_message, create_subscription, remove_subscription

# Define lifespan context manager for startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup event logic
    print("Application startup - Initializing messaging services")
    yield
    # Shutdown event logic
    print("Application shutdown - Cleaning up messaging resources")

# Initialize FastAPI app with lifespan
app = FastAPI(
    docs_url="/api/docs", 
    openapi_url="/api/openapi.json",
    lifespan=lifespan
)

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

@app.get("/api/user_id")
async def get_session(token: str = Depends(oauth2_scheme)):
    try:
        # Get the session using the token
        response = supabase.auth.get_user(token)
        return {
            "profile_id": response.user.id,
            # Add any other session data you need
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid authentication token")
    
# Include existing routers
app.include_router(profiles.router, prefix="/api", dependencies=[Depends(get_current_user)])
app.include_router(employers.router, prefix="/api", dependencies=[Depends(get_current_user)])
app.include_router(gig_workers.router, prefix="/api", dependencies=[Depends(get_current_user)])
app.include_router(gigs.router, prefix="/api", dependencies=[Depends(get_current_user)])
app.include_router(applications.router, prefix="/api", dependencies=[Depends(get_current_user)])
app.include_router(documents.router, prefix="/api", dependencies=[Depends(get_current_user)])
app.include_router(financial.router, prefix="/api", dependencies=[Depends(get_current_user)])
app.include_router(posts.router, prefix="/api", dependencies=[Depends(get_current_user)])
app.include_router(postInteractions.router, prefix="/api", dependencies=[Depends(get_current_user)])
app.include_router(follows.router, prefix="/api", dependencies=[Depends(get_current_user)])

# Include the messaging router - API requires authentication
app.include_router(messaging_router, prefix="/api", dependencies=[Depends(get_current_user)])

# For backward compatibility - messaging endpoints without the /messaging prefix
@app.get("/api/topics/")
async def legacy_get_topics(current_user=Depends(get_current_user)):
    return await get_topics()

@app.get("/api/topics/{topic}/messages/")
async def legacy_get_topic_messages(topic: str, current_user=Depends(get_current_user)):
    return await get_topic_messages(topic)

@app.post("/api/messages/")
async def legacy_send_message(message: Message, current_user=Depends(get_current_user)):
    return await send_message(message)

@app.post("/api/create_subscription/")
async def legacy_create_subscription(topic: str, user_id: str, current_user=Depends(get_current_user)):
    return await create_subscription(topic, user_id)

@app.delete("/api/remove_subscription/")
async def legacy_remove_subscription(topic: str, user_id: str, current_user=Depends(get_current_user)):
    return await remove_subscription(topic, user_id)

# Required for Vercel
module_app = app