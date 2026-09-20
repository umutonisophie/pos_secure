import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()
database_url = os.getenv("DATABASE_URL")
engine = create_engine(database_url, echo=False, future=True)
sessionMaker = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = sessionMaker()
    try:
        yield db
    finally:
        db.close()