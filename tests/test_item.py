import pytest
from unittest.mock import patch
from datetime import date
from sistema.modulos.validadores_input import date_validator
from sistema.modelos.produto import Produto
from sistema.modelos.produto import Lote
from sistema.modelos.sale_item import SaleItem


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

    item  = SaleItem (
        product = produto,
        batch = lote,
        quantity_sold = 3
    )
    return item

#######################################################################################################################################################

def test_item_calcular_subtotal():
    'a funcao tem como objetivo testar a classe Item e seu metodo calcular_subtotal()'
    
    item = instancia_item()
    resultado_teste = item.calculate_subtotal()
    assert resultado_teste == 30.0


@pytest.mark.parametrize('current_date, expiration_date, product_price, product_cost, expected_discounted_price', 
    [
        (date(2025, 8, 14), date(2025, 8, 21), 10.0, 5.0, 10.0,),
        (date(2025, 8, 14), date(2025, 8, 27), 10.0, 5.0, 5.0,),
        (date(2025, 8, 14), date(2025, 9, 3), 10.0, 5.0, 7.0,),
        (date(2025, 8, 14), date(2025, 9, 10), 10.0, 5.0, 8.0)

])

def test_get_discounted_price(current_date: date, expiration_date: date, product_price: float, product_cost: float, expected_discounted_price: float) -> float:

    def item_instance():
        product_instance = Produto (
            id = '0',
            ean = 123456789101112,
            nome = 'Test Product',
            preco_venda = product_price
        )

        batch_instance = Lote (
            id_lote = 0,
            id_lote_fisico = 'AB123CD',
            produto_id = '0',
            quantidade = 1,
            preco_custo = product_cost,
            data_validade = expiration_date,
            data_entrada = '01/01/2026'
        )

        item_test = SaleItem (
            product = product_instance,
            batch = batch_instance,
            quantity_sold = 1
        )
        return item_test
        
    
    call_item_instance = item_instance()
    call_test = call_item_instance.get_discounted_price(current_date)
    assert call_test == expected_discounted_price