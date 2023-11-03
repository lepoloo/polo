from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from configs.settings import DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME

DATABASE_URL = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@localhost/{DATABASE_NAME}"
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
        

# class Session:
#     def __enter__(self):
#         self.session = SessionLocal()
#         return self.session

#     def __exit__(self, exc_type, exc_val, exc_tb):
#         self.session.close()

# Base.metadata.create_all(bind=engine)