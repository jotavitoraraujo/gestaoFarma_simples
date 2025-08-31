####### --- IMPORTS --- #######
from sqlite3 import Connection
from sistema.database import criar_tabelas

####### --- TEST FUNCTIONS WHERE EACH FUNCTION CHECK IF DERTEMINED TABLE WAS CREATE WITHIN DATABASE.PY --- #######
####### --- TEST FUNCTION ONE: TABLE -> PRODUCTS --- #######
def test_create_table_products(db_connection: Connection):
    
    expected_result = ('produtos',)
    criar_tabelas(db_connection)
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
    criar_tabelas(db_connection)
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
    criar_tabelas(db_connection)
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
    criar_tabelas(db_connection)
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
    criar_tabelas(db_connection)
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
    criar_tabelas(db_connection)
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
    criar_tabelas(db_connection)
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