########### --- IMPORTS --- ##########
import sqlite3
import pytest
import logging

########## --- FIXTURES UTILITS --- ###########
@pytest.fixture
def db_connection():

    db_connection = None
    try:
        db_connection = sqlite3.connect(':memory:')
        logging.warning(f'[ALERT] Test connection with database is on.')
        yield db_connection
    
    except Exception as instance_error:
        logging.error(f'[ERROR] An exception was raised. Details: {instance_error}')
        if db_connection:
            db_connection.rollback()
        raise instance_error

    else:
        if db_connection:
            db_connection.commit()
    
    finally:
        if db_connection:
            db_connection.close()
            logging.warning(f'[ALERT] Test connection with database is off.')
