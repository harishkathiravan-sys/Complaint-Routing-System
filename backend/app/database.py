"""
Database configuration and session management
SQLAlchemy ORM setup with PostgreSQL support
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database URL - use PostgreSQL for production, SQLite for development
DATABASE_TYPE = os.getenv("DATABASE_TYPE", "sqlite")

if DATABASE_TYPE == "postgresql":
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql://user:password@localhost:5432/complaint_routing_db"
    )
elif DATABASE_TYPE == "sqlite":
    # Use absolute path for SQLite
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    DB_FILE = os.path.join(BASE_DIR, "complaint_routing.db")
    DATABASE_URL = f"sqlite:///{DB_FILE}"
else:
    raise ValueError(f"Unsupported DATABASE_TYPE: {DATABASE_TYPE}")

print(f"Using database: {DATABASE_TYPE}")

# Create engine
if "sqlite" in DATABASE_URL:
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        echo=os.getenv("SQL_ECHO", "false").lower() == "true"
    )
else:
    engine = create_engine(
        DATABASE_URL,
        echo=os.getenv("SQL_ECHO", "false").lower() == "true",
        pool_pre_ping=True
    )

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative base for models
Base = declarative_base()

def get_db() -> Session:
    """
    Dependency to get database session
    Usage: session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Health check function
def check_database():
    """Check if database is accessible"""
    try:
        with SessionLocal() as session:
            session.execute("SELECT 1")
        return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False
