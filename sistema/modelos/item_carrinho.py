from sistema.modelos.produto import Produto
from sistema.modelos.lote import Lote

class item_carrinho:
    def __init__(self, produto: Produto, lote: Lote, quantidade):
        self.produto = produto
        self.lote = lote
        self.lote.quantidade = quantidade