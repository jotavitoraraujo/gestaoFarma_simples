import pytest
from unittest.mock import patch
from pathlib import Path
from sistema.modelos.product import Product
from sistema.modelos.batch import Batch
from sistema.modulos import xml_parser
from datetime import datetime

######################################### --- TEST SUIT FROM EXTRACT DATA NFE FUNCTION --- ########################################
### DATE (TODAY) INSTANCE ###
@pytest.fixture
def object_today():
    today = datetime.now().strftime('%Y-%m-%d')
    return today

### PRODUCTs AND BATCHs INSTANCEs ###
@pytest.fixture
def dipirona_product(object_today):     # <-- Functional Cenario
    product_instance = Product (
        id = '12345',
        ean = '7891020304050',
        name = 'DIPIRONA 500MG COM 10 COMPRIMIDOS',
        sale_price = None        
    )
    batch_instance = Batch (
        batch_id = None,
        physical_batch_id = None,
        product_id = product_instance.id,
        quantity = float(20.0),
        cost_price = float(8.50),
        expiration_date = None,
        entry_date = object_today
    )
    product_instance.batch.append(batch_instance)
    dipirona_instance = product_instance    
    return dipirona_instance

@pytest.fixture
def dipirona_product_unstable(object_today):     # <-- EAN Empty / Unstable Cenario
    'fixture of the dipirona_product instance with ean_tag empty'

    product_instance = Product (
        id = '12345',
        ean = None,
        name = 'DIPIRONA 500MG COM 10 COMPRIMIDOS',
        sale_price = None
    )

    batch_instance = Batch (
        batch_id = None,
        physical_batch_id = None,
        product_id = product_instance.id,
        quantity = float(20.0),
        cost_price = float(8.5),
        expiration_date = None,
        entry_date = object_today
    )

    product_instance.batch.append(batch_instance)
    dipirona_product_unstable = product_instance
    return dipirona_product_unstable

@pytest.fixture
def vitamina_product(object_today):     # <-- Functional Cenario
    product_instance = Product (
        id = '67890',
        ean = '7895040302010',
        name = 'VITAMINA C EFERVESCENTE',
        sale_price = None
    )
    batch_instance = Batch (
        batch_id = None,
        physical_batch_id = None,
        product_id = product_instance.id,
        quantity = float(15.0),
        cost_price = float(12.75),
        expiration_date = None,
        entry_date = object_today
    )
    product_instance.batch.append(batch_instance)
    vitamina_instance = product_instance
    return vitamina_instance

@pytest.fixture
def algodao_product(object_today):      # <-- Functional Cenario
    product_instance = Product (
        id = '101112',
        ean = None,
        name = 'ALGODÃO HIDRÓFILO 50G',
        sale_price = None
    )
    batch_instance = Batch (
        batch_id = None,
        physical_batch_id = None,
        product_id = product_instance.id,
        quantity = float(30.0),
        cost_price = float(3.20),
        expiration_date = None,
        entry_date = object_today
    )
    product_instance.batch.append(batch_instance)
    algodao_instance = product_instance
    return algodao_instance

### LIST OF INSTANCE PRODUCTS ####
@pytest.fixture
def expected_list_products(dipirona_product: Product, vitamina_product: Product, algodao_product: Product) -> list[Product]:
    list = [
        dipirona_product, vitamina_product, algodao_product
    ]
    return list

#### PATH FILES FIXTURES ####
@pytest.fixture
def functional_xml():    
    path_object = Path (__file__).parent
    file_xml = path_object/'data_tests'/'functional_xml_data.xml'
    with open(file_xml, encoding = 'UTF-8') as funcional_xml:
        return funcional_xml.read()

@pytest.fixture
def unstable_xml():
    path_object = Path (__file__).parent
    file_xml = path_object/'data_tests'/'unstable_xml_data.xml'
    with open(file_xml, encoding = 'UTF-8') as unstable_xml:
        return unstable_xml.read()
    
@pytest.fixture
def broken_xml():
    path_object = Path (__file__).parent
    file_xml = path_object/'data_tests'/'broken_xml_data.xml'
    with open(file_xml, encoding = 'UTF-8') as broken_xml:
        return broken_xml.read()        

#####################################################

def test_extract_nfe_data(functional_xml, expected_list_products):                      # <----- TEST FUNCTIONAL XML 

    result = xml_parser.extract_nfe_data(functional_xml)

    assert isinstance(result, list)
    assert len(result) == len(expected_list_products)
    assert result == expected_list_products
    
##################################################### 

def test_extract_nfe_data_unstable(dipirona_product_unstable, unstable_xml, expected_list_products):
    
    expected_list_unstable = expected_list_products.copy()
    expected_list_unstable[0] = dipirona_product_unstable

    result = xml_parser.extract_nfe_data(unstable_xml)
    
    assert isinstance(result, list)
    assert len(result) == len(expected_list_unstable)
    assert result == expected_list_unstable
