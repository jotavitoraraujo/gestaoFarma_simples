### IMPORTS ###
from system.models.product import Product
from system.models.fiscal import FiscalProfile
from decimal import Decimal

fiscal_profile = FiscalProfile (
    id = 1,
    ncm = '1234',
    cest = '1234',
    origin_code = '1234' 
)

### --- ARRANGE/ACT PHASE --- ###
product_test_A = Product (
    id = 1,
    supplier_code = '1234',
    ean = 'TEST123TEST',
    name = 'PRODUCT TEST',
    anvisa_code = '1234',
    sale_price = Decimal('1.99'),
    max_consumer_price = Decimal('2.99'),
    fiscal_profile = fiscal_profile
)

product_test_B = Product (
    id = 1,
    supplier_code = '1234',
    ean = 'TEST123TEST',
    name = 'PRODUCT TEST',
    anvisa_code = '1234',
    sale_price = Decimal('1.99'),
    max_consumer_price = Decimal('2.99'),
    fiscal_profile = fiscal_profile
)

product_test_C = Product (
    id = 1,
    supplier_code = '12345',
    ean = 'TEST123TEST',
    name = 'PRODUCT TEST',
    anvisa_code = '12345',
    sale_price = Decimal('1.98'),
    max_consumer_price = Decimal('2.98'),
    fiscal_profile = fiscal_profile
)

repr_string = f'''
        --- Product Atributes ---
        1. ID Autoincrement: {product_test_A.id}
        2. ID Supplier: {product_test_A.supplier_code}
        3. EAN: {product_test_A.ean}
        4. Name: {product_test_A.name}
        5. ANVISA Code: {product_test_A.anvisa_code}
        6. Sale price: {product_test_A.sale_price}
        7. MAX Price Consumer: {product_test_A.max_consumer_price:.2f}
        {product_test_A.fiscal_profile}
        '''
repr_real = repr(product_test_A)

### --- ASSERT PHASE __init__ --- ###
def test_product_construition():
    assert product_test_A.id == 1
    assert product_test_A.supplier_code == '1234'
    assert product_test_A.ean == 'TEST123TEST'
    assert product_test_A.name == 'PRODUCT TEST'
    assert product_test_A.anvisa_code == '1234'
    assert product_test_A.sale_price == Decimal('1.99')
    assert product_test_A.max_consumer_price == Decimal('2.99')
    assert product_test_A.fiscal_profile == fiscal_profile

### --- ASSERT PHASE __eq__ --- ###
def test_product_equality():    
    assert product_test_A == product_test_A
    assert product_test_A == product_test_B
    assert product_test_A != product_test_C

### --- ASSERT PHASE __repr__ --- ###
def test_product_representation():
    assert repr_string == repr_real
