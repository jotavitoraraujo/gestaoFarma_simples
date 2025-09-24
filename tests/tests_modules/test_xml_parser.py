import debug_data
import pytest
import xml.etree.ElementTree as ET
from unittest.mock import patch
from pathlib import Path
from system.models.product import Product
from system.models.batch import Batch
from system.modules import xml_parser
from datetime import date


######################################### --- TEST SUIT FROM EXTRACT DATA NFE FUNCTION --- ########################################
### DATE (TODAY) INSTANCE ###
@pytest.fixture
def object_today():
    today = date.today()
    return today

### PRODUCTs AND BATCHs INSTANCEs ###
@pytest.fixture
def dipirona_product(object_today):     # <-- Functional Scenario
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
def dipirona_product_unstable(object_today):     # <-- EAN Empty / Unstable Scenario
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
def vitamina_product(object_today):     # <-- Functional Scenario
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
def algodao_product(object_today):      # <-- Functional Scenario
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
def functional_xml() -> str:    
    path_object = Path (__file__).parent.parent
    file_xml = path_object/'data_tests'/'functional_xml_data.xml'
    with open(file_xml, encoding = 'UTF-8') as funcional_xml:
        return funcional_xml.read()

@pytest.fixture
def unstable_xml() -> str:
    path_object = Path (__file__).parent.parent
    file_xml = path_object/'data_tests'/'unstable_xml_data.xml'
    with open(file_xml, encoding = 'UTF-8') as unstable_xml:
        return unstable_xml.read()
    
@pytest.fixture
def broken_xml() -> str:
    path_object = Path (__file__).parent.parent
    file_xml = path_object/'data_tests'/'broken_xml_data.xml'
    with open(file_xml, encoding = 'UTF-8') as broken_xml:
        return broken_xml.read()        

#####################################################
@pytest.mark.skip(reason = 'THE NEW ARCHTECTURE COVER THIS SUITE')
def test_extract_nfe_data(functional_xml, expected_list_products):                      # <----- TEST FUNCTIONAL XML - STATUS: PASSED

    result = xml_parser.extract_nfe_data(functional_xml)

    assert isinstance(result, list)
    assert len(result) == len(expected_list_products)
    assert result == expected_list_products
    
##################################################### 
@pytest.mark.skip(reason = 'THE NEW ARCHTECTURE COVER THIS SUITE')
def test_extract_nfe_data_unstable(dipirona_product_unstable, unstable_xml, expected_list_products):            # <------ TEST UNSBTABLE XML - STATUS: PASSED
    
    expected_list_unstable = expected_list_products.copy()
    expected_list_unstable[0] = dipirona_product_unstable

    result = xml_parser.extract_nfe_data(unstable_xml)
    
    assert isinstance(result, list)
    assert len(result) == len(expected_list_unstable)
    assert result == expected_list_unstable

#####################################################

def test_extract_nfe_data_broken(broken_xml):           # <------- TEST BROKEN XML - STATUS: PASSED

    result = xml_parser.extract_nfe_data(broken_xml)
    assert result is None
        
# LAST DATE OF IN TESTS THEY WERE PERFORM, 26 AUGUST
###### --- NEW SESSION OF THE XML_PARSER.PY TESTS FOR RECEIVE THE NEW ARCHTECTURE --- ######

@pytest.fixture
def object_det() -> ET.Element:
    det_string = '''
        <det nItem="1">
            <prod>
                <cProd>12345</cProd>
                <cEAN>7891020304050</cEAN>
                <xProd>DIPIRONA 500MG COM 10 COMPRIMIDOS</xProd>
                <qCom>20.0000</qCom>
                <vUnCom>8.50</vUnCom>
            </prod>
        </det>
    '''
    object_det = ET.fromstring(det_string)
    return object_det

def test_manufacture_product(object_det, dipirona_product):

    product = debug_data.manufacture_product(object_det)
    assert product == dipirona_product

