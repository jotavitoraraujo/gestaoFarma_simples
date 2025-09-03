#################### --- IMPORTS --- #######################
from sqlite3 import Connection
from pathlib import Path
from sistema.modelos.product import Product 
from sistema.modelos.user import User
from sistema.modelos.batch import Batch
from datetime import datetime, date
import sqlite3
import logging
import contextlib

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

###################### --- PATH FOR DATABASE 'farmacia.db' --- #############################
pasta_sistema = Path(__file__).parent
db_file = pasta_sistema.parent/'dados'/'farmacia.db'

###################### --- CONNECTION FUNCTION WITH DATABASE --- ###########################
@contextlib.contextmanager
def connect_db():
    'database connection control'
    
    connect_db = None
    try:
        ####### --- DATE OBJECT -> BYTES (STR) OBJECT --- #######
        sqlite3.register_adapter(date, date_adapter)
        ####### --- BYTES (STR) OBJECT -> DATE OBJECT --- #######
        sqlite3.register_converter('date', date_conversor)

        connect_db = sqlite3.connect(db_file, detect_types = sqlite3.PARSE_DECLTYPES)
        logging.warning(f'[ALERTA] Conexão com banco de dados iniciada.')
        yield connect_db
    
    except Exception as instance_error:
        logging.error(f'[ERRO] Um erro inesperado foi detectado, para preservar a integridade do banco de dados as alterações não foram efetivadas. Detalhes: {type(instance_error)}')
        if connect_db:
            connect_db.rollback()
        raise instance_error
    
    else:
        if connect_db:
            connect_db.commit()
    
    finally:
        if connect_db:
            connect_db.close()
            logging.warning(f'[ALERTA] Conexão com o banco de dados finalizada.')

###################### --- ALL FUNCTIONALITYS (UNTIL NOW) OF THE MODULE 'DATABASE' --- ########################
def create_tables(connect_db: Connection):
    'start a creating the of tables for structure in the database' 
    
    cursor = connect_db.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id TEXT PRIMARY KEY,
            nome_produto TEXT NOT NULL,            
            ean TEXT NOT NULL,
            preco_venda REAL,            
            estoque_minimo INTEGER,            
            curva_abc TEXT
            
        )
    ''')    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lotes (
        id_lote INTEGER PRIMARY KEY AUTOINCREMENT,
        id_lote_fisico TEXT NOT NULL,
        produto_id TEXT NOT NULL,        
        quantidade INTEGER NOT NULL,        
        preco_custo REAL NOT NULL,  
        data_validade DATE NOT NULL,
        data_entrada DATE NOT NULL,                           
        FOREIGN KEY(produto_id) REFERENCES produtos(id)
            
        )  
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
        id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_usuario TEXT NOT NULL,
        pin_usuario TEXT NOT NULL
        
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pedidos (
        id_pedido INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER NOT NULL,
        data_pedido DATE NOT NULL,
        valor_total REAL NOT NULL,
        FOREIGN KEY(usuario_id) REFERENCES usuarios(id_usuario)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS itens_pedido (
        id_item INTEGER PRIMARY KEY AUTOINCREMENT,
        pedido_id INTEGER NOT NULL,
        lote_id INTEGER NOT NULL,
        quantidade_vendida INTEGER NOT NULL,
        pv_registrado REAL,
        FOREIGN KEY(pedido_id) REFERENCES pedidos(id_pedido),
        FOREIGN KEY(lote_id) REFERENCES lotes(id_lote) 
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alertas_lote (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_pedido INTEGER NOT NULL,
        id_produto INTEGER NOT NULL,
        id_lote_correto INTEGER NOT NULL, 
        id_lote_vendido INTEGER NOT NULL,
        id_usuario INTEGER NOT NULL,
        data DATE NOT NULL,
        negligencia INTEGER NOT NULL
        )           
    ''')
    connect_db.commit()

def save_products(connect_db: Connection, list_products: list[Product]):
    'Salva uma lista de produtos no banco de dados | insere novos ou atualiza a quantidade e o preço de custo dos produtos existentes'
    'save an list of products in the database | insert an new or update of the quantity/cost-price of existing products'
    if not list_products:
        return
    
    cursor = connect_db.cursor()    

    for product in list_products: 
        cursor.execute('''
            INSERT INTO produtos (id, ean, nome_produto, preco_venda)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                ean = excluded.ean,
                nome_produto = excluded.nome_produto,
                preco_venda = excluded.preco_venda;
            ''', 
            (
                product.id,
                product.ean,
                product.name,
                product.sale_price
                
            ))
        
        save_batch = product.batch[0]     

        cursor.execute('''
            INSERT INTO lotes (id_lote_fisico, produto_id, quantidade, preco_custo, data_validade, data_entrada)
            VALUES (?, ?, ?, ?, ?, ?)            
            ''',
            
            
            (
                save_batch.physical_batch_id,
                save_batch.product_id,
                save_batch.quantity,
                save_batch.cost_price,
                save_batch.expiration_date,
                save_batch.entry_date
            
            ))
        

    connect_db.commit()
    logging.info(f'\n [INFO] {len(list_products)} produtos foram salvos/atualizados no banco de dados.')

def products_existing(connect_db: Connection, product: Product) -> bool:
    'verify if an product with determined id already existing on the database'

    connector = connect_db.cursor()

    connector.execute ('''
            SELECT COUNT(*) 
            FROM produtos 
            WHERE id = ?
        ''',                
        (
            product.id,
                          
        ))              
    
    db_answer = connector.fetchone()
    products_answer = db_answer[0]
   
    if products_answer > 0:
        return True     
    else:
        return False

def search_product(connect_db: Connection, product: Product):
    'search for a product using an object -> Product'
    
    connector = connect_db.cursor()

    connector.execute('''
                     
            SELECT id, nome_produto, preco_venda, data_validade 
            FROM produtos 
            JOIN lotes 
            ON produtos.id = lotes.produto_id 
            WHERE produtos.id = ? 
            ORDER BY data_validade ASC 
            LIMIT 1 
        
        ''', 
        (
            product.id,
            
        ))
    
    db_answer = connector.fetchone()
    return db_answer

def search_product_name(connect_db: Connection, search: str) -> list:
    'search an product using the integer name or a part of the name of respective Product '
    connector = connect_db.cursor()

    connector.execute('''
        
        SELECT id, nome_produto, ean, preco_venda, id_lote, id_lote_fisico, produto_id, quantidade, preco_custo, data_validade, data_entrada
        FROM produtos
        JOIN lotes
        ON produtos.id = lotes.produto_id
        WHERE produtos.nome_produto LIKE ?
        ORDER BY data_validade ASC        
    
    ''',
    (
        f'%{search}%',
    ))

    db_answer = connector.fetchall()    
    return db_answer

def register_user(connect_db: Connection, user: User):
    'register an new user on database'
    
    connector = connect_db.cursor()

    connector.execute('''
            INSERT INTO usuarios (nome_usuario, pin_usuario)
            VALUES (?, ?)
            ''',
            (
                user.user_name,
                user.user_pin               
            
            ))

    connect_db.commit()
    print('=' * 30)
    logging.info(f'[INFO] O usuário, {user.user_name} foi cadastrado.')
    print('=' * 30)

def search_user(connect_db: Connection, user: str) -> tuple:
    'search an user by name, but the function returns all contained data in database'

    connector = connect_db.cursor()

    connector.execute('''
            SELECT id_usuario, nome_usuario, pin_usuario
            FROM usuarios
            WHERE usuarios.nome_usuario = ?
            LIMIT 1
            
        ''',
        (
            user,
            
        ))
    
    db_answer = connector.fetchone()    
    return db_answer
  
def register_batch_alert(connect_db: Connection, order_id, product_id: Product, user_id: User, batch_sold: Batch, batch_correct: Batch):
    'register of alert of the batch sold incorretly'

    today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if batch_sold != batch_correct:
        neglect = 1
    else:
        neglect = 0

    connector = connect_db.cursor()
    connector.execute('''
        INSERT INTO alertas_lote (id_pedido, id_produto, id_usuario, id_lote_vendido, id_lote_correto, data, negligencia)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''',
        (
            order_id,
            product_id.id,
            user_id.user_id,
            batch_sold.physical_batch_id,
            batch_correct.physical_batch_id,
            today,
            neglect
        ))
    connect_db.commit()

    print('=' * 30)
    logging.info(f'[INFO] Os dados dessa venda foram registrados.')
    print('=' * 30)

######################################################################################################################
