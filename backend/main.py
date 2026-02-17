from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from fastapi.responses import JSONResponse
from src.api.auth import auth_router
from src.api.tasks import tasks_router
from src.config.settings import settings
from src.database.database import init_db
import os

# Initialize FastAPI app with security scheme components
security = HTTPBearer()

app = FastAPI(
    title="Todo Application API",
    description="API for the Todo Application Full-Stack Web Application",
    version="1.0.0",
    swagger_ui_parameters={"docExpansion": "tags"},
    security=[{"HTTPBearer": []}],
    components={
        "securitySchemes": {
            "HTTPBearer": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
                "description": "Enter your JWT token to access protected endpoints"
            }
        }
    }
)

# Initialize database tables on startup
@app.on_event("startup")
def startup_event():
    try:
        init_db()
        print("Database tables initialized successfully")
    except Exception as e:
        print(f"Error initializing database: {e}")

# Dynamic CORS for production (allows all *.hf.space subdomains)
def get_allowed_origins():
    origins = settings.BACKEND_CORS_ORIGINS.copy()
    # In production, be more permissive with CORS for Hugging Face
    if os.getenv("ENVIRONMENT") == "production":
        origins.append("*")
    return origins

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/api", tags=["auth"])
app.include_router(tasks_router, prefix="/api", tags=["tasks"])

@app.get("/")
def read_root():
    return {"message": "Todo Application API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "todo-api"}