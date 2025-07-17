class Produto:
    def __init__(self, id, ean, nome, preco_venda):
        self.id = id
        self.ean = ean
        self.nome = nome
        self.preco_venda = preco_venda
        self.lotes = []