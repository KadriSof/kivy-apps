import logging
from functools import wraps

from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from pymysql.err import IntegrityError as PyMySQLError
from app.database.session import get_session


def managed_session(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        session = get_session()
        try:
            result = func(*args, session=session, **kwargs)
            session.commit()
            return result

        except Exception as e:
            session.rollback()
            logging.error(f"Exception during session management {e}", exc_info=True)
            raise

        finally:
            session.close()

    return wrapper
