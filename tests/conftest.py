########### --- IMPORTS --- ##########
import sqlite3
import pytest
import logging
from datetime import datetime, date
from sistema.modelos.product import Product
from sistema.modelos.batch import Batch

########## --- FIXTURES UTILITS --- ###########
@pytest.fixture
def db_connection():

    db_connection = None
    try:
        db_connection = sqlite3.connect(':memory:', detect_types = sqlite3.PARSE_DECLTYPES)
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

### DATE'S INSTANCES ###
@pytest.fixture
def object_today():
    today = datetime.now().strftime('%Y-%m-%d')
    return today

@pytest.fixture
def object_date():
    object_date_future = date(2035, 8, 31)
    return object_date_future

### PRODUCTs AND BATCHs INSTANCEs ###
@pytest.fixture
def vitamina_product(object_today, object_date):
    product_instance = Product (
        id = '67890',
        ean = '7895040302010',
        name = 'VITAMINA C EFERVESCENTE',
        sale_price = None
    )
    batch_instance = Batch (
        batch_id = None,
        physical_batch_id = 'ABC123DE',
        product_id = product_instance.id,
        quantity = float(15.0),
        cost_price = float(12.75),
        expiration_date = object_date,
        entry_date = object_today
    )
    product_instance.batch.append(batch_instance)
    vitamina_instance = product_instance
    return vitamina_instance

@pytest.fixture
def algodao_product(object_today, object_date):
    product_instance = Product (
        id = '101112',
        ean = '7895040302015',
        name = 'ALGODÃO HIDRÓFILO 50G',
        sale_price = None
    )
    batch_instance = Batch (
        batch_id = None,
        physical_batch_id = 'ABC123FG',
        product_id = product_instance.id,
        quantity = float(30.0),
        cost_price = float(3.20),
        expiration_date = object_date,
        entry_date = object_today
    )
    product_instance.batch.append(batch_instance)
    algodao_instance = product_instance
    return algodao_instance

@pytest.fixture
def dipirona_product(object_today, object_date):
    product_instance = Product (
        id = '12345',
        ean = '7891020304050',
        name = 'DIPIRONA 500MG COM 10 COMPRIMIDOS',
        sale_price = None        
    )
    batch_instance = Batch (
        batch_id = None,
        physical_batch_id = 'ABC123HI',
        product_id = product_instance.id,
        quantity = float(20.0),
        cost_price = float(8.50),
        expiration_date = object_date,
        entry_date = object_today
    )
    product_instance.batch.append(batch_instance)
    dipirona_instance = product_instance    
    return dipirona_instance

### LIST OF INSTANCE PRODUCTS ####
@pytest.fixture
def expected_list_products(dipirona_product: Product, vitamina_product: Product, algodao_product: Product) -> list[Product]:
    list = [
        dipirona_product, vitamina_product, algodao_product
    ]
    return list