"""
Shared complaint routes
General complaint endpoints accessible to both students and faculty
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging

from app.database import get_db
from app.models import Complaint, Department
from app.schemas import ComplaintResponse, DepartmentResponse
from app.auth import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/complaint", tags=["Complaints"])

# ============ DEPARTMENT ENDPOINTS ============

@router.get("/departments")
async def get_all_departments(db: Session = Depends(get_db)):
    """
    Get list of all departments
    Public endpoint - no authentication required
    """
    departments = db.query(Department).all()
    
    return {
        "departments": [
            DepartmentResponse.from_orm(d) for d in departments
        ]
    }

@router.get("/department/{dept_code}", response_model=DepartmentResponse)
async def get_department_by_code(
    dept_code: str,
    db: Session = Depends(get_db)
):
    """Get department by code (CSE, IT, ELECTRICAL, etc.)"""
    department = db.query(Department).filter(Department.code == dept_code).first()
    
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Department {dept_code} not found"
        )
    
    return DepartmentResponse.from_orm(department)

# ============ STATISTICS ENDPOINTS ============

@router.get("/statistics")
async def get_system_statistics(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get system-wide statistics
    Available to authenticated users
    """
    try:
        complaints = db.query(Complaint).all()
        
        stats = {
            "total_complaints": len(complaints),
            "submitted": len([c for c in complaints if c.status.value == "Submitted"]),
            "sent_to_dept": len([c for c in complaints if c.status.value == "Sent to Department"]),
            "read": len([c for c in complaints if c.status.value == "Read by Faculty"]),
            "resolved": len([c for c in complaints if c.status.value == "Resolved"]),
            "by_department": {}
        }
        
        # Statistics by department
        departments = db.query(Department).all()
        for dept in departments:
            dept_complaints = db.query(Complaint).filter(Complaint.department_id == dept.id).all()
            stats["by_department"][dept.code] = {
                "total": len(dept_complaints),
                "resolved": len([c for c in dept_complaints if c.status.value == "Resolved"])
            }
        
        return stats
    
    except Exception as e:
        logger.error(f"Failed to get statistics: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get statistics"
        )
