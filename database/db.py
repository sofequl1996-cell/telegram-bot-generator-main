from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from config import Config
from database.models import Base

# Create engine
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=False)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initialize database"""
    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized successfully!")

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def close_db():
    """Close database connection"""
    engine.dispose()
