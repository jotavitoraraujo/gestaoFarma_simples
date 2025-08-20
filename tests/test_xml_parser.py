import pytest
from unittest.mock import patch
from pathlib import Path
from sistema.modelos.product import Product
from sistema.modelos.batch import Batch
from datetime import datetime

######################################### DATE (TODAY) INSTANCE ########################################
def today_instance():
    today = datetime.now().strftime('%Y-%m-%d')
    return today

######################################### PRODUCT AND BATCH INSTANCE ###################################
def dipirona_instance():
    product_instance = Product (
        id = 12345,
        ean = 7891020304050,
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
        entry_date = today_instance()
    )
    product_instance.batch.append(batch_instance)
    dipirona_instance = product_instance    
    return dipirona_instance

def vitamina_instance():
    product_instance = Product (
        id = 67890,
        ean = 7895040302010,
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
        entry_date = today_instance()
    )
    product_instance.batch.append(batch_instance)
    vitamina_instance = product_instance
    return vitamina_instance

def algodao_instance():
    product_instance = Product (
        id = 101112,
        ean = None,
        name = 'ALGODÃO HIDRÓFILO 50G',
        sale_price = None
    )
    batch_instance = Batch (
        id = None,
        physical_batch_id = None,
        product_id = product_instance.id,
        quantity = float(30.0),
        cost_price = float(3.20),
        expiration_date = None,
        entry_date = today_instance()
    )
    product_instance.batch.append(batch_instance)
    vitamina_instance = product_instance
    return vitamina_instance

######################################### LIST OF INSTANCE PRODUCTS ####################################
def list_instance_product(instance_1: Product, instance_2: Product, instance_3: Product) -> list[Product]:
    list_instance_product = [
        instance_1, instance_2, instance_3
    ]
    return list_instance_product

######################################### PATH INSTANCE FILES ##########################################
path_object = Path ('.')
file_1 = path_object/'data_tests'/'functional_xml_data.xml'
file_2 = path_object/'data_tests'/'unstable_xml_data.xml'
file_3 = path_object/'data_tests'/'broken_xml_data.xml'

######################################### OPEN AND READ FILES ##########################################
with open(file_1) as xml_data_1, open(file_2) as xml_data_2, open(file_3) as xml_data_3:
    functional_xml_data = xml_data_1.read()
    unstable_xml_data = xml_data_2.read()
    broken_xml_data = xml_data_3.read()

######################################### DECORATOR CONSTRUCT ##########################################
@pytest.mark.parametrize('xml_content, expected_result', [
    (functional_xml_data, 3,),  
])
    
    