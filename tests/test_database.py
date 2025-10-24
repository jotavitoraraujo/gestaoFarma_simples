####### --- IMPORTS --- #######
from sqlite3 import Connection
from system import database
####### --- TEST FUNCTIONS WHERE EACH FUNCTION CHECK IF DERTEMINED TABLE WAS CREATE WITHIN DATABASE.PY --- #######
####### --- TEST FUNCTION ZERO: TABLE -> PRODUCTS --- #######
def test_create_table_products(db_connection: Connection):
    
    expected_result = ('products',)
    database.starter_schema(db_connection)
    cursor = db_connection.cursor()   
    cursor.execute('''
        SELECT name
        FROM sqlite_schema
        WHERE type = 'table' AND name = 'products';
    ''')
    real_result = cursor.fetchone()
    assert real_result == expected_result

####### --- TEST FUNCTION ONE: TABLE -> FISCAL PROFILE --- #######
def test_create_table_fiscal_profile(db_connection: Connection):
    
    expected_result = ('fiscal_profile',)
    database.starter_schema(db_connection)
    cursor = db_connection.cursor()   
    cursor.execute('''
        SELECT name
        FROM sqlite_schema
        WHERE type = 'table' AND name = 'fiscal_profile';
    ''')
    real_result = cursor.fetchone()
    assert real_result == expected_result

####### --- TEST FUNCTION TWO: TABLE -> BATCHS --- #######
def test_create_table_batchs(db_connection: Connection):

    expected_result = ('batchs',)
    database.starter_schema(db_connection)
    cursor = db_connection.cursor()
    cursor.execute('''
        SELECT name
        FROM sqlite_schema
        WHERE type = 'table' AND name = 'batchs';
    ''')
    real_result = cursor.fetchone()
    assert real_result == expected_result

####### --- TEST FUNCTION THREE: TABLE -> OUTSTANDING PRODUCTS --- #######
def test_create_table_purchase_tax_details(db_connection: Connection):
    
    expected_result = ('purchase_tax_details',)
    database.starter_schema(db_connection)
    cursor = db_connection.cursor()   
    cursor.execute('''
        SELECT name
        FROM sqlite_schema
        WHERE type = 'table' AND name = 'purchase_tax_details';
    ''')
    real_result = cursor.fetchone()
    assert real_result == expected_result

####### --- TEST FUNCTION FOUR: TABLE -> EVENTS --- #######
def test_create_table_users(db_connection: Connection):

    expected_result = ('events',)
    database.starter_schema(db_connection)
    cursor = db_connection.cursor()
    cursor.execute('''
        SELECT name
        FROM sqlite_schema
        WHERE type = 'table' AND name = 'events'
    ''')
    real_result = cursor.fetchone()
    assert real_result == expected_result

####### --- TEST FUNCTION FIVE: TABLE -> USERS --- #######
def test_create_table_users(db_connection: Connection):

    expected_result = ('users',)
    database.starter_schema(db_connection)
    cursor = db_connection.cursor()
    cursor.execute('''
        SELECT name
        FROM sqlite_schema
        WHERE type = 'table' AND name = 'users'
    ''')
    real_result = cursor.fetchone()
    assert real_result == expected_result

####### --- TEST FUNCTION SIX: TABLE -> ORDERS --- #######
def test_create_table_orders(db_connection: Connection):

    expected_result = ('orders',)
    database.starter_schema(db_connection)
    cursor = db_connection.cursor()
    cursor.execute('''
        SELECT name
        FROM sqlite_schema
        WHERE type = 'table' AND name = 'orders'
    ''')
    real_result = cursor.fetchone()
    assert real_result == expected_result

####### --- TEST FUNCTION SEVEN: TABLE -> ITEMS_ORDERS --- #######
def test_create_table_items_orders(db_connection: Connection):

    expected_result = ('order_items',)
    database.starter_schema(db_connection)
    cursor = db_connection.cursor()
    cursor.execute('''
        SELECT name
        FROM sqlite_schema
        WHERE type = 'table' AND name = 'order_items'
    ''')
    real_result = cursor.fetchone()
    assert real_result == expected_result

####################################################################################################
####### --- THIS TEST FUNCTION HAS THE SAME FUNCTION AS THE PREVIOUS ONES, HOWEVER USING A FOR LOOP TO DO THE WORK --- #######
def test_create_all_tables(db_connection: Connection):
    
    expected_result_list = [
        'products',
        'fiscal_profile',
        'batchs',
        'purchase_tax_details',
        'events',
        'users',
        'orders',
        'order_items',
    ]
    database.starter_schema(db_connection)
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