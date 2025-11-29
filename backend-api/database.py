import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base

# Database configuration
DATABASE_URL = os.environ.get(
    'DATABASE_URL',
    'postgresql://taskuser:taskpass@postgres:5432/taskmanager'
)

# Create engine
engine = create_engine(DATABASE_URL, echo=True)

# Create scoped session
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

# Base class for models
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    """Initialize the database, creating all tables."""
    # Import all models here to ensure they are registered with Base
    from models import Task
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")


def shutdown_session(exception=None):
    """Close the database session."""
    db_session.remove()
