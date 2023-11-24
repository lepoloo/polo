from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app import config

DATABASE_URL = f"postgresql://{config.database_username}:{config.database_password}@{config.database_hostname}:{config.database_port}/{config.database_name}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Dependencies
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
