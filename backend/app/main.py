"""
Smart Complaint Routing System - Main Backend Application
Production-ready FastAPI application with JWT authentication
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError
import logging
import os
from dotenv import load_dotenv

load_dotenv()

from app.database import engine, Base, get_db
from app.models import Status, Department
from app.routers import student_routes, faculty_routes, complaint_routes
from app.auth import create_access_token

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Smart Complaint Routing System",
    description="NLP-based complaint routing system for Karunya Institute",
    version="1.0.0"
)

# Configure CORS - development and production
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(student_routes.router, tags=["Students"])
app.include_router(faculty_routes.router, tags=["Faculty"])
app.include_router(complaint_routes.router, tags=["Complaints"])

# Health check endpoint
@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring
    """
    try:
        return {
            "status": "healthy",
            "message": "Smart Complaint Routing System is running"
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Service unavailable")

# Initial data setup endpoint (for development)
@app.post("/init-db")
async def initialize_database(db = Depends(get_db)):
    """
    Initialize database with departments and initial status values
    WARNING: Only for development/setup
    """
    try:
        # Check if departments already exist
        existing_dept = db.query(Department).first()
        
        if not existing_dept:
            # Create departments
            departments_data = [
                {"code": "CSE", "name": "Computer Science & Engineering"},
                {"code": "IT", "name": "Information Technology"},
                {"code": "ELECTRICAL", "name": "Electrical Engineering"},
                {"code": "PLUMBING", "name": "Plumbing & Facilities"},
                {"code": "ADMINISTRATION", "name": "Administration"}
            ]
            
            for dept_data in departments_data:
                dept = Department(code=dept_data["code"], name=dept_data["name"])
                db.add(dept)
            
            db.commit()
            logger.info("Departments initialized successfully")
        
        return {"message": "Database initialized successfully"}
    
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database initialization failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Database initialization failed")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Smart Complaint Routing System",
        "docs": "/docs",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
