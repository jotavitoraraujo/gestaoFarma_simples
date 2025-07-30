import sqlite3
from pathlib import Path
from sistema.modelos.produto import Produto 
from sistema.modelos.usuario import Usuario
pasta_sistema = Path(__file__).parent
db_file = pasta_sistema.parent/'dados'/'farmacia.db'

def criar_tabelas():
    'Cria tabela de produtos/lotes e usuários no db se ela não existir | Utiliza um comando SQL pra criar a tabela'
    conn = sqlite3.connect('dados/farmacia.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id TEXT PRIMARY KEY,
            nome_produto TEXT NOT NULL,            
            preco_venda REAL,            
            estoque_minimo INTEGER,            
            curva_abc TEXT
            
        )
    ''')    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lotes (
        id_lote INTEGER PRIMARY KEY AUTOINCREMENT,
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
    
    print("[SUCESSO] Tabelas criadas.")
    conn.commit()
    conn.close()

def salvar_produtos(lista_produtos: list[Produto]):
    'Salva uma lista de produtos no banco de dados | insere novos ou atualiza a quantidade e o preço de custo dos produtos existentes'
    if not lista_produtos:
        return
    
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()    

    for produto in lista_produtos: 
        cursor.execute('''
            INSERT INTO produtos (id, nome_produto, preco_venda)
            VALUES (?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                nome_produto = excluded.nome_produto,
                preco_venda = excluded.preco_venda;
            ''', 
            (
                produto.id,
                produto.nome,
                produto.preco_venda
                
            ))
        
        salvar_lote = produto.lotes[0]     

        cursor.execute('''
            INSERT INTO lotes (produto_id, quantidade, preco_custo, data_validade, data_entrada)
            VALUES (?, ?, ?, ?, ?)            
            ''',
            
            
            (
                salvar_lote.produto_id,
                salvar_lote.quantidade,
                salvar_lote.preco_custo,
                salvar_lote.data_validade,
                salvar_lote.data_entrada
            
            ))
        

    conn.commit()
    conn.close()
    print(f'\n [SUCESSO] {len(lista_produtos)} produtos foram salvos/atualizados no banco de dados.')

def produtos_existentes(produto: Produto):
    'verifica se um produto com determinado id já existe no database'

    conectar_db = sqlite3.connect(db_file)
    conector = conectar_db.cursor()

    conector.execute ('SELECT COUNT(*) FROM produtos WHERE id = ?', 
                        
                        (
                          produto.id,
                          
                        ))              
    
    resposta_db = conector.fetchone()
    resposta_produtos = resposta_db[0]

    conectar_db.close()
   
    if resposta_produtos > 0:
        return True     
    else:
        return False

def buscar_produto(produto: Produto):
    'busca um produto a partir do tipo Produto'
    conectar_db = sqlite3.connect(db_file)
    conector = conectar_db.cursor()

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
    
    conectar_db.close()
    
    return resposta_db

def inserir_usuario(usuario: Usuario):
    
    'cadastra um novo usuário no database'
    
    conectar_db = sqlite3.connect(db_file)
    conector = conectar_db.cursor()

    conector.execute('''
            INSERT INTO usuarios (nome_usuario, pin_usuario)
            VALUES (?, ?)
            ''',
            (
                usuario.nome_usuario,
                usuario.pin_usuario               
            
            ))

    conectar_db.commit()
    conectar_db.close()
    print('=' * 30)
    print(f'[SUCESSO] O usuário, {usuario.nome_usuario} foi cadastrado.')
    print('=' * 30)

def buscar_usuario(usuario: Usuario):
    'busca um usuário por nome, mas, retorna todos seus dados contidos no database'
    
    conectar_db = sqlite3.connect(db_file)
    conector = conectar_db.cursor()

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
    
    conectar_db.close()
    
    return resposta_db