import pytest
from datetime import date
from sistema.modelos.produto import Produto
from sistema.modelos.produto import Lote
from sistema.modelos.item import Item


data_validade = date(2025, 8, 12)

def instancia_item():
    produto = Produto (
        id = 0,
        ean = 123456789101112,
        nome = 'PRODUTO DE TESTE',
        preco_venda = float(10.0)
    )

    lote = Lote (
        id_lote = 0,
        id_lote_fisico = 'AB123CD',
        produto_id = 0,
        quantidade = 5,
        preco_custo = float(5.0),
        data_validade = data_validade,
        data_entrada = date.today()
    )

    item  = Item (
        produto = produto,
        lote = lote,
        quantidade_vendida = 3
    )
    return item

#######################################################################################################################################################

def test_item_calcular_subtotal():
    'a funcao tem como objetivo testar a classe Item e seu metodo calcular_subtotal()'
    
    item = instancia_item()
    resultado_teste = item.calcular_subtotal()
    assert resultado_teste == 30.0


def test_item_desconto():
    'a funcao tem como objetivo testar a classe Item e seu metodo desconto()'

    item = instancia_item()
    resultado_teste = item.desconto()    
    desconto = item.produto.preco_venda - (item.produto.preco_venda * 0.8)
    assert resultado_teste == 10.0
    
    # OBS: as funcoes precisam ter algumas variaveis ajustadas para se adequar ao que vc deseja testar (validade, preco de venda ou custo, qtd)
    # OBS: 10/08/25 -> 100% funcional