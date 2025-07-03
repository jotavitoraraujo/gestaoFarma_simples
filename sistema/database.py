import sqlite3

def criar_tabela_produtos():
    'Cria tabela de produtos no BD se ela não existir'
    'Utiliza um comando SQL pra criar a tabela'
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
            data_validade TEXT NOT NULL,
            curva_abc TEXT
        )
    ''')
    print("Tabela 'produtos' verificada/criada com sucesso.")
    conn.commit()
    conn.close()