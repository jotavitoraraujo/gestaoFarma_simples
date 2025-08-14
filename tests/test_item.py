import pytest
from datetime import date
from sistema.modelos.product import Product
from sistema.modelos.product import Batch
from sistema.modelos.sale_item import SaleItem


data_validade = date(2025, 8, 12)

def instancia_item():
    produto = Product (
        id = 0,
        ean = 123456789101112,
        name = 'PRODUTO DE TESTE',
        sale_price = float(10.0)
    )

    lote = Batch (
        batch_id = 0,
        physical_batch_id = 'AB123CD',
        product_id = 0,
        quantity = 5,
        cost_price = float(5.0),
        expiration_date = data_validade,
        entry_date = date.today()
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
        (date(2025, 8, 14), date(2025, 8, 21), 10.0, 5.0, 10.0,), # 80% discount apply
        (date(2025, 8, 14), date(2025, 8, 27), 10.0, 5.0, 5.0,), # '' 50% apply
        (date(2025, 8, 14), date(2025, 9, 3), 10.0, 5.0, 7.0,), # '' 30% apply
        (date(2025, 8, 14), date(2025, 9, 10), 10.0, 5.0, 8.0) # '' 20% apply

])

def test_get_discounted_price(current_date: date, expiration_date: date, product_price: float, product_cost: float, expected_discounted_price: float) -> float:

    def item_instance():
        product_instance = Product (
            id = '0',
            ean = 123456789101112,
            name = 'Test Product',
            sale_price = product_price
        )

        batch_instance = Batch (
            batch_id = 0,
            physical_batch_id = 'AB123CD',
            product_id = '0',
            quantity = 1,
            cost_price = product_cost,
            expiration_date = expiration_date,
            entry_date = '01/01/2026'
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