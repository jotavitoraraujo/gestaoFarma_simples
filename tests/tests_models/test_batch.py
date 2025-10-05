### --- IMPORTS --- ###
from system.models.batch import Batch
from system.models.fiscal import PurchaseTaxDetails
from decimal import Decimal
from datetime import date

purchase_tax_details = PurchaseTaxDetails (
    id = 1,
    cfop = '1234',
    icms_cst = '1234',
    icms_st_base_amount = Decimal('0.1'),
    icms_st_percentage = Decimal('0.2'),
    icms_st_retained_amount = Decimal('0.3'),
    pis_cst = '1234',
    cofins_cst = '1234'
)

### --- ARRANGE/ACT PHASE --- ###
batch_test_A = Batch (
    id = 1,
    physical_id = '123AB45',
    product_id = 1,
    quantity = Decimal('1'),
    unit_cost_amount = Decimal('0.99'),
    other_expenses_amount = Decimal('1.99'),
    use_by_date = date(2035, 9, 21),
    manufacturing_date = date(2035, 8, 21),
    received_date = date.today(),
    taxation_details = purchase_tax_details
)

batch_test_B = Batch (
    id = 1,
    physical_id = '123AB45',
    product_id = 1,
    quantity = Decimal('1'),
    unit_cost_amount = Decimal('0.99'),
    other_expenses_amount = Decimal('1.99'),
    use_by_date = date(2035, 9, 21),
    manufacturing_date = date(2035, 8, 21),
    received_date = date.today(),
    taxation_details = purchase_tax_details
)

batch_test_C = Batch (
    id = 1,
    physical_id = '123AB46',
    product_id = 1,
    quantity = Decimal('1'),
    unit_cost_amount = Decimal('0.98'),
    other_expenses_amount = Decimal('1.98'),
    use_by_date = date(2035, 9, 21),
    manufacturing_date = date(2035, 8, 21),
    received_date = date.today(),
    taxation_details = purchase_tax_details
)

repr_string = f'''
        --- Batch Atributes ---
        1. Batch ID: {batch_test_A.id}
        2. Pyshical Batch ID: {batch_test_A.physical_id}
        3. Product ID: {batch_test_A.product_id}
        4. Quantity: {batch_test_A.quantity}
        5. Cost price: {batch_test_A.unit_cost_amount}
        6. Cost extras: {batch_test_A.other_expenses_amount}
        7. Expiration date: {batch_test_A.use_by_date}
        8. Manufacturing: {batch_test_A.manufacturing_date}
        9. Entry date: {batch_test_A.received_date}
        {batch_test_A.taxation_details}
    '''
repr_real = repr(batch_test_A)

### --- ASSERT PHASE __init__ --- ###
def test_batch_construiction():
    assert batch_test_A.id == 1
    assert batch_test_A.physical_id == '123AB45'
    assert batch_test_A.product_id == 1
    assert batch_test_A.quantity == Decimal('1')
    assert batch_test_A.unit_cost_amount == Decimal('0.99')
    assert batch_test_A.other_expenses_amount == Decimal('1.99')
    assert batch_test_A.use_by_date == date(2035, 9, 21)
    assert batch_test_A.manufacturing_date == date(2035, 8, 21)
    assert batch_test_A.received_date == date.today()
    assert batch_test_A.taxation_details == purchase_tax_details

### --- ASSERT PHASE __eq__ --- ###
def test_batch_equality():
    assert batch_test_A == batch_test_A
    assert batch_test_A == batch_test_B
    assert batch_test_A != batch_test_C

### --- ASSERT PHASE __repr__ --- ###
def test_batch_representation():
    assert repr_real == repr_string

