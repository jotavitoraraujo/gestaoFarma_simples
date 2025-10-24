#################### --- IMPORTS --- #######################
from sqlite3 import Connection, Cursor
from pathlib import Path
from datetime import date
from decimal import Decimal
import sqlite3
import logging
import contextlib

#################### --- ADAPTERS AND CONVERSORS FOR DATE --- ####################
def date_to_str_adapter(value: date) -> str:
    'inject a object_date in the date translator to sql pattern'
    value_string = value.strftime('%Y-%m-%d')
    return value_string

def bytes_to_date_conversor(value: bytes) -> date:
    'inject a object_str in the date translator the of sql pattern to python object'
    value_decode = value.decode()
    value_date = date.fromisoformat(value_decode)
    return value_date

#################### --- ADAPTERS AND CONVERSORS FOR DECIMALS --- ####################
def decimal_to_str_adapter(value: Decimal) -> str:
    'adapt the value of the an object decimal to an string for inputed in database'
    value_string = str(value)
    return value_string

def bytes_to_decimal_conversor(value: bytes) -> Decimal:
    'receives from the database a value that was previously bytes and is now converted to decimal'
    value_decode = value.decode()
    value_decimal = Decimal(f'{value_decode}')
    return value_decimal

###################### --- PATH FOR DATABASE 'farmacia.db' --- #############################
root_folder = Path(__file__).parent.parent
db_file = root_folder/'data'/'farmacia.db'

###################### --- CONNECTION FUNCTION WITH DATABASE --- ###########################
@contextlib.contextmanager
def connect_db():
    'database connection control'
    
    connect_db = None
    try:
        ####### --- ANY OBJECT -> BYTES (STR) OBJECT --- #######
        sqlite3.register_adapter(date, date_to_str_adapter)
        sqlite3.register_adapter(Decimal, decimal_to_str_adapter)
        ####### --- BYTES (STR) OBJECT -> ANY OBJECT --- #######
        sqlite3.register_converter('date', bytes_to_date_conversor)
        sqlite3.register_converter('Decimal', bytes_to_decimal_conversor)
        ######################################################
        connect_db = sqlite3.connect(db_file, detect_types = sqlite3.PARSE_DECLTYPES)
        logging.info('\n')
        logging.info(f'*' * 50)
        logging.warning(f'[ALERTA] Conexão com banco de dados iniciada.')
        logging.info(f'*' * 50)
        yield connect_db
        ######################################################
    except Exception as instance_error:
        logging.error(f'[ERRO] Um erro inesperado foi detectado, para preservar a integridade do banco de dados as alterações não foram efetivadas. Detalhes: {type(instance_error)}')
        if connect_db:
            connect_db.rollback()
        raise instance_error
        ######################################################
    else:
        if connect_db:
            connect_db.commit()
        ######################################################
    finally:
        if connect_db:
            connect_db.close()
            logging.info('\n')
            logging.info(f'*' * 50)
            logging.warning(f'[ALERTA] Conexão com o banco de dados finalizada.')
            logging.info(f'*' * 50)
##############################################
def _create_product_schema(cursor: Cursor):
    'create schema to the model product in database'

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_fiscal_profile INTEGER NOT NULL,
            supplier_code TEXT,
            ean TEXT,            
            name_product TEXT,
            anvisa_code TEXT,
            sale_price DECIMAL,
            max_consumer_price DECIMAL,
            min_stock INTEGER,
            curva_abc TEXT,
            FOREIGN KEY(id_fiscal_profile) REFERENCES fiscal_profile(id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fiscal_profile (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ncm_code TEXT,
            cest_code TEXT,
            origin_code TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS batchs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_taxation_details INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            physical_id TEXT,
            quantity DECIMAL,
            unit_cost_amount DECIMAL,
            other_expenses_amount DECIMAL,
            use_by_date DATE,
            manufacturing_date DATE,
            receive_date DATE NOT NULL,
            UNIQUE (product_id, physical_id),
            FOREIGN KEY(product_id) REFERENCES products(id),
            FOREIGN KEY(id_taxation_details) REFERENCES purchase_tax_details(id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS purchase_tax_details (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cfop TEXT,
            icms_cst TEXT,
            icms_st_base_amount DECIMAL,
            icms_st_percentage DECIMAL,
            icms_st_retained_amount DECIMAL,
            pis_cst TEXT,
            cofins_cst TEXT
        )
    ''')

def _create_auth_schema(cursor: Cursor):
    'create schema to authenticate in database'

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT NOT NULL,
            pin_hash TEXT NOT NULL,
            salt BLOB NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS roles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role_name TEXT NOT NULL,
            UNIQUE(role_name)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS permissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            permission_name TEXT NOT NULL,
            UNIQUE(permission_name)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS role_permissions (
            role_id INTEGER NOT NULL,
            permission_id INTEGER NOT NULL,
            PRIMARY KEY (role_id, permission_id),
            FOREIGN(role_id) REFERENCES roles(id),
            FOREIGN(permission_id) REFERENCES permissions(id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_roles (
            user_id INTEGER NOT NULL,
            role_id INTEGER NOT NULL,
            PRIMARY KEY (user_id, role_id),
            FOREIGN(user_id) REFERENCES users(id),
            FOREIGN(role_id) REFERENCES roles(id)
        )
    ''')

def _create_sales_schema(cursor: Cursor):
    'create the sales schema'

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            order_date DATE NOT NULL,
            total_value REAL NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            batch_id INTEGER NOT NULL,
            quantity_sold INTEGER NOT NULL,
            sale_price_register REAL,
            FOREIGN KEY(order_id) REFERENCES orders(id),
            FOREIGN KEY(batch_id) REFERENCES batchs(id)
        )
    ''')

def _create_events_schema(cursor: Cursor):
    'create the schema for events'

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATE NOT NULL,
            event_type TEXT NOT NULL,
            user_id INTEGER,
            product_id INTEGER,
            batch_id INTEGER,
            details TEXT NOT NULL           
        )
    ''')

def _create_idx_users_schema(cursor: Cursor):
    'create the indexes for schema users'

    ### --- INDEX'S TABLE USERS --- ###
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_id ON users(user_name)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_user_name ON users(user_name)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_pin_hash ON users(pin_hash)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_salt ON users(salt)')

def _create_idx_events_schema(cursor: Cursor):
    'create the indexes for schema events'

    ### --- INDEX'S TABLE EVENTS --- ### 
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_events_user_id ON events(user_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_events_product_id ON events(product_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_events_batch_id ON events(batch_id)')

def starter_schema(connect_db: Connection):
    'start a creating the of tables for structure in the database' 
    
    cursor = connect_db.cursor()
    
    ### -- SCHEMAS -- ## 
    _create_product_schema(cursor)
    _create_auth_schema(cursor)
    _create_sales_schema(cursor)
    _create_events_schema(cursor)

    ### -- INDEXES -- ##
    _create_idx_users_schema(cursor)
    _create_idx_events_schema(cursor)

# def search_product(connect_db: Connection, product: Product):
#     'search for a product using an object -> Product'
    
#     connector = connect_db.cursor()

#     connector.execute('''
                     
#             SELECT id, nome_produto, preco_venda, data_validade 
#             FROM produtos 
#             JOIN lotes 
#             ON produtos.id = lotes.produto_id 
#             WHERE produtos.id = ? 
#             ORDER BY data_validade ASC 
#             LIMIT 1 
        
#         ''', 
#         (
#             product.id,
            
#         ))
    
#     db_answer = connector.fetchone()
#     return db_answer

# def search_product_name(connect_db: Connection, search: str) -> list:
#     'search an product using the integer name or a part of the name of respective Product '
#     connector = connect_db.cursor()

#     connector.execute('''
        
#         SELECT id, nome_produto, ean, preco_venda, id_lote, id_lote_fisico, produto_id, quantidade, preco_custo, data_validade, data_entrada
#         FROM produtos
#         JOIN lotes
#         ON produtos.id = lotes.produto_id
#         WHERE produtos.nome_produto LIKE ?
#         ORDER BY data_validade ASC        
    
#     ''',
#     (
#         f'%{search}%',
#     ))

#     db_answer = connector.fetchall()    
#     return db_answer

######################################################################################################################
