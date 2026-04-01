"""
Pydantic schemas for request/response validation
Ensures data integrity and type safety across API endpoints
"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime
from app.models import StatusEnum

# ============ AUTHENTICATION SCHEMAS ============

class StudentLoginRequest(BaseModel):
    email: EmailStr
    password: str
    
    @validator('email')
    def validate_student_email(cls, v):
        if not v.endswith("@karunya.edu.in"):
            raise ValueError('Student email must end with @karunya.edu.in')
        return v

class FacultyLoginRequest(BaseModel):
    email: EmailStr
    password: str
    
    @validator('email')
    def validate_faculty_email(cls, v):
        if not v.endswith("@karunya.edu"):
            raise ValueError('Faculty email must end with @karunya.edu')
        return v

class StudentRegisterRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    
    @validator('email')
    def validate_student_email(cls, v):
        if not v.endswith("@karunya.edu.in"):
            raise ValueError('Student email must end with @karunya.edu.in')
        return v
    
    @validator('password')
    def validate_password_format(cls, v):
        """Validate password format: URK25CSXXXX"""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    email: str
    role: str

# ============ DEPARTMENT SCHEMAS ============

class DepartmentResponse(BaseModel):
    id: int
    code: str
    name: str
    email: Optional[str] = None
    
    class Config:
        from_attributes = True

# ============ COMPLAINT SCHEMAS ============

class ComplaintSubmitRequest(BaseModel):
    complaint_text: str = Field(..., min_length=10, max_length=2000)
    
    @validator('complaint_text')
    def validate_complaint_text(cls, v):
        if not v or len(v.strip()) < 10:
            raise ValueError('Complaint must be at least 10 characters')
        return v.strip()

class ComplaintReplyRequest(BaseModel):
    reply_text: str = Field(..., min_length=5, max_length=2000)
    
    @validator('reply_text')
    def validate_reply_text(cls, v):
        if not v or len(v.strip()) < 5:
            raise ValueError('Reply must be at least 5 characters')
        return v.strip()

class ComplaintReplyResponse(BaseModel):
    id: int
    complaint_id: int
    faculty_id: int
    reply_text: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ComplaintResponse(BaseModel):
    id: int
    complaint_id: str
    student_email: str
    complaint_text: str
    status: StatusEnum
    priority: str
    department: DepartmentResponse
    created_at: datetime
    submitted_to_dept_at: Optional[datetime] = None
    read_by_faculty_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    replies: List[ComplaintReplyResponse] = []
    
    class Config:
        from_attributes = True

class ComplaintListResponse(BaseModel):
    id: int
    complaint_id: str
    complaint_text: str
    status: StatusEnum
    priority: str
    department: DepartmentResponse
    created_at: datetime
    reply_count: int = 0
    
    class Config:
        from_attributes = True

class ComplaintStatusResponse(BaseModel):
    complaint_id: str
    status: StatusEnum
    current_stage: int  # 1-4
    stages: List[str]
    last_update: datetime
    latest_reply: Optional[str] = None
    
    class Config:
        from_attributes = True

# ============ STUDENT SCHEMAS ============

class StudentProfileResponse(BaseModel):
    id: int
    email: str
    full_name: Optional[str] = None
    department_code: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class StudentDashboardResponse(BaseModel):
    profile: StudentProfileResponse
    total_complaints: int
    active_complaints: int
    resolved_complaints: int
    recent_complaints: List[ComplaintListResponse]
    
    class Config:
        from_attributes = True

# ============ FACULTY SCHEMAS ============

class FacultyProfileResponse(BaseModel):
    id: int
    email: str
    full_name: Optional[str] = None
    department_id: int
    department: DepartmentResponse
    created_at: datetime
    
    class Config:
        from_attributes = True

class FacultyDashboardResponse(BaseModel):
    profile: FacultyProfileResponse
    total_complaints: int
    pending_complaints: int
    resolved_complaints: int
    unread_complaints: int
    complaints: List[ComplaintListResponse]
    
    class Config:
        from_attributes = True

# ============ STATUS TRACKING SCHEMAS ============

class StatusStageResponse(BaseModel):
    stage: int
    name: str
    completed: bool
    timestamp: Optional[datetime] = None

class CompleteStatusTrackingResponse(BaseModel):
    complaint_id: str
    stages: List[StatusStageResponse]
    overall_progress: float  # 0-100
    
    class Config:
        from_attributes = True

# ============ ERROR SCHEMAS ============

class ErrorResponse(BaseModel):
    detail: str
    status_code: int
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        from_attributes = True

# ============ UTILITY SCHEMAS ============

class HealthCheckResponse(BaseModel):
    status: str
    message: str
    
    class Config:
        from_attributes = True
