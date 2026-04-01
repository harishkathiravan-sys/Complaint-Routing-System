"""
Student routes and endpoints
Handles student login, dashboard, complaint submission, and tracking
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_
from datetime import timedelta
import logging
from typing import List

from app.database import get_db
from app.models import Student, Complaint, StatusEnum, Department, ComplaintReply
from app.schemas import (
    StudentLoginRequest, TokenResponse, StudentRegisterRequest,
    StudentDashboardResponse, StudentProfileResponse, ComplaintListResponse,
    ComplaintResponse, ComplaintStatusResponse, ComplaintSubmitRequest,
    DepartmentResponse
)
from app.auth import (
    hash_password, verify_password, create_access_token,
    get_current_student, get_current_user
)
from app.nlp import classify_complaint
import uuid

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/student", tags=["Student"])

# ============ AUTHENTICATION ENDPOINTS ============

@router.post("/login", response_model=TokenResponse)
async def student_login(
    credentials: StudentLoginRequest,
    db: Session = Depends(get_db)
):
    """
    Student login endpoint
    
    Validates:
    - Email ends with @karunya.edu.in
    - Password correct
    
    Returns JWT token for authenticated requests
    """
    # Validate email format
    if not credentials.email.endswith("@karunya.edu.in"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student email must end with @karunya.edu.in"
        )
    
    # Find student in database
    student = db.query(Student).filter(Student.email == credentials.email).first()
    
    if not student or not verify_password(credentials.password, student.password_hash):
        logger.warning(f"Failed login attempt for student: {credentials.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Create access token
    access_token = create_access_token(
        data={
            "user_id": student.id,
            "email": student.email,
            "role": "student"
        }
    )
    
    logger.info(f"Student logged in: {student.email}")
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user_id=student.id,
        email=student.email,
        role="student"
    )

@router.post("/register", response_model=TokenResponse)
async def student_register(
    data: StudentRegisterRequest,
    db: Session = Depends(get_db)
):
    """
    Student registration endpoint
    
    Creates new student account with validated email format
    """
    # Validate email format
    if not data.email.endswith("@karunya.edu.in"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student email must end with @karunya.edu.in"
        )
    
    # Check if student already exists
    existing = db.query(Student).filter(Student.email == data.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Student with this email already exists"
        )
    
    # Hash password
    hashed_password = hash_password(data.password)
    
    # Extract department code from email
    # Format: URK25CSXXXX -> CS
    email_local = data.email.split("@")[0]
    dept_code = None
    if len(email_local) >= 6:
        dept_code = email_local[4:6].upper()
    
    # Create new student
    new_student = Student(
        email=data.email,
        password_hash=hashed_password,
        full_name=data.full_name,
        department_code=dept_code
    )
    
    try:
        db.add(new_student)
        db.commit()
        db.refresh(new_student)
        logger.info(f"New student registered: {new_student.email}")
    except Exception as e:
        db.rollback()
        logger.error(f"Student registration failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )
    
    # Create token
    access_token = create_access_token(
        data={
            "user_id": new_student.id,
            "email": new_student.email,
            "role": "student"
        }
    )
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user_id=new_student.id,
        email=new_student.email,
        role="student"
    )

# ============ PROFILE ENDPOINTS ============

@router.get("/profile", response_model=StudentProfileResponse)
async def get_student_profile(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current student's profile"""
    student = db.query(Student).filter(Student.id == current_user["user_id"]).first()
    
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    
    return StudentProfileResponse.from_orm(student)

# ============ DASHBOARD ENDPOINTS ============

@router.get("/dashboard", response_model=StudentDashboardResponse)
async def get_student_dashboard(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get student dashboard with statistics and recent complaints
    Returns profile info, complaint counts, and recent complaints
    """
    student = db.query(Student).filter(Student.id == current_user["user_id"]).first()
    
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    
    # Get complaint statistics
    all_complaints = db.query(Complaint).filter(Complaint.student_id == student.id).all()
    total = len(all_complaints)
    active = len([c for c in all_complaints if c.status != StatusEnum.RESOLVED])
    resolved = len([c for c in all_complaints if c.status == StatusEnum.RESOLVED])
    
    # Get recent complaints (last 5)
    recent = (
        db.query(Complaint)
        .filter(Complaint.student_id == student.id)
        .order_by(desc(Complaint.created_at))
        .limit(5)
        .all()
    )
    
    recent_list = [
        ComplaintListResponse(
            id=c.id,
            complaint_id=c.complaint_id,
            complaint_text=c.complaint_text[:100] + "..." if len(c.complaint_text) > 100 else c.complaint_text,
            status=c.status,
            priority=c.priority,
            department=DepartmentResponse.from_orm(c.department),
            created_at=c.created_at,
            reply_count=len(c.replies)
        )
        for c in recent
    ]
    
    return StudentDashboardResponse(
        profile=StudentProfileResponse.from_orm(student),
        total_complaints=total,
        active_complaints=active,
        resolved_complaints=resolved,
        recent_complaints=recent_list
    )

# ============ COMPLAINT ENDPOINTS ============

@router.post("/complaint/submit", response_model=ComplaintResponse)
async def submit_complaint(
    complaint_data: ComplaintSubmitRequest,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Submit a new complaint
    
    - Validates complaint text (10-2000 characters)
    - Uses NLP to classify to department
    - Creates complaint record
    - Sets initial status to SUBMITTED
    """
    student = db.query(Student).filter(Student.id == current_user["user_id"]).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    
    # Classify complaint using NLP
    dept_code, confidence = classify_complaint(complaint_data.complaint_text)
    logger.info(f"Complaint classified to {dept_code} with confidence {confidence:.2%}")
    
    # Get department by code
    department = db.query(Department).filter(Department.code == dept_code).first()
    if not department:
        logger.error(f"Department {dept_code} not found")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Department not found")
    
    # Generate unique complaint ID
    complaint_id = f"CMP-{uuid.uuid4().hex[:8].upper()}"
    
    # Create complaint
    new_complaint = Complaint(
        complaint_id=complaint_id,
        student_id=student.id,
        student_email=student.email,
        complaint_text=complaint_data.complaint_text,
        department_id=department.id,
        status=StatusEnum.SUBMITTED,
        priority="medium"  # Can be enhanced with sentiment analysis
    )
    
    try:
        db.add(new_complaint)
        db.commit()
        db.refresh(new_complaint)
        logger.info(f"New complaint created: {complaint_id} for student {student.email}")
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to create complaint: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create complaint")
    
    return ComplaintResponse.from_orm(new_complaint)

@router.get("/complaints", response_model=List[ComplaintResponse])
async def get_student_complaints(
    status: StatusEnum = Query(None),
    limit: int = Query(50, ge=1, le=100),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all complaints for current student
    
    Optional filters:
    - status: Filter by complaint status
    - limit: Maximum number of results
    """
    query = db.query(Complaint).filter(Complaint.student_id == current_user["user_id"])
    
    if status:
        query = query.filter(Complaint.status == status)
    
    complaints = query.order_by(desc(Complaint.created_at)).limit(limit).all()
    
    return [ComplaintResponse.from_orm(c) for c in complaints]

@router.get("/complaint/{complaint_id}", response_model=ComplaintResponse)
async def get_complaint_details(
    complaint_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get detailed information about a specific complaint"""
    complaint = db.query(Complaint).filter(
        and_(
            Complaint.complaint_id == complaint_id,
            Complaint.student_id == current_user["user_id"]
        )
    ).first()
    
    if not complaint:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Complaint not found")
    
    return ComplaintResponse.from_orm(complaint)

@router.get("/complaint/{complaint_id}/status", response_model=ComplaintStatusResponse)
async def get_complaint_status(
    complaint_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get detailed status information for a complaint
    
    Returns:
    - Current status
    - Progress stages (1-4)
    - Latest faculty reply
    """
    complaint = db.query(Complaint).filter(
        and_(
            Complaint.complaint_id == complaint_id,
            Complaint.student_id == current_user["user_id"]
        )
    ).first()
    
    if not complaint:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Complaint not found")
    
    # Get latest reply
    latest_reply = None
    if complaint.replies:
        latest_reply = complaint.replies[-1].reply_text
    
    # Map status to stage
    status_to_stage = {
        StatusEnum.SUBMITTED: 1,
        StatusEnum.SENT_TO_DEPARTMENT: 2,
        StatusEnum.READ_BY_FACULTY: 3,
        StatusEnum.RESOLVED: 4
    }
    
    stages = [
        "Complaint Submitted",
        "Sent to Department",
        "Read by Faculty",
        "Resolved"
    ]
    
    return ComplaintStatusResponse(
        complaint_id=complaint.complaint_id,
        status=complaint.status,
        current_stage=status_to_stage.get(complaint.status, 1),
        stages=stages,
        last_update=complaint.updated_at,
        latest_reply=latest_reply
    )
