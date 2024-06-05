import os
import logging
import pymysql


def check_database_connection():
    db_username = os.getenv('MyDB_USERNAME')
    db_password = os.getenv('MyDB_PASSWORD')
    db_host = os.getenv('MyDB_HOST')
    db_name = os.getenv('MyDB_NAME')

    try:
        connection = pymysql.connect(
            host=db_host,
            user=db_username,
            password=db_password,
            database=db_name
        )
        logging.info("Database: Database connection successful!")
        connection.close()

    except Exception as e:
        logging.error(f"Database connection error: {e}")


def get_database_url():
    db_username = os.getenv('MyDB_USERNAME')
    db_password = os.getenv('MyDB_PASSWORD')
    db_host = os.getenv('MyDB_HOST')
    db_name = os.getenv('MyDB_NAME')

    if not all([db_username, db_password, db_host, db_name]):
        raise ValueError('One or more database environment variables are missing.')

    check_database_connection()
    database_url = f'mysql+pymysql://{db_username}:{db_password}@{db_host}/{db_name}'
    print(database_url)
    return database_url
