import sqlite3
from system.utils import converters, validators, exceptions
from system.models.product import Product
from hashlib import sha256
from datetime import date, datetime
import sys
import logging
from pwinput import pwinput
from typing import Callable, TypeVar
import xml.etree.ElementTree as ET
from system.models.batch import Batch

###############################################################################
print('\n')
print(f'=' * 25, '--- PYTHON AND SQLITE3 VERSION ---', '=' * 25)
print(f'Python Version: {sys.version}')
print(f'Sqlite3 Version: {sqlite3.sqlite_version_info}')
print(f'=' * 50)
###############################################################################

#################### --- ADAPTERS AND CONVERSORS --- ####################
def date_adapter(object_date: date) -> str:
    'receives an object_date in the date adapter for adaptation to the new pattern of sqlite3'
    #print('Adapter Called')
    adapter_format_str = object_date.isoformat()
    return adapter_format_str

def date_conversor(object_bytes: bytes) -> date:
    'receives an object_bytes from database for the converting in a object_date to python'
    #print('Conversor Called')
    convert_object_str = object_bytes.decode()
    adapter_format_date = date.fromisoformat(convert_object_str)
    return adapter_format_date

####### --- DATE OBJECT -> BYTES (STR) OBJECT --- #######
sqlite3.register_adapter(date, date_adapter)
####### --- BYTES (STR) OBJECT -> DATE OBJECT --- #######
sqlite3.register_converter('date', date_conversor)

####### --- CREATING AN DB WITHIN MEMORY --- #######
test_conn = sqlite3.connect(':memory:', detect_types = sqlite3.PARSE_DECLTYPES)
cursor = test_conn.cursor()
object_today = date.today()

###############################################################################
print(f'=' * 25, '--- TYPE INPUT ---', '=' * 25)
print(f'[DEBUG] Type Object Input in Database: {type(object_today)}')
print(f'=' * 50)
print('\n')
print(f'#' * 25, '--- WARNING HERE ---', '#' * 25)
###############################################################################

####### --- CREATING TABLE, INSERTING VALUE AND SELECTING THE OBJECT--- #######
cursor.execute('''
        CREATE TABLE IF NOT EXISTS test (
        id INTEGER PRYMARY KEY,
        date_today DATE NOT NULL
        )
    ''')
cursor.execute('''
        INSERT INTO test (date_today)
        VALUES (?)
    ''',
    (
        object_today,
    ))

cursor.execute('''
        SELECT *
        FROM test
    ''')
return_database = cursor.fetchall()
test_conn.commit()
test_conn.close()

###############################################################################
print(f'#' * 25, '--- WARNING HERE ---', '#' * 25)
print('\n')
print(f'=' * 25, '--- TYPE OUTPUT ---', '=' * 25)
print(f'[DEBUG] Type Object Output from Database: {type(return_database[0][1])}')
print(f'=' * 50)
###############################################################################

######## --- THIS SESSION IS RESPONSABLE FOR ENCRYPTING A TEST PASSWORD --- #########

pin_input = '1234'
pin_bytes = pin_input.encode()
pin_cripto = sha256(pin_bytes).hexdigest()
print('\n')
print('=' * 50)
print(f'Encrypting Password Hash: {pin_cripto}')
print(f'Type for object hash: {type(pin_cripto)}')
print('=' * 50)

######## --- THIS SESSION IS AN EXPERIMENT FOR A NEW FUCTION --- ########

######## --- TYPE HINT EXPERIMENT WITH TYPEVAR --- ########
joker_type = TypeVar('joker_type')

######## --- FUNCTION --- ########
def _collector_generic_input(ask: str, 
    func_conv: Callable[[str], joker_type], 
    func_valid: Callable[[joker_type], bool], 
    func_input: Callable = input):

    while True:
        ask_input = func_input(f'{ask}')
        try:
            conversion_result = func_conv(ask_input)
            validated_result = func_valid(conversion_result)
            if validated_result is True:
                return conversion_result
            else:
                logging.error(f'[ERRO] Os dados inseridos são inválidos. Tente novamente.')
        except exceptions.ConversionError:
            logging.error(f'[ERRO] Os dados inseridos são inválidos. Tente novamente.')

def return_value(value):
    return value

def collect_price() -> float:
    print('=' * 30)
    print('APLICAR PREÇO')
    print('=' * 30)


    converter = return_value
    validator = validators.price_validator

    ask_price = f'[ALERTA] Insira o preço: '
    result = _collector_generic_input(ask_price, converter, validator)
    return result 

######### --- THIS SESSION CONTAINS AN NEW LOGIC FOR THE XML PARSER --- ###########
def extract_nfe_data(xml_content: str) -> str:

    if xml_content is not None:
        if isinstance(xml_content, str):
            root_element: ET.Element = ET.fromstring(xml_content)
            return root_element
    else:
        return None
  
def extract_tags_nfe(root_element: ET.Element) -> list[ET.Element]:
    
    if isinstance(root_element, ET.Element):
        name_space = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
        list_dets = root_element.findall('.//nfe:det', name_space)
        return list_dets
    else:
        None

def manufacture_product(det: ET.Element) -> Product:

    if isinstance(det, ET.Element):
        name_space = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
        
        supplier_code_xml: ET.Element = det.find('.//nfe:cProd', name_space)           
        if supplier_code_xml is not None:
            supplier_code_xml = supplier_code_xml.text

        ean_xml: ET.Element = det.find('.//nfe:cEAN', name_space)
        if ean_xml is not None:
            ean_xml = ean_xml.text
        
        name_xml: ET.Element = det.find('.//nfe:xProd', name_space)
        if name_xml is not None:
            name_xml = name_xml.text
        
        quantity_xml: ET.Element = det.find('.//nfe:qCom', name_space)    
        if quantity_xml is not None:
            quantity_xml = float(quantity_xml.text)
        
        cost_price_xml: ET.Element = det.find('.//nfe:vUnCom', name_space)
        if cost_price_xml is not None:
            cost_price_xml = float(cost_price_xml.text)

    new_product = Product (
        id = None,
        supplier_code = supplier_code_xml,
        ean = ean_xml,
        name = name_xml,
        sale_price = None
    )
    new_batch = Batch (
        batch_id = None,
        physical_batch_id = None,
        product_id = new_product.id,
        quantity = quantity_xml,
        cost_price = cost_price_xml,
        expiration_date = None,
        entry_date = date.today()
    )

    new_product.batch.append(new_batch)
    return new_product

def manager_import(
        xml_content,
        func_data: Callable[[str], ET.Element],
        func_tags: Callable[[ET.Element], list[ET.Element]],
        func_manufacture: Callable[[ET.Element], Product]
    ) -> list[Product]:


        root_element = func_data(xml_content)
        dets = func_tags(root_element)
        list_products = []
        
        for tag in dets:  
            product = func_manufacture(tag)
            list_products.append(product)
        
        return list_products

    