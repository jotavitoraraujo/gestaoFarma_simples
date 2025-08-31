#################### --- IMPORTS --- #######################
from sqlite3 import Connection
from pathlib import Path
from sistema.modelos.product import Product 
from sistema.modelos.usuario import Usuario
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
    adapter_format_date = datetime.strptime(convert_object_str, '%Y-%m-%d').date()
    return adapter_format_date

#################### --- TRANSLATORS --- ####################
sqlite3.register_adapter(datetime.date, date_adapter)
sqlite3.register_converter('date', date_conversor)

###################### --- PATH FOR DATABASE 'farmacia.db' --- #############################
pasta_sistema = Path(__file__).parent
db_file = pasta_sistema.parent/'dados'/'farmacia.db'

###################### --- CONNECTION FUNCTION WITH DATABASE --- #############################
@contextlib.contextmanager
def connect_db():
    'database connection control'
    
    connect_db = None
    try:
        connect_db = sqlite3.connect(db_file)
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
    'Cria tabela de produtos/lotes e usuários no db se ela não existir | Utiliza um comando SQL pra criar a tabela'
    
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
        data_validade TEXT NOT NULL,
        data_entrada TEXT NOT NULL,                           
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
        data_pedido TEXT NOT NULL,
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
        data TEXT NOT NULL,
        negligencia INTEGER NOT NULL
        )           
    ''')
    connect_db.commit()

def save_products(connect_db: Connection, list_products: list[Product]):
    'Salva uma lista de produtos no banco de dados | insere novos ou atualiza a quantidade e o preço de custo dos produtos existentes'
    if not list_products:
        return
    
    cursor = connect_db.cursor()    

    for produto in list_products: 
        cursor.execute('''
            INSERT INTO produtos (id, ean, nome_produto, preco_venda)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                ean = excluded.ean,
                nome_produto = excluded.nome_produto,
                preco_venda = excluded.preco_venda;
            ''', 
            (
                produto.id,
                produto.ean,
                produto.name,
                produto.sale_price
                
            ))
        
        salvar_lote = produto.batch[0]     

        cursor.execute('''
            INSERT INTO lotes (id_lote_fisico, produto_id, quantidade, preco_custo, data_validade, data_entrada)
            VALUES (?, ?, ?, ?, ?, ?)            
            ''',
            
            
            (
                salvar_lote.physical_batch_id,
                salvar_lote.product_id,
                salvar_lote.quantity,
                salvar_lote.cost_price,
                salvar_lote.expiration_date,
                salvar_lote.entry_date
            
            ))
        

    connect_db.commit()
    logging.info(f'\n [INFO] {len(list_products)} produtos foram salvos/atualizados no banco de dados.')

def produtos_existentes(connect_db: Connection, produto: Product):
    'verifica se um produto com determinado id já existe no database'

    conector = connect_db.cursor()

    conector.execute ('SELECT COUNT(*) FROM produtos WHERE id = ?', 
                        
                        (
                          produto.id,
                          
                        ))              
    
    resposta_db = conector.fetchone()
    resposta_produtos = resposta_db[0]
   
    if resposta_produtos > 0:
        return True     
    else:
        return False

def buscar_produto(connect_db: Connection, produto: Product):
    'busca um produto a partir do tipo Produto'
    
    conector = connect_db.cursor()

    conector.execute('''
                     
            SELECT id, nome_produto, preco_venda, data_validade 
            FROM produtos 
            JOIN lotes 
            ON produtos.id = lotes.produto_id 
            WHERE produtos.id = ? 
            ORDER BY data_validade ASC 
            LIMIT 1 
        
        ''', 
        (
            produto.id,
            
        ))
    
    resposta_db = conector.fetchone()
    
    return resposta_db

def buscar_produto_nome(connect_db: Connection, busca: str) -> list:

    conector = connect_db.cursor()

    conector.execute('''
        
        SELECT id, nome_produto, ean, preco_venda, id_lote, id_lote_fisico, produto_id, quantidade, preco_custo, data_validade, data_entrada
        FROM produtos
        JOIN lotes
        ON produtos.id = lotes.produto_id
        WHERE produtos.nome_produto LIKE ?
        ORDER BY data_validade ASC        
    
    ''',
    (
        f'%{busca}%',
    ))

    resposta_db = conector.fetchall()    
    return resposta_db

def inserir_usuario(connect_db: Connection, usuario: Usuario):
    
    'cadastra um novo usuário no database'
    
    conector = connect_db.cursor()

    conector.execute('''
            INSERT INTO usuarios (nome_usuario, pin_usuario)
            VALUES (?, ?)
            ''',
            (
                usuario.nome_usuario,
                usuario.pin_usuario               
            
            ))

    connect_db.commit()
    print('=' * 30)
    logging.info(f'[INFO] O usuário, {usuario.nome_usuario} foi cadastrado.')
    print('=' * 30)

def buscar_usuario(connect_db: Connection, usuario: Usuario):
    'busca um usuário por nome, mas, retorna todos seus dados contidos no database'

    conector = connect_db.cursor()

    conector.execute('''
            SELECT id_usuario, nome_usuario, pin_usuario
            FROM usuarios
            WHERE usuarios.nome_usuario = ?
            LIMIT 1
            
        ''',
        (
            usuario.nome_usuario,
            
        ))
    
    resposta_db = conector.fetchone()    
    return resposta_db
  
def registrar_alerta_lote(connect_db: Connection, id_pedido, id_produto: Product, id_usuario: Usuario, lote_vendido: Batch, lote_correto: Batch):
    'registra o alerta do lote vendido incorretamente'

    data_hoje = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if lote_vendido != lote_correto:
        negligencia = 1
    else:
        negligencia = 0

    conector = connect_db.cursor()

    conector.execute('''
        INSERT INTO alertas_lote (id_pedido, id_produto, id_usuario, id_lote_vendido, id_lote_correto, data, negligencia)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''',
        (
            id_pedido,
            id_produto.id,
            id_usuario.id_usuario,
            lote_vendido.physical_batch_id,
            lote_correto.physical_batch_id,
            data_hoje,
            negligencia
        ))
    
    connect_db.commit()

    print('=' * 30)
    logging.info(f'[INFO] Os dados dessa venda foram registrados.')
    print('=' * 30)

######################################################################################################################