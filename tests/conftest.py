########### --- IMPORTS --- ##########
import pytest
import logging
import sqlite3
from datetime import date
from sistema.modelos.product import Product
from sistema.modelos.batch import Batch
from sistema.modelos.user import User

#################### --- ADAPTERS AND CONVERSORS --- ####################
def date_adapter(object_date: date) -> str:
    'inject a object_date in the date translator to sql pattern'
    adapter_format_str = object_date.strftime('%Y-%m-%d')
    return adapter_format_str

def date_conversor(object_bytes: bytes) -> date:
    'inject a object_str in the date translator the of sql pattern to python object'
    convert_object_str = object_bytes.decode()
    adapter_format_date = date.fromisoformat(convert_object_str)
    return adapter_format_date

########## --- FIXTURES UTILITS --- ###########
@pytest.fixture
def db_connection():

    db_connection = None
    try:
        ####### --- DATE OBJECT -> BYTES (STR) OBJECT --- #######
        sqlite3.register_adapter(date, date_adapter)
        ####### --- BYTES (STR) OBJECT -> DATE OBJECT --- #######
        sqlite3.register_converter('date', date_conversor)
        
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
def object_today() -> date:
    today = date.today()
    return today

@pytest.fixture
def object_date() -> date:
    object_date_future = date(2035, 8, 31)
    return object_date_future

############################################################
# --- EXCLUSIVE VARIANT FOR THE TEST REGISTER BATCH ALERT --- 
@pytest.fixture
def object_date_2() -> date:
    object_date_future = date(2045, 8, 31)
    return object_date_future
############################################################

### PRODUCTs AND BATCHs INSTANCEs ###
@pytest.fixture
def dipirona_product(object_today, object_date) -> Product:
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

############################################################
# --- EXCLUSIVE VARIANT FOR THE TEST REGISTER BATCH ALERT ---
def dipirona_product_2(object_today, object_date_2) -> Product:
    product_instance = Product (
        id = '12345',
        ean = '7891020304050',
        name = 'DIPIRONA 500MG COM 10 COMPRIMIDOS',
        sale_price = None        
    )
    batch_instance = Batch (
        batch_id = None,
        physical_batch_id = 'ABC123HJ',
        product_id = product_instance.id,
        quantity = float(20.0),
        cost_price = float(8.50),
        expiration_date = object_date_2,
        entry_date = object_today
    )
    product_instance.batch.append(batch_instance)
    dipirona_instance = product_instance    
    return dipirona_instance
############################################################

@pytest.fixture
def vitamina_product(object_today, object_date) -> Product:
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
def algodao_product(object_today, object_date) -> Product:
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

### LIST OF INSTANCE PRODUCTS ####
@pytest.fixture
def expected_list_products(dipirona_product: Product, vitamina_product: Product, algodao_product: Product) -> list[Product]:
    list = [
        dipirona_product, vitamina_product, algodao_product
    ]
    return list

############################################################
# --- EXCLUSIVE VARIANT FOR THE TEST REGISTER BATCH ALERT ---
@pytest.fixture
def expected_list_products_2(dipirona_product: Product, dipirona_product_2: Product, vitamina_product: Product, algodao_product: Product) -> list[Product]:
    list = [
        dipirona_product, dipirona_product_2, vitamina_product, algodao_product
    ]
    return list
############################################################

### INSTANCE USER ###
@pytest.fixture
def user_test() -> User:
    user = User (
        user_id = 1,
        user_name = 'JoaoVitor',
        user_pin = '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4'
    )
    return user

### ORDER ID FIXTURE ###
@pytest.fixture
def order_id() -> str:
    order_id = '1'
    return order_id