########### --- IMPORTS --- ##########
import pytest
import logging
import sqlite3
from datetime import date, datetime
from system.models.product import Product
from system.models.batch import Batch
from system.models.user import User

#################### --- ADAPTERS AND CONVERSORS --- ####################
def date_adapter(object_date: date) -> str:
    'inject a object_date in the date translator to sql pattern'
    adapter_format_str = object_date.strftime('%Y-%m-%d')
    return adapter_format_str

def datetime_conversor(object_bytes: bytes) -> datetime:
    'inject a object_str in the datetime translator the of sql pattern to python object'
    convert_object_str = object_bytes.decode()
    adapter_format_date = datetime.strptime(convert_object_str, '%Y-%m-%d %HH:%MM:SS')
    return adapter_format_date

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
        batch_id = 2,
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
@pytest.fixture
def dipirona_product_2(object_today, object_date_2) -> Product:
    product_instance = Product (
        id = '12346',
        ean = '7891020304051',
        name = 'DIPIRONA 500MG COM 11 COMPRIMIDOS',
        sale_price = None        
    )
    batch_instance = Batch (
        batch_id = 1,
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

### THIS SESSION I AM TRYING CREATE AN CLASS CALLED 'ALERT' AS FIXTURE, FOR BE WITHIN TEST FUNCTION REGISTER_BATCH_ALERT
class Alert:
    def __init__(self,
        alert_id: int,
        order_id: int,  
        user: User, 
        product: Product,
        batch_id_sold: Batch,
        batch_id_correct: Batch, 
        today: str, 
        neglect: int
        ):
        
        self.alert_id = alert_id
        self.order_id = order_id
        self.user_id = user
        self.product_id = product
        self.batch_id_sold = batch_id_sold
        self.batch_id_correct = batch_id_correct
        self.today = today
        self.neglect = neglect

    def __repr__(self):
        'technical representation of type Alert'

        return f'''
        --- Data Alert ---
        1. Alert ID: {self.alert_id}
        2. Order ID: {self.order_id}
        3. User ID: {self.user_id}
        4. Product ID: {self.product_id}
        5. Batch ID Sold: {self.batch_id_sold}
        6. Batch ID Correct: {self.batch_id_correct}
        7. Date: {self.today}
        8. Neglect: {self.neglect}
    '''

    def __eq__(self, other):
        'dunder method for comparassion between types Alert'

        if isinstance(other, type(self)):
            return (
                other.order_id == self.order_id
                and other.product_id == self.product_id
                and other.user_id == self.user_id
                and other.batch_id_sold == self.batch_id_sold
                and other.batch_id_correct == self.batch_id_correct
            )
        else:
            return False
        
### INSTANCE ALERT ###
@pytest.fixture
def alert(dipirona_product: Product, dipirona_product_2: Product, user_test: User):
    
    object_datetime_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    alert_type = Alert (
        alert_id = 2,
        order_id = 1,
        user = user_test.user_id,
        product = int(dipirona_product_2.id),        
        batch_id_sold = dipirona_product_2.batch[0].batch_id,
        batch_id_correct = dipirona_product.batch[0].batch_id,
        today = object_datetime_str,
        neglect = 1
    )
    return alert_type