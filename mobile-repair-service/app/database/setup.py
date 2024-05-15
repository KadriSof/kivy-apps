import os
import logging
import pymysql
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from app.models.base import Base
from app.models.client import Client
from app.models.device import Device
from app.models.repair_order import RepairOrder


logging.basicConfig(level=logging.INFO)


def test_database_connection(host, username, password, database):
    try:
        # Attempt to connect to the database
        connection = pymysql.connect(host=host, user=username, password=password, database=database)
        print("Database connection successful!")
        connection.close()  # Close the connection
    except Exception as e:
        print(f"Database connection error: {e}")


def get_database_url():
    db_username = os.getenv('MyDB_USERNAME')
    db_password = os.getenv('MyDB_PASSWORD')
    db_host = os.getenv('MyDB_HOST')
    db_name = os.getenv('MyDB_NAME')

    if not all([db_username, db_password, db_host, db_name]):
        raise ValueError('One or more database environment variables are missing.')

    test_database_connection(db_host, db_username, db_password, db_name)
    database_url = f'mysql+pymysql://{db_username}:{db_password}@{db_host}/{db_name}'
    return database_url


def init_database():
    try:
        database_url = get_database_url()
        engine = create_engine(database_url, echo=True)
        Base.metadata.bind = engine
        sessionmaker(bind=engine)
        Base.metadata.create_all(engine)
        logging.info('DATABASE: Database initialized.')

    except ValueError as ve:
        logging.error(f"DATABASE: Error initializing database: {ve}")

    except SQLAlchemyError as se:
        logging.error(f"DATABASE: SQLAlchemy error: {se}")

    except Exception as e:
        logging.exception(f"DATABASE: Unexpected error: {e}")


if __name__ == '__main__':
    init_database()
