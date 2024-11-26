from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import DATA_PATH

DATABASE_URL = f"sqlite:///./{DATA_PATH}/chat_history.db"

# Create database engine
engine = create_engine(DATABASE_URL, echo=True)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
Base = declarative_base()

def get_db():
    """
    Dependency for database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def init_db():
    Base.metadata.create_all(bind=engine)