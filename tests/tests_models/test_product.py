### IMPORTS ###
from system.models.product import Product
from system.models.batch import Batch

### --- ARRANGE/ACT PHASE --- ###

product_test_a = Product (
    id = 1,
    supplier_code = '123',
    ean = 'TEST123TEST',
    name = 'PRODUCT TEST',
    sale_price = 1.99
)

product_test_b = Product (
    id = 1,
    supplier_code = '123',
    ean = 'TEST123TEST',
    name = 'PRODUCT TEST',
    sale_price = 1.99
)

product_test_c = Product (
    id = 1,
    supplier_code = '123',
    ean = 'TEST123TEST',
    name = 'PRODUCT TEST DIFFERENT',
    sale_price = 1.99
)

repr_string = f'''
        --- Product Atributes ---
        1. ID Autoincrement: {product_test_a.id}
        2. ID Supplier: {product_test_a.supplier_code}
        3. EAN: {product_test_a.ean}
        4. Name: {product_test_a.name}
        5. Sale price: {product_test_a.sale_price}
        '''
repr_real = repr(product_test_a)

### --- ASSERT PHASE __init__ --- ###
def test_product_construition():
    assert product_test_a.id == 1
    assert product_test_a.supplier_code == '123'
    assert product_test_a.ean == 'TEST123TEST'
    assert product_test_a.name == 'PRODUCT TEST'
    assert product_test_a.sale_price == 1.99

### --- ASSERT PHASE __eq__ --- ###
def test_product_equality():    
    assert product_test_a == product_test_a
    assert product_test_a == product_test_b
    assert product_test_a != product_test_c

### --- ASSERT PHASE __repr__ --- ###
def test_product_representation():
    assert repr_string == repr_real