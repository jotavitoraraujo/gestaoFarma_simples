####### --- IMPORTS --- #######
import pytest
from sqlite3 import Connection
from sistema import database
from sistema.modelos.product import Product
from sistema.modelos.batch import Batch

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

####### --- THIS FUNCTION IS RESPONSABLE FOR THE SEARCH OF AN PRODUCT WITHIN DATABASE --- #######
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