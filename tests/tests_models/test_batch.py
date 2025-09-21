### --- IMPORTS --- ###
from system.models.batch import Batch

### --- ARRANGE/ACT PHASE --- ###
batch_test_a = Batch (
    batch_id = '123',
    physical_batch_id = '123AB45',
    product_id = '1234',
    quantity = 1,
    cost_price = 0.99,
    expiration_date = '2035-9-21',
    entry_date = '2034-9-20'
)

batch_test_b = Batch (
    batch_id = '123',
    physical_batch_id = '123AB45',
    product_id = '1234',
    quantity = 1,
    cost_price = 0.99,
    expiration_date = '2035-9-21',
    entry_date = '2034-9-20'
)

batch_test_c = Batch (
    batch_id = '123',
    physical_batch_id = '123AB45',
    product_id = '1234',
    quantity = 1,
    cost_price = 0.98,
    expiration_date = '2035-9-21',
    entry_date = '2034-9-20'
)

repr_string = f'''
        --- Batch Atributes ---
        1. Batch ID: {batch_test_a.batch_id}
        2. Pyshical Batch ID: {batch_test_a.physical_batch_id}
        3. Product ID: {batch_test_a.product_id}
        4. Quantity: {batch_test_a.quantity}
        5. Cost price: {batch_test_a.cost_price}
        6. Expiration date: {batch_test_a.expiration_date}
        7. Entry date: {batch_test_a.entry_date}
    '''
repr_real = repr(batch_test_a)

### --- ASSERT PHASE __init__ --- ###
def test_batch_construiction():
    assert batch_test_a.batch_id == '123'
    assert batch_test_a.physical_batch_id == '123AB45'
    assert batch_test_a.product_id == '1234'
    assert batch_test_a.quantity == 1
    assert batch_test_a.cost_price == 0.99
    assert batch_test_a.expiration_date == '2035-9-21'
    assert batch_test_a.entry_date == '2034-9-20'

### --- ASSERT PHASE __eq__ --- ###
def test_batch_equality():
    assert batch_test_a == batch_test_a
    assert batch_test_a == batch_test_b
    assert batch_test_a != batch_test_c

### --- ASSERT PHASE __repr__ --- ###
def test_batch_representation():
    assert repr_real == repr_string

