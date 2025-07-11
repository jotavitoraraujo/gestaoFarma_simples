import sqlite3
from datetime import datetime
from pathlib import Path
pasta_sistema = Path(__file__).parent
db_file = pasta_sistema.parent/'dados'/'farmacia.db'

def criar_tabelas():
    'Cria tabela de produtos no BD se ela não existir | Utiliza um comando SQL pra criar a tabela'
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
    
    print("Tabela 'produtos' verificada/criada com sucesso.")
    conn.commit()
    conn.close()

def salvar_produtos(lista_produtos):
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
                produto['codigo'],
                produto['nome'],
                produto['preco_venda']
                
            ))
        
        data_hoje = datetime.now().strftime('%Y-%m-%d')

        cursor.execute('''
            INSERT INTO lotes (produto_id, quantidade, preco_custo, data_validade, data_entrada)
            VALUES (?, ?, ?, ?, ?)            
            ''',
            (     
                produto['codigo'],
                produto['quantidade'],
                produto['preco_custo'],
                produto['data_validade'],
                data_hoje
            ))
        

    conn.commit()
    conn.close()
    print(f'\n [SUCESSO] {len(lista_produtos)} produtos foram salvos/atualizados no banco de dados.')

def produtos_existentes(produto_id):
    'verifica se um produto com determinado id já existe no database'

    conectar_db = sqlite3.connect(db_file)
    conector = conectar_db.cursor()

    conector.execute ('SELECT COUNT(*) FROM produtos WHERE id = ?', (produto_id,))              
    resposta_db = conector.fetchone()
    resposta_produtos = resposta_db[0]

    conectar_db.close()
   
    if resposta_produtos > 0:
        return True     
    else:
        return False

def buscar_produto(produto_id):

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
        
        ''', (produto_id,)
        
        )
    
    resposta_db = conector.fetchone()
    
    conectar_db.close()
    
    return resposta_db
