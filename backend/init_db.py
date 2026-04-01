"""
Database initialization script
Initializes database with required departments and default data
Run this script once before starting the application
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine, Base
from app.models import Department, Faculty, Student
from app.auth import hash_password
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def initialize_database():
    """Initialize database with required data"""
    
    # Create tables
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("✓ Tables created successfully")
    
    # Get database session
    db = SessionLocal()
    
    try:
        # Initialize departments
        logger.info("Initializing departments...")
        departments_data = [
            {
                "code": "CSE",
                "name": "Computer Science & Engineering",
                "email": "cse@karunya.edu"
            },
            {
                "code": "IT",
                "name": "Information Technology",
                "email": "it@karunya.edu"
            },
            {
                "code": "ELECTRICAL",
                "name": "Electrical Engineering",
                "email": "electrical@karunya.edu"
            },
            {
                "code": "PLUMBING",
                "name": "Plumbing & Facilities",
                "email": "plumbing@karunya.edu"
            },
            {
                "code": "ADMINISTRATION",
                "name": "Administration",
                "email": "administration@karunya.edu"
            }
        ]
        
        for dept_data in departments_data:
            # Check if department already exists
            existing = db.query(Department).filter(Department.code == dept_data["code"]).first()
            
            if not existing:
                dept = Department(
                    code=dept_data["code"],
                    name=dept_data["name"],
                    email=dept_data["email"]
                )
                db.add(dept)
                logger.info(f"  ✓ Created department: {dept_data['code']}")
            else:
                logger.info(f"  ✓ Department {dept_data['code']} already exists")
        
        db.commit()
        
        # Initialize faculty members
        logger.info("Initializing faculty members...")
        faculty_data = [
            {
                "email": "cse@karunya.edu",
                "password": "admin123",
                "full_name": "CSE Department",
                "dept_code": "CSE"
            },
            {
                "email": "it@karunya.edu",
                "password": "admin123",
                "full_name": "IT Department",
                "dept_code": "IT"
            },
            {
                "email": "electrical@karunya.edu",
                "password": "admin123",
                "full_name": "Electrical Department",
                "dept_code": "ELECTRICAL"
            },
            {
                "email": "plumbing@karunya.edu",
                "password": "admin123",
                "full_name": "Plumbing & Facilities",
                "dept_code": "PLUMBING"
            },
            {
                "email": "administration@karunya.edu",
                "password": "admin123",
                "full_name": "Administration",
                "dept_code": "ADMINISTRATION"
            }
        ]
        
        for fac_data in faculty_data:
            # Check if faculty already exists
            existing = db.query(Faculty).filter(Faculty.email == fac_data["email"]).first()
            
            if not existing:
                # Get department
                dept = db.query(Department).filter(Department.code == fac_data["dept_code"]).first()
                if dept:
                    faculty = Faculty(
                        email=fac_data["email"],
                        password_hash=hash_password(fac_data["password"]),
                        full_name=fac_data["full_name"],
                        department_id=dept.id
                    )
                    db.add(faculty)
                    logger.info(f"  ✓ Created faculty: {fac_data['email']}")
            else:
                logger.info(f"  ✓ Faculty {fac_data['email']} already exists")
        
        db.commit()
        
        # Initialize demo student
        logger.info("Initializing demo student...")
        student_data = {
            "email": "demo@karunya.edu.in",
            "password": "student123",
            "full_name": "Demo Student"
        }
        
        existing_student = db.query(Student).filter(Student.email == student_data["email"]).first()
        
        if not existing_student:
            student = Student(
                email=student_data["email"],
                password_hash=hash_password(student_data["password"]),
                full_name=student_data["full_name"]
            )
            db.add(student)
            db.commit()
            logger.info(f"  ✓ Created demo student: {student_data['email']}")
        else:
            logger.info(f"  ✓ Demo student {student_data['email']} already exists")
        
        logger.info("✓ Database initialized successfully!")
        logger.info("\nDefault credentials for testing:")
        logger.info("\n📚 STUDENT LOGIN:")
        logger.info(f"  Email: {student_data['email']}")
        logger.info(f"  Password: {student_data['password']}")
        logger.info("\n👨‍💼 FACULTY LOGIN:")
        for fac in faculty_data:
            logger.info(f"  Email: {fac['email']}")
            logger.info(f"  Password: {fac['password']}")
        
    except Exception as e:
        logger.error(f"✗ Error during initialization: {str(e)}")
        db.rollback()
        raise
    
    finally:
        db.close()

if __name__ == "__main__":
    initialize_database()
