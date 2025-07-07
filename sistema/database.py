import sqlite3
import os
db_file = os.path.join('dados', 'farmacia.db')

def criar_tabela_produtos():
    'Cria tabela de produtos no BD se ela não existir | Utiliza um comando SQL pra criar a tabela'
    conn = sqlite3.connect('dados/farmacia.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id TEX PRIMARY KEY,
            nome_produto TEXT NOT NULL,
            preco_custo REAL NOT NULL,
            preco_venda REAL,
            quantidade INTEGER NOT NULL,
            estoque_minimo INTEGER,
            data_validade TEXT,
            curva_abc TEXT
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
            INSERT INTO produtos (id, nome_produto, preco_custo, quantidade, data_validade, preco_venda)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                quantidade = quantidade + excluded.quantidade,
                preco_custo = excluded.preco_custo,
                data_validade = excluded.data_validade,
                preco_venda = excluded.preco_venda;
            ''', (
                produto['codigo'],
                produto['nome'],
                produto['preco_custo'],
                produto['quantidade'],
                produto['data_validade'],
                produto['preco_venda']
                
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
