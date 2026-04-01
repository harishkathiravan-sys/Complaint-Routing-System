"""
SQLAlchemy models for database tables
Defines Student, Faculty, Department, Complaint, and Status entities
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base

# Enum for complaint status
class StatusEnum(str, enum.Enum):
    SUBMITTED = "Submitted"
    SENT_TO_DEPARTMENT = "Sent to Department"
    READ_BY_FACULTY = "Read by Faculty"
    RESOLVED = "Resolved"

# Enum for user roles
class RoleEnum(str, enum.Enum):
    STUDENT = "student"
    FACULTY = "faculty"

# Department Model
class Department(Base):
    __tablename__ = "departments"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, index=True, nullable=False)  # CSE, IT, etc.
    name = Column(String(200), nullable=False)  # Full name
    email = Column(String(100), unique=True)  # department@karunya.edu
    
    # Relationships
    complaints = relationship("Complaint", back_populates="department")
    faculty = relationship("Faculty", back_populates="department")
    
    def __repr__(self):
        return f"<Department(code={self.code}, name={self.name})>"

# Student Model
class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)  # Hashed password
    full_name = Column(String(200))
    department_code = Column(String(50))  # From roll number like URK25CS1234
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    complaints = relationship("Complaint", back_populates="student")
    
    def __repr__(self):
        return f"<Student(email={self.email}, department={self.department_code})>"

# Faculty Model
class Faculty(Base):
    __tablename__ = "faculty"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True, nullable=False)  # dept@karunya.edu
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(200))
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    department = relationship("Department", back_populates="faculty")
    replies = relationship("ComplaintReply", back_populates="faculty")
    
    def __repr__(self):
        return f"<Faculty(email={self.email}, department_id={self.department_id})>"

# Complaint Model
class Complaint(Base):
    __tablename__ = "complaints"
    
    id = Column(Integer, primary_key=True, index=True)
    complaint_id = Column(String(20), unique=True, index=True)  # Unique complaint number
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    student_email = Column(String(100), nullable=False)  # Store email for quick access
    complaint_text = Column(Text, nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    status = Column(SQLEnum(StatusEnum), default=StatusEnum.SUBMITTED, index=True)
    priority = Column(String(20), default="medium")  # low, medium, high
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    submitted_to_dept_at = Column(DateTime)
    read_by_faculty_at = Column(DateTime)
    resolved_at = Column(DateTime)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    student = relationship("Student", back_populates="complaints")
    department = relationship("Department", back_populates="complaints")
    replies = relationship("ComplaintReply", back_populates="complaint", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Complaint(id={self.complaint_id}, status={self.status}, department_id={self.department_id})>"

# Complaint Reply Model
class ComplaintReply(Base):
    __tablename__ = "complaint_replies"
    
    id = Column(Integer, primary_key=True, index=True)
    complaint_id = Column(Integer, ForeignKey("complaints.id"), nullable=False)
    faculty_id = Column(Integer, ForeignKey("faculty.id"), nullable=False)
    reply_text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    complaint = relationship("Complaint", back_populates="replies")
    faculty = relationship("Faculty", back_populates="replies")
    
    def __repr__(self):
        return f"<ComplaintReply(complaint_id={self.complaint_id}, faculty_id={self.faculty_id})>"

# Status tracking model (for maintaining status history)
class StatusHistory(Base):
    __tablename__ = "status_history"
    
    id = Column(Integer, primary_key=True, index=True)
    complaint_id = Column(Integer, ForeignKey("complaints.id"), nullable=False)
    old_status = Column(SQLEnum(StatusEnum))
    new_status = Column(SQLEnum(StatusEnum), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<StatusHistory(complaint_id={self.complaint_id}, {self.old_status} -> {self.new_status})>"

# For backward compatibility
Status = StatusEnum
