####### --- IMPORTS --- #######
import pytest
from unittest.mock import patch
from sqlite3 import Connection
from sistema import database
from sistema.modelos.product import Product
from sistema.modelos.batch import Batch
from sistema.modelos.user import User
from tests.conftest import Alert


####### --- TEST FUNCTIONS WHERE EACH FUNCTION CHECK IF DERTEMINED TABLE WAS CREATE WITHIN DATABASE.PY --- #######
####### --- TEST FUNCTION ONE: TABLE -> PRODUCTS --- #######
def test_create_table_products(db_connection: Connection):
    
    expected_result = ('produtos',)
    database.create_tables(db_connection)
    cursor = db_connection.cursor()   
    cursor.execute('''
        SELECT name
        FROM sqlite_schema
        WHERE type = 'table' AND name = 'produtos';
    ''')
    real_result = cursor.fetchone()
    assert real_result == expected_result

####### --- TEST FUNCTION TWO: TABLE -> BATCHS --- #######
def test_create_table_batchs(db_connection: Connection):

    expected_result = ('lotes',)
    database.create_tables(db_connection)
    cursor = db_connection.cursor()
    cursor.execute('''
        SELECT name
        FROM sqlite_schema
        WHERE type = 'table' AND name = 'lotes';
    ''')
    real_result = cursor.fetchone()
    assert real_result == expected_result

####### --- TEST FUNCTION THREE: TABLE -> USERS --- #######
def test_create_table_users(db_connection: Connection):

    expected_result = ('usuarios',)
    database.create_tables(db_connection)
    cursor = db_connection.cursor()
    cursor.execute('''
        SELECT name
        FROM sqlite_schema
        WHERE type = 'table' AND name = 'usuarios'
    ''')
    real_result = cursor.fetchone()
    assert real_result == expected_result

####### --- TEST FUNCTION FOUR: TABLE -> ORDERS --- #######
def test_create_table_orders(db_connection: Connection):

    expected_result = ('pedidos',)
    database.create_tables(db_connection)
    cursor = db_connection.cursor()
    cursor.execute('''
        SELECT name
        FROM sqlite_schema
        WHERE type = 'table' AND name = 'pedidos'
    ''')
    real_result = cursor.fetchone()
    assert real_result == expected_result

####### --- TEST FUNCTION FIVE: TABLE -> ITEMS_ORDERS --- #######
def test_create_table_items_orders(db_connection: Connection):

    expected_result = ('itens_pedido',)
    database.create_tables(db_connection)
    cursor = db_connection.cursor()
    cursor.execute('''
        SELECT name
        FROM sqlite_schema
        WHERE type = 'table' AND name = 'itens_pedido'
    ''')
    real_result = cursor.fetchone()
    assert real_result == expected_result

####### --- TEST FUNCTION SIX: TABLE -> BATCH_ALERTS --- #######
def test_create_table_batch_alerts(db_connection: Connection):

    expected_result = ('alertas_lote',)
    database.create_tables(db_connection)
    cursor = db_connection.cursor()
    cursor.execute('''
        SELECT name
        FROM sqlite_schema
        WHERE type = 'table' AND name = 'alertas_lote'
    ''')
    real_result = cursor.fetchone()
    assert real_result == expected_result

####################################################################################################
####### --- THIS TEST FUNCTION HAS THE SAME FUNCTION AS THE PREVIOUS ONES, HOWEVER USING A FOR LOOP TO DO THE WORK --- #######
def test_create_all_tables(db_connection: Connection):
    
    expected_result_list = [
        'produtos',
        'lotes',
        'usuarios',
        'pedidos',
        'itens_pedido',
        'alertas_lote',
    ]
    database.create_tables(db_connection)
    cursor = db_connection.cursor()
    cursor.execute('''
        SELECT name
        FROM sqlite_schema
        WHERE type = 'table' AND name NOT LIKE 'sqlite_%'
    ''')
    real_result = cursor.fetchall()
    real_result_list = []
    
    for item in real_result:
        real_result_list.append(item[0])
    
    assert real_result_list == expected_result_list

####################################################################################################
####### --- THIS SESSION HAS OBJECTIVE TEST THE RECORD THE OF DATA IN TABLES THE OF DATABASE --- #######
# @pytest.mark.filterwarnings("ignore:The default date adapter is deprecated")
def test_save_products(db_connection: Connection, expected_list_products: list[Product]):

    database.create_tables(db_connection)
    database.save_products(db_connection, expected_list_products)
    cursor = db_connection.cursor()
    cursor.execute('''
        SELECT *
        FROM produtos
        JOIN lotes
        ON produtos.id = lotes.produto_id        
    ''')
    result = cursor.fetchall()
    result_list = []
    for item in result:
        product_instance = Product (
            id = item[0],
            ean = item[2],
            name = item[1],
            sale_price = item[3]           
        )
        ### --- INSTANCE EXPIRATION DATE --- ###
        object_expiration_date = item[11]
        print(type(object_expiration_date))
        ########################################
        batch_instance = Batch (
            batch_id = item[6],
            physical_batch_id = item[7],
            product_id = item[8],
            quantity = item[9],
            cost_price = item[10],
            expiration_date = object_expiration_date,
            entry_date = item[12]
        )
        product_instance.batch.append(batch_instance)
        result_list.append(product_instance)
    
    assert result_list == expected_list_products

####### --- THIS TEST FUNCTION VERIFY IF AN PRODUCT AS DETERMINED ID ALREADY EXISTS WITHIN DATABASE --- #######
def test_products_existing(db_connection: Connection, expected_list_products: list[Product], dipirona_product: Product):
    database.create_tables(db_connection)
    database.save_products(db_connection, expected_list_products)
    result = database.products_existing(db_connection, dipirona_product)

    assert result == True

####### --- THIS TEST FUNCTION IS RESPONSABLE FOR THE SEARCH OF AN PRODUCT WITHIN DATABASE --- #######
def test_search_product(db_connection: Connection, expected_list_products: list[Product], dipirona_product: Product):
    database.create_tables(db_connection)
    database.save_products(db_connection, expected_list_products)
    result = database.search_product(db_connection, dipirona_product)

    if isinstance(result, type(tuple)):
        assert (
            result[0] == dipirona_product.id
        and result[1] == dipirona_product.name
        and result[2] == dipirona_product.sale_price
        and result[3] == dipirona_product.batch[0].expiration_date
        )

####### --- THIS TEST FUNCTION IS RESPONSABLE FOR THE SEARCH AN PRODUCT BY THE NAME OR PART OF THE NAME --- #######
####### --- SCENARIO ONE: WRONG SEARCHES
@pytest.mark.parametrize('search_input, expected_result', 
    [
        ('X', [],),
        ('XX', [],),
        ('XXX', [],),
        ('/', [],),
        ('Ç', [],),
        ('1', [],),
        ('-1', [],),
        ('1.0', [],),
        ('', [],),
        (' ', [],),
])
def test_search_product_name(db_connection: Connection, expected_list_products: list[Product], search_input: str, expected_result):
    database.create_tables(db_connection)
    database.save_products(db_connection, expected_list_products)
    result = database.search_product_name(db_connection, search_input)

    if isinstance(result, type(list)):
        assert result == expected_result

####### --- SCENARIO TWO: CORRECT SEARCHES --- #######
def test_search_products_name_2(db_connection: Connection, expected_list_products: list[Product], vitamina_product: Product):
    database.create_tables(db_connection)
    database.save_products(db_connection, expected_list_products)

    search_input = 'VIT'
    result = database.search_product_name(db_connection, search_input)

    if isinstance(result, list):
        assert result[0][1] == vitamina_product.name

####### --- THIS TEST FUCTION IS RESPONSABLE OF REGISTER AN USER ON DATABASE --- #######
def test_register_user(db_connection: Connection, user_test: User):
    database.create_tables(db_connection)
    database.register_user(db_connection, user_test)
    cursor = db_connection.cursor()
    cursor.execute('''
        SELECT *
        FROM usuarios
    ''')
    result = cursor.fetchone()
    user_result = User (
        user_id = result[0],
        user_name = result[1],
        user_pin = result[2]
    )
    assert user_result == user_test
    
####### --- THIS TEST FUNCTION IS RESPONSABLE BY THE LOOKING-FOR AN USER WITHIN DATABASE --- #######
####### --- SCENARIO ONE: WRONG SEARCHS --- #######
@pytest.mark.parametrize('user_name_str, expected_result', 
    [
        ('Joao', None,),
        ('JoaoV', None,),
        ('/', None,),
        ('JoaoVito', None,)
])
def test_search_user(db_connection: Connection, user_test: User, user_name_str: str, expected_result):
    database.create_tables(db_connection)
    database.register_user(db_connection, user_test)
    result = database.search_user(db_connection, user_name_str)

    if isinstance(result, type(tuple)):
        assert result == expected_result

####### --- SCENARIO TWO: CORRECT SEARCHS --- #######
def test_search_user_2(db_connection: Connection, user_test: User):
    database.create_tables(db_connection)
    database.register_user(db_connection, user_test)
    
    user_name_str = 'JoaoVitor'
    result = database.search_user(db_connection, user_name_str)

    if isinstance(result, type(tuple)):

        user_result = User (
            user_id = result[0],
            user_name = result[1],
            user_pin = result[2]
        )

        assert user_result == user_test

####### --- THIS TEST FUNCTION IS RESPONSABLE FOR RECORDING A SALES DEVIATION FROM THE CORRECT BATCH --- #######
def test_register_batch_alert(
    db_connection: Connection, 
    expected_list_products_2: list[Product], 
    dipirona_product: Product, 
    dipirona_product_2: Product, 
    user_test: User, 
    alert: Alert
    ):
    
    database.create_tables(db_connection)
    database.save_products(db_connection, expected_list_products_2)
    database.register_user(db_connection, user_test)
    
    order_id = 1
    batch_correct = dipirona_product.batch[0].batch_id
    batch_sold = dipirona_product_2.batch[0].batch_id
    
    database.register_batch_alert(db_connection, order_id, dipirona_product_2, user_test, batch_sold, batch_correct)
    cursor = db_connection.cursor()
    cursor.execute('''
        SELECT *
        FROM alertas_lote
    ''')
    result = cursor.fetchone()

    if isinstance(result, type(tuple)):
        real_alert = Alert (
            alert_id = result[0],
            order_id = result[1],
            product = result[3],
            user = result[4],
            batch_sold = result[5],
            batch_correct = result[6],
            today = result[7],
            neglect = result[8]
        )
    assert real_alert == alert

