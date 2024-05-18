"""database initialization and schema setup."""
import logging
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from app.models.base import Base
from app.models.client import Client
from app.models.device import Device
from app.models.repair_order import RepairOrder

from app.utils.database_utils import check_database_connection, get_database_url

logging.basicConfig(level=logging.INFO)


def init_database():
    try:
        check_database_connection()
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
