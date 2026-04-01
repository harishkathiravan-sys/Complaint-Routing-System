"""
Faculty routes and endpoints
Handles faculty login, complaint management, and response
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_
from datetime import datetime
import logging
from typing import List

from app.database import get_db
from app.models import Faculty, Complaint, ComplaintReply, Department, StatusEnum
from app.schemas import (
    FacultyLoginRequest, TokenResponse, FacultyDashboardResponse,
    FacultyProfileResponse, ComplaintListResponse, ComplaintResponse,
    ComplaintReplyRequest, DepartmentResponse
)
from app.auth import hash_password, verify_password, create_access_token, get_current_user

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/faculty", tags=["Faculty"])

# ============ AUTHENTICATION ENDPOINTS ============

@router.post("/login", response_model=TokenResponse)
async def faculty_login(
    credentials: FacultyLoginRequest,
    db: Session = Depends(get_db)
):
    """
    Faculty login endpoint
    
    Validates:
    - Email format: department@karunya.edu (e.g., cse@karunya.edu)
    - Password: admin123 (configurable, currently hardcoded)
    
    Returns JWT token for authenticated requests
    """
    # Validate email format
    if not credentials.email.endswith("@karunya.edu"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Faculty email must end with @karunya.edu"
        )
    
    # Find faculty in database
    faculty = db.query(Faculty).filter(Faculty.email == credentials.email).first()
    
    if not faculty or not verify_password(credentials.password, faculty.password_hash):
        logger.warning(f"Failed login attempt for faculty: {credentials.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Create access token
    access_token = create_access_token(
        data={
            "user_id": faculty.id,
            "email": faculty.email,
            "role": "faculty",
            "department_id": faculty.department_id
        }
    )
    
    logger.info(f"Faculty logged in: {faculty.email}")
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user_id=faculty.id,
        email=faculty.email,
        role="faculty"
    )

# ============ PROFILE ENDPOINTS ============

@router.get("/profile", response_model=FacultyProfileResponse)
async def get_faculty_profile(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current faculty member's profile"""
    if current_user.get("role") != "faculty":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This endpoint is only for faculty"
        )
    
    faculty = db.query(Faculty).filter(Faculty.id == current_user["user_id"]).first()
    
    if not faculty:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Faculty not found")
    
    return FacultyProfileResponse.from_orm(faculty)

# ============ DASHBOARD ENDPOINTS ============

@router.get("/dashboard", response_model=FacultyDashboardResponse)
async def get_faculty_dashboard(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get faculty dashboard with statistics
    
    Shows:
    - Total complaints for their department
    - Pending (unread) complaints
    - Resolved complaints
    - List of complaints
    
    Faculty can only see complaints routed to their department
    """
    if current_user.get("role") != "faculty":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This endpoint is only for faculty"
        )
    
    faculty = db.query(Faculty).filter(Faculty.id == current_user["user_id"]).first()
    
    if not faculty:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Faculty not found")
    
    # Get all complaints for this department
    all_complaints = (
        db.query(Complaint)
        .filter(Complaint.department_id == faculty.department_id)
        .all()
    )
    
    total = len(all_complaints)
    unread = len([c for c in all_complaints if c.status == StatusEnum.SUBMITTED])
    pending = len([c for c in all_complaints if c.status != StatusEnum.RESOLVED])
    resolved = len([c for c in all_complaints if c.status == StatusEnum.RESOLVED])
    
    # Get complaints list
    complaints_list = (
        db.query(Complaint)
        .filter(Complaint.department_id == faculty.department_id)
        .order_by(desc(Complaint.created_at))
        .limit(50)
        .all()
    )
    
    complaints_response = [
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
        for c in complaints_list
    ]
    
    return FacultyDashboardResponse(
        profile=FacultyProfileResponse.from_orm(faculty),
        total_complaints=total,
        pending_complaints=pending,
        resolved_complaints=resolved,
        unread_complaints=unread,
        complaints=complaints_response
    )

# ============ COMPLAINT MANAGEMENT ENDPOINTS ============

@router.get("/complaints", response_model=List[ComplaintResponse])
async def get_faculty_complaints(
    status: StatusEnum = Query(None),
    limit: int = Query(50, ge=1, le=100),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all complaints for faculty's department
    
    Optional filters:
    - status: Filter by complaint status
    - limit: Maximum number of results
    """
    if current_user.get("role") != "faculty":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This endpoint is only for faculty"
        )
    
    faculty = db.query(Faculty).filter(Faculty.id == current_user["user_id"]).first()
    if not faculty:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Faculty not found")
    
    query = db.query(Complaint).filter(Complaint.department_id == faculty.department_id)
    
    if status:
        query = query.filter(Complaint.status == status)
    
    complaints = query.order_by(desc(Complaint.created_at)).limit(limit).all()
    
    return [ComplaintResponse.from_orm(c) for c in complaints]

@router.get("/complaint/{complaint_id}", response_model=ComplaintResponse)
async def get_faculty_complaint(
    complaint_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get detailed information about a specific complaint (department-scoped)"""
    if current_user.get("role") != "faculty":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This endpoint is only for faculty"
        )
    
    faculty = db.query(Faculty).filter(Faculty.id == current_user["user_id"]).first()
    if not faculty:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Faculty not found")
    
    complaint = db.query(Complaint).filter(
        and_(
            Complaint.complaint_id == complaint_id,
            Complaint.department_id == faculty.department_id
        )
    ).first()
    
    if not complaint:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Complaint not found")
    
    return ComplaintResponse.from_orm(complaint)

# ============ COMPLAINT ACTION ENDPOINTS ============

@router.put("/complaint/{complaint_id}/read", response_model=ComplaintResponse)
async def mark_complaint_as_read(
    complaint_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Mark a complaint as read by faculty
    Updates status from SUBMITTED to READ_BY_FACULTY
    Records timestamp
    """
    if current_user.get("role") != "faculty":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This endpoint is only for faculty"
        )
    
    faculty = db.query(Faculty).filter(Faculty.id == current_user["user_id"]).first()
    if not faculty:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Faculty not found")
    
    complaint = db.query(Complaint).filter(
        and_(
            Complaint.complaint_id == complaint_id,
            Complaint.department_id == faculty.department_id
        )
    ).first()
    
    if not complaint:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Complaint not found")
    
    # Update status only if not already read
    if complaint.status in [StatusEnum.SUBMITTED, StatusEnum.SENT_TO_DEPARTMENT]:
        complaint.status = StatusEnum.READ_BY_FACULTY
        complaint.read_by_faculty_at = datetime.utcnow()
        complaint.updated_at = datetime.utcnow()
        
        try:
            db.commit()
            db.refresh(complaint)
            logger.info(f"Complaint {complaint_id} marked as read by {faculty.email}")
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to update complaint: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update complaint"
            )
    
    return ComplaintResponse.from_orm(complaint)

@router.put("/complaint/{complaint_id}/reply", response_model=ComplaintResponse)
async def add_reply_to_complaint(
    complaint_id: str,
    reply_data: ComplaintReplyRequest,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Faculty replies to a complaint
    - Adds a reply record
    - Updates complaint status to READ_BY_FACULTY
    """
    if current_user.get("role") != "faculty":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This endpoint is only for faculty"
        )
    
    faculty = db.query(Faculty).filter(Faculty.id == current_user["user_id"]).first()
    if not faculty:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Faculty not found")
    
    complaint = db.query(Complaint).filter(
        and_(
            Complaint.complaint_id == complaint_id,
            Complaint.department_id == faculty.department_id
        )
    ).first()
    
    if not complaint:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Complaint not found")
    
    try:
        # Create reply
        new_reply = ComplaintReply(
            complaint_id=complaint.id,
            faculty_id=faculty.id,
            reply_text=reply_data.reply_text
        )
        
        # Update complaint status if needed
        if complaint.status == StatusEnum.SUBMITTED:
            complaint.status = StatusEnum.READ_BY_FACULTY
            complaint.read_by_faculty_at = datetime.utcnow()
        
        complaint.updated_at = datetime.utcnow()
        
        db.add(new_reply)
        db.commit()
        db.refresh(complaint)
        
        logger.info(f"Faculty {faculty.email} replied to complaint {complaint_id}")
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to add reply: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to add reply"
        )
    
    return ComplaintResponse.from_orm(complaint)

@router.put("/complaint/{complaint_id}/resolve", response_model=ComplaintResponse)
async def resolve_complaint(
    complaint_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Mark complaint as resolved
    Updates status to RESOLVED and records resolution timestamp
    """
    if current_user.get("role") != "faculty":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This endpoint is only for faculty"
        )
    
    faculty = db.query(Faculty).filter(Faculty.id == current_user["user_id"]).first()
    if not faculty:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Faculty not found")
    
    complaint = db.query(Complaint).filter(
        and_(
            Complaint.complaint_id == complaint_id,
            Complaint.department_id == faculty.department_id
        )
    ).first()
    
    if not complaint:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Complaint not found")
    
    if complaint.status != StatusEnum.RESOLVED:
        complaint.status = StatusEnum.RESOLVED
        complaint.resolved_at = datetime.utcnow()
        complaint.updated_at = datetime.utcnow()
        
        try:
            db.commit()
            db.refresh(complaint)
            logger.info(f"Complaint {complaint_id} marked as resolved by {faculty.email}")
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to resolve complaint: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to resolve complaint"
            )
    
    return ComplaintResponse.from_orm(complaint)
