#################### --- IMPORTS --- #######################
from sqlite3 import Connection
from pathlib import Path
from datetime import date
from decimal import Decimal
from system.models.product import Product 
# from system.models.user import User
# from system.models.batch import Batch
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

###################### --- ALL FUNCTIONALITYS (UNTIL NOW) OF THE MODULE 'DATABASE' --- ########################
def create_tables(connect_db: Connection):
    'start a creating the of tables for structure in the database' 
    
    cursor = connect_db.cursor()
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
    
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_events_user_id ON events(user_id);')
    cursor.execute('CREATE INDEX idx_events_product_id ON events(product_id);')
    cursor.execute('CREATE INDEX idx_events_batch_id ON events(batch_id);')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_name TEXT NOT NULL,
        user_pin TEXT NOT NULL
        
        )
    ''')
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

# def register_user_database(connect_db: Connection, user: User):
#     'register an new user on database'
    
#     connector = connect_db.cursor()

#     connector.execute('''
#             INSERT INTO usuarios (nome_usuario, pin_usuario)
#             VALUES (?, ?)
#             ''',
#             (
#                 user.user_name,
#                 user.user_pin               
            
#             ))

#     connect_db.commit()
#     print('=' * 30)
#     logging.info(f'[INFO] O usuário, {user.user_name} foi cadastrado.')
#     print('=' * 30)

# def search_user(connect_db: Connection, user: str) -> tuple:
#     'search an user by name, but the function returns all contained data in database'

#     connector = connect_db.cursor()

#     connector.execute('''
#             SELECT id_usuario, nome_usuario, pin_usuario
#             FROM usuarios
#             WHERE usuarios.nome_usuario = ?
#             LIMIT 1
            
#         ''',
#         (
#             user,
            
#         ))
    
#     db_answer = connector.fetchone()    
#     return db_answer
  
# def register_batch_alert(connect_db: Connection, order_id, product: Product, user: User, batch_sold: Batch, batch_correct: Batch):
#     'register of alert of the batch sold incorretly'

#     today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

#     if batch_sold != batch_correct:
#         neglect = 1
#     else:
#         neglect = 0

    # connector = connect_db.cursor()
    # connector.execute('''
    #     INSERT INTO alertas_lote (id_pedido, id_produto, id_usuario, id_lote_vendido, id_lote_correto, data, negligencia)
    #     VALUES (?, ?, ?, ?, ?, ?, ?)
    #     ''',
    #     (
    #         order_id,
    #         product.id,
    #         user.user_id,
    #         batch_sold.id,
    #         batch_correct.id,
    #         today,
    #         neglect
    #     ))
    # connect_db.commit()

    # print('=' * 30)
    # logging.info(f'[INFO] Os dados dessa venda foram registrados.')
    # print('=' * 30)

######################################################################################################################
