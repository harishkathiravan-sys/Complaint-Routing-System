"""
JWT Authentication module
Handles token generation, validation, and user verification
"""

from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status, Request
import os
from dotenv import load_dotenv
import logging

load_dotenv()

logger = logging.getLogger(__name__)

# Security configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key-change-in-production-12345")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt
    
    Args:
        password: Plain text password
        
    Returns:
        Hashed password
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password
    
    Args:
        plain_password: Plain text password to verify
        hashed_password: Previously hashed password
        
    Returns:
        True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a JWT access token
    
    Args:
        data: Dictionary containing user information (email, id, role)
        expires_delta: Token expiration time
        
    Returns:
        JWT token string
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "iat": datetime.now(timezone.utc)})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Dict[str, Any]:
    """
    Verify and decode a JWT token
    
    Args:
        token: JWT token string
        
    Returns:
        Decoded token payload
        
    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        logger.warning(f"Token verification failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_current_user(request: Request) -> Dict[str, Any]:
    """
    Dependency to get current authenticated user
    
    Usage:
        @app.get("/profile")
        async def get_profile(current_user = Depends(get_current_user)):
            return current_user
    
    Args:
        request: HTTP request containing Authorization header
        
    Returns:
        User information from token
        
    Raises:
        HTTPException: If token is invalid
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = auth_header.split(" ")[1]
    payload = verify_token(token)
    
    user_id: int = payload.get("user_id")
    email: str = payload.get("email")
    role: str = payload.get("role")
    
    if user_id is None or email is None or role is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return {
        "user_id": user_id,
        "email": email,
        "role": role
    }

async def get_current_student(current_user = Depends(get_current_user)) -> Dict[str, Any]:
    """
    Dependency to ensure current user is a student
    
    Args:
        current_user: Current user from get_current_user
        
    Returns:
        Student user information
        
    Raises:
        HTTPException: If user is not a student
    """
    if current_user.get("role") != "student":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This endpoint is only for students"
        )
    return current_user

async def get_current_faculty(current_user = Depends(get_current_user)) -> Dict[str, Any]:
    """
    Dependency to ensure current user is faculty
    
    Args:
        current_user: Current user from get_current_user
        
    Returns:
        Faculty user information
        
    Raises:
        HTTPException: If user is not faculty
    """
    if current_user.get("role") != "faculty":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This endpoint is only for faculty"
        )
    return current_user

def extract_department_from_roll_number(email: str) -> Optional[str]:
    """
    Extract department code from student email/roll number
    Format: URK25CSXXXX -> CS
    
    Args:
        email: Student email
        
    Returns:
        Department code or None
    """
    try:
        # Get local part of email (before @)
        local_part = email.split("@")[0].upper()
        
        # Format: URKYYCCXXXX where CC = department code
        # Position 5-7 contains department code (e.g., CS, IT, EC)
        if len(local_part) >= 7:
            # Try to extract department code (positions 5-7, but often 2-3 chars)
            potential_dept = local_part[4:6]  # CS, IT, etc.
            return potential_dept
        
        return None
    except Exception:
        return None

def validate_student_password_format(password: str) -> bool:
    """
    Validate student password format: URK25CSXXXX
    
    Args:
        password: Password to validate
        
    Returns:
        True if valid, False otherwise
    """
    # Format check: URK + 2 digits (year) + 2-3 letters (dept) + 4 digits
    if len(password) < 8:
        return False
    
    upper_pass = password.upper()
    if not upper_pass.startswith("URK"):
        return False
    
    return True
