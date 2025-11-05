import sqlite3
from system.utils import validators, exceptions
from system.models.product import Product
from hashlib import sha256
from datetime import date
import sys
import logging
from typing import Callable, TypeVar
import xml.etree.ElementTree as ET
from system.models.batch import Batch
from system.utils.exceptions import MissingTagError, ConversionError

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
######## --- IMPORTS --- ########
from system.models.product import Product
from system.models.batch import Batch
from system.utils.exceptions import MissingTagError, ConversionError
from datetime import date
from typing import Callable
import xml.etree.ElementTree as ET
import logging

######### --- THIS SESSION CONTAINS AN NEW LOGIC FOR THE XML PARSER --- ###########
def extract_xml_data(xml_content: str) -> ET.Element:
    'extract data of the xml and transform he at a object ET as root for the use'

    if xml_content is not None:
        if isinstance(xml_content, str):
            root_element: ET.Element = ET.fromstring(xml_content)
            return root_element
    else:
        return None
  
def extract_dets(root_element: ET.Element) -> list[ET.Element]:
    '''
    create a list of the ET objects from argument this function and returns an list of the knots for the tratament
    use with a for loop provide the control variable a single knot det to no broken the data flow in next functions
    '''
    
    if isinstance(root_element, ET.Element):
        name_space = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
        list_dets: list[ET.Element] = root_element.findall('.//nfe:det', name_space)
        return list_dets
    else:
        None

def find_tags(det: ET.Element) -> dict:
    'find and pull of this knot det all tags that will make use to Product instance and returns an dictionary'
    
    if isinstance(det, ET.Element):
        
        name_space: dict = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
        supplier_code_xml: ET.Element = det.find('.//nfe:cProd', name_space)           
        ean_xml: ET.Element = det.find('.//nfe:cEAN', name_space)
        name_xml: ET.Element = det.find('.//nfe:xProd', name_space)
        quantity_xml: ET.Element = det.find('.//nfe:qCom', name_space)    
        cost_price_xml: ET.Element = det.find('.//nfe:vUnCom', name_space)
     
        dict_tags: dict = {
            'cProd': supplier_code_xml,
            'cEAN': ean_xml,
            'xProd': name_xml, 
            'qCom': quantity_xml, 
            'vUnCom': cost_price_xml
        }
    return dict_tags

def verify_integrity_tags(dict_tags: dict, det: ET.Element) -> None:
    '''
    verify if some tag from dict received of argument is equal a none and capture a nItem of the knot det to use within the except.
    this function or returns None or returns a raising the error MissingTagError.
    '''
    
    if not isinstance(dict_tags, dict):
        raise ValueError

    tags_mandatory: set = {'cProd', 'xProd', 'qCom', 'vUnCom'}
    tags_missing: list = []
    for key_tag, element in dict_tags.items():
        if element is None and key_tag in tags_mandatory:
            tags_missing.append(key_tag)

    if tags_missing:
        det_nItem = det.attrib.get('nItem')
        raise MissingTagError('[ERRO] An mandatory tag is absent. Verify the content', tags_missing, det_nItem)

def convertion_tags(tags: dict) -> tuple:
    'convert the tags in objetcs type string/float and manage a lift as error inside of except'
    
    ean = None
    try:
        supplier_code: str = tags['cProd'].text
        
        if tags['cEAN'] is not None:
            ean = tags['cEAN'].text        
        
        name: str = tags['xProd'].text
        quantity: float = float(tags['qCom'].text)
        cost_price: float = float(tags['vUnCom'].text)
        product_data: tuple = (supplier_code, ean, name, quantity, cost_price,)
        return product_data
    
    except (ValueError) as conversion_error:
        raise ConversionError('[ERRO] This conversion is fail. Verify of types of the values in your keys within dicionary', tags, ean) from conversion_error

def manufacture_product(product_data: tuple) -> Product:
    'an simple function what instance a product'
    
    if len(product_data) == 5:
        new_product = Product (
            id = None,
            supplier_code = product_data[0],
            ean = product_data[1],
            name = product_data[2],
            sale_price = None
        )
        new_batch = Batch (
            id = None,
            physical_id = None,
            product_id = new_product.id,
            quantity = product_data[3],
            unit_cost_amount = product_data[4],
            use_by_date = None,
            received_date = date.today()
        )

        new_product.batch.append(new_batch)
    return new_product

def filter_products(product: Product) -> tuple:
    '''
    filter the products sent by the manufacture function at perfect product or  in case of .ean attribute absent, product imperfect.
    then insert hes at your adequate list and returns an tuple which contains the two lists.
    '''
    list_perfect_products: list = []
    list_absent_product_ean: list  = []
    
    if product.ean is not None:
        list_perfect_products.append(product)
    else:
        list_absent_product_ean.append(product)

    return (list_perfect_products, list_absent_product_ean,)

def manager_import(
        xml_content,
        func_extractor_data: Callable[[str], ET.Element],
        func_extractor_det: Callable[[ET.Element], list[ET.Element]],
        func_find_tags: Callable[[ET.Element], dict],
        func_verify_tags: Callable[[dict], str],
        func_convertion_tags: Callable[[dict], tuple],
        func_manufacture: Callable[[tuple], Product]
    ) -> tuple:

    '''
    this orchestrator manage all scenario of the parsing in xml since initiation until conclusion.
    giving you an list from the products instantiated by manufacture_product function in the end of the data flow here
    i kwon that are many args but is required that you respect of assingnature of the function
    '''
    try:        
        root_element: ET.Element = func_extractor_data(xml_content)
        list_dets: list[ET.Element] = func_extractor_det(root_element)
        list_products_complets = []
        list_products_ean_absent = []

        # THIS TWO INSTANCES OF THE LISTS HAVE A UNIQUE FINALLITY
        # STORE IN THE LIST_PRODUCTS_COMPLETS THE PRODUCTS INSTANTIATED CORRECTLY
        # AND STORE IN THE LIST_PRODUCTS_EAN_ABSENT THE PRODUCTS INSTANTIATED WITH THE ATTRIBUTE .ean AS NONE
        # LIST_PRODUCTS_COMPLETS -> GO TO THE TABLE: products, WITHIN OF DATABASE
        # LIST_PRODUCTS_EAN_ABSENT -> GO TO THE TABLE: quarantined_products, WITHIN OF DATABASE
        #         
        if list_dets is not None:
            for det in list_dets:
                nItem = det.attrib.get('nItem')
                
                try:
                    tags: dict = func_find_tags(det)
                    func_verify_tags(tags, det)
                    clean_data: tuple = func_convertion_tags(tags)
                    final_product: Product = func_manufacture(clean_data)

                    if final_product.ean is not None:
                        list_products_complets.append(final_product)
                    else:
                        list_products_ean_absent.append(final_product)
                
                except (MissingTagError, ConversionError) as error:
                    logging.warning(f'[ALERTA] O Item DET Nº: {nItem} da NF-e foi ignorado. Motivo: {error}')
                    continue
            return (list_products_complets, list_products_ean_absent,)
        
        else:
            logging.warning(f'[ERRO] Conteúdo do XML vazio. Verifique o arquivo e tente novamente.')
    
    except ET.ParseError as error:
        logging.warning(
            f'''
            [ERRO] A Nota Fiscal inserida está sintaximente mal formada e não importará nenhum item. 
            Verifique a integridade das tags dentro do arquivo XML e tente novamente ou insira outra NF-e.
            Dados do Erro: {error}
            '''
            )
        return ([], [])