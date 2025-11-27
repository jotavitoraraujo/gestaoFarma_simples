import pytest
pytestmark = pytest.mark.skip(reason = 'PAUSE')
from datetime import date
from system.models.product import Product
from system.models.product import Batch
from system.models.item import Item

######################################### --- OBJECTS INSTANCES ---############################################################
def date_instance():
    date_object = date(2026, 1, 1)
    return date_object

#########################################

def item_instance():
    produto = Product (
        id = 0,
        supplier_code = '123',
        ean = 123456789101112,
        name = 'PRODUTO DE TESTE',
        sale_price = float(10.0)
    )

    lote = Batch (
        id = 0,
        physical_id = 'AB123CD',
        product_id = 0,
        quantity = 5,
        unit_cost_amount = float(5.0),
        use_by_date = date_instance(),
        received_date = date.today()
    )

    item  = Item (
        product = produto,
        batch = lote,
        quantity_sold = 3
    )
    return item

######################################### --- TEST FUNCTION _item_calculate_subtotal ---######################################################

def test_item_calcular_subtotal():
    'a funcao tem como objetivo testar a classe Item e seu metodo calcular_subtotal()'
    
    item = item_instance()
    resultado_teste = item.calculate_subtotal()
    assert resultado_teste == 30.0

######################################### --- TEST FUNCTION _convert_price_str ---############################################################
@pytest.mark.parametrize('current_date, expiration_date, product_price, product_cost, expected_discounted_price', 
    [
        (date(2025, 8, 14), date(2025, 8, 21), 10.0, 5.0, 10.0,), # 80% discount apply
        (date(2025, 8, 14), date(2025, 8, 27), 10.0, 5.0, 5.0,), # '' 50% apply
        (date(2025, 8, 14), date(2025, 9, 3), 10.0, 5.0, 7.0,), # '' 30% apply
        (date(2025, 8, 14), date(2025, 9, 10), 10.0, 5.0, 8.0) # '' 20% apply

])

#########################################

def test_get_discounted_price(current_date: date, expiration_date: date, product_price: float, product_cost: float, expected_discounted_price: float) -> float:

    def nested_item_instance():
        product_instance = Product (
            id = '0',
            supplier_code = '123',
            ean = 123456789101112,
            name = 'Test Product',
            sale_price = product_price
        )

        batch_instance = Batch (
            id = 0,
            physical_id = 'AB123CD',
            product_id = '0',
            quantity = 1,
            unit_cost_amount = product_cost,
            use_by_date = expiration_date,
            received_date = '01/01/2026'
        )

        item_test = Item (
            product = product_instance,
            batch = batch_instance,
            quantity_sold = 1
        )
        return item_test
        
    
    call_item_instance = nested_item_instance()
    call_test = call_item_instance.get_discounted_price(current_date)
    assert call_test == expected_discounted_price

######################################### --- TEST FUNCTION XXXXXXXXXXXXXXX ---############################################################