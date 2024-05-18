"""For managing database sessions during the application's runtime"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.utils.database_utils import get_database_url

DATABASE_URL = get_database_url()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session():
    return SessionLocal()
