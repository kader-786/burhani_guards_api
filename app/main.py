# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import Login_controller, ITS_API_controller, Duty_controller, Team_controller
from app.config import API_BASE_PATH
from app.db import initialize_connection_pool
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app with custom docs URL
app = FastAPI(
    title="Burhani Guards API",
    description="Burhani Guards Management System API",
    version="1.0.0",
    docs_url=f"{API_BASE_PATH}/docs",
    redoc_url=f"{API_BASE_PATH}/redoc",
    openapi_url=f"{API_BASE_PATH}/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database connection pool on startup
@app.on_event("startup")
async def startup_event():
    """Initialize resources on startup"""
    try:
        initialize_connection_pool(minconn=2, maxconn=10)
        logger.info("Database connection pool initialized")
    except Exception as e:
        logger.error(f"Failed to initialize database connection pool: {e}")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup resources on shutdown"""
    logger.info("Application shutting down")


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Burhani Guards API",
        "status": "running",
        "docs": f"{API_BASE_PATH}/docs"
    }


# Health check endpoint
@app.get(f"{API_BASE_PATH}/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "api": "Burhani Guards API",
        "version": "1.0.0"
    }


# Include routers with the base path
app.include_router(
    Login_controller.router,
    prefix=API_BASE_PATH
)

app.include_router(
    ITS_API_controller.router,
    prefix=API_BASE_PATH
)

app.include_router(
    Duty_controller.router,
    prefix=API_BASE_PATH
)


app.include_router(
    Team_controller.router,
    prefix=API_BASE_PATH
)

# You can add more routers here as you develop them
# app.include_router(
#     another_controller.router,
#     prefix=API_BASE_PATH
# )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
