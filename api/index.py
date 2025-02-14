from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import profiles, employers

app = FastAPI(docs_url="/api/docs", openapi_url="/api/openapi.json")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(profiles.router, prefix="/api")
app.include_router(employers.router, prefix="/api")
# app.include_router(users.router, prefix="/api")
# app.include_router(items.router, prefix="/api")

# Required for Vercel
module_app = app