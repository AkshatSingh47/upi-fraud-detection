from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models import Base
from app.db.user_models import User  # Import User model to register it
import os
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Database URL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./fraud_detection.db")

# Create engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
    echo=False
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """
    Initialize database tables
    """
    try:
        # Import all models here to ensure they're registered
        from app.db.user_models import User
        
        Base.metadata.create_all(bind=engine)
        logger.info("Database initialized successfully (transaction_logs + users tables)")
    except Exception as e:
        logger.error(f"Database initialization error: {e}")

def get_db_session():
    """
    Get database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize database on import
init_db()

