########### --- IMPORTS --- ##########
import pytest
import logging
import sqlite3
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import date, datetime
from decimal import Decimal
from system.models.product import Product
from system.models.fiscal import FiscalProfile, PurchaseTaxDetails
from system.models.batch import Batch
from system.models.user import User


#################### --- ADAPTERS AND CONVERSORS --- ####################
def date_adapter(object_date: date) -> str:
    'inject a object_date in the date translator to sql pattern'
    adapter_format_str = object_date.strftime('%Y-%m-%d')
    return adapter_format_str

##############
def datetime_conversor(object_bytes: bytes) -> datetime:
    'inject a object_str in the datetime translator the of sql pattern to python object'
    convert_object_str = object_bytes.decode()
    adapter_format_date = datetime.strptime(convert_object_str, '%Y-%m-%d %HH:%MM:SS')
    return adapter_format_date

##############
def date_conversor(object_bytes: bytes) -> date:
    'inject a object_str in the date translator the of sql pattern to python object'
    convert_object_str = object_bytes.decode()
    adapter_format_date = date.fromisoformat(convert_object_str)
    return adapter_format_date

########## --- FIXTURES UTILITS --- ###########
@pytest.fixture(scope = 'session')
def db_connection():

    db_connection = None
    try:
        ####### --- DATE OBJECT -> BYTES (STR) OBJECT --- #######
        sqlite3.register_adapter(date, date_adapter)
        ####### --- BYTES (STR) OBJECT -> DATE OBJECT --- #######
        sqlite3.register_converter('date', date_conversor)
        
        db_connection = sqlite3.connect(':memory:', detect_types = sqlite3.PARSE_DECLTYPES)
        logging.warning(f'[ALERT] Test connection with database is on.')
        yield db_connection
    
    except Exception as instance_error:
        logging.error(f'[ERROR] An exception was raised. Details: {instance_error}')
        if db_connection:
            db_connection.rollback()
        raise instance_error

    else:
        if db_connection:
            db_connection.commit()
    
    finally:
        if db_connection:
            db_connection.close()
            logging.warning(f'[ALERT] Test connection with database is off.')

#### --- PATH FILES FIXTURES --- ####
@pytest.fixture(scope = 'module')
def functional_xml():    
    path_object = Path (__file__).parent
    file_xml = path_object/'data_tests'/'functional_xml_data.xml'
    with open(file_xml, encoding = 'UTF-8') as funcional_xml:
        return funcional_xml.read()

##############
@pytest.fixture(scope = 'module')
def unstable_xml():
    path_object = Path (__file__).parent
    file_xml = path_object/'data_tests'/'unstable_xml_data.xml'
    with open(file_xml, encoding = 'UTF-8') as unstable_xml:
        return unstable_xml.read()

##############
@pytest.fixture(scope = 'module')
def missing_tags_xml():
    path_object = Path (__file__).parent
    file_xml = path_object/'data_tests'/'missing_tags_xml_data.xml'
    with open(file_xml, encoding = 'UTF-8') as missing_tags_xml:
        return missing_tags_xml.read()

##############
@pytest.fixture(scope = 'module')
def missing_dets_xml_data():
    path_object = Path (__file__).parent
    file_xml = path_object/'data_tests'/'missing_dets_xml_data.xml'
    with open(file_xml, encoding = 'UTF-8') as missing_dets_xml_data:
        return missing_dets_xml_data.read()

##############
@pytest.fixture(scope = 'module')
def malformed_xml_data():
    path_object = Path (__file__).parent
    file_xml = path_object/'data_tests'/'malformed_xml_data.xml'
    with open(file_xml, encoding = 'UTF-8') as malformed_xml_data:
        return malformed_xml_data.read()

############## 
@pytest.fixture(scope = 'module')
def broken_xml():
    path_object = Path (__file__).parent
    file_xml = path_object/'data_tests'/'broken_xml_data.xml'
    with open(file_xml, encoding = 'UTF-8') as broken_xml:
        return broken_xml.read()

### --- DATE'S INSTANCES --- ###
@pytest.fixture(scope = 'module')
def object_today() -> date:
    today = date.today()
    return today

##############
@pytest.fixture(scope = 'module')
def object_date() -> date:
    object_date_future = date(2035, 8, 31)
    return object_date_future

############################################################
# --- EXCLUSIVE VARIANT FOR THE TEST REGISTER BATCH ALERT --- 
@pytest.fixture(scope = 'module')
def object_date_2() -> date:
    object_date_future = date(2045, 8, 31)
    return object_date_future
############################################################
###### --- OBJECTS DET'S FOR TEST OF THE NEW ARCHTECTURE IN XML_PARSER.PY --- #######

###### --- SCENARIO FUNCTIONAL --- #######
@pytest.fixture(scope = 'module')
def object_det() -> ET.Element:
    det_string = '''
        <NFe xmlns="http://www.portalfiscal.inf.br/nfe">    
            <infNFe>    
                <det nItem="1">
                    <prod>
                        <cProd>12345</cProd>
                        <cEAN>7891020304050</cEAN>
                        <xProd>DIPIRONA 500MG COM 10 COMPRIMIDOS</xProd>
                        <qCom>20.0000</qCom>
                        <vUnCom>8.50</vUnCom>
                    </prod>
                </det>
            </infNFe>
        </NFe>        
    '''
    object_nfe = ET.fromstring(det_string)
    name_space = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
    object_det = object_nfe.find('.//nfe:det', name_space)
    return object_det

###### --- SCENARIO UNSTABLE (<cEAN></cEAN> NOT CONTENT)--- #########
@pytest.fixture(scope = 'module')
def object_det_unstable() -> ET.Element:
    det_string = '''
        <NFe xmlns="http://www.portalfiscal.inf.br/nfe">    
            <infNFe>    
                <det nItem="1">
                    <prod>
                        <cProd>12345</cProd>
                        <cEAN></cEAN>
                        <xProd>DIPIRONA 500MG COM 10 COMPRIMIDOS</xProd>
                        <qCom>20.0000</qCom>
                        <vUnCom>8.50</vUnCom>
                    </prod>
                </det>
            </infNFe>
        </NFe>        
    '''
    object_nfe = ET.fromstring(det_string)
    name_space = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
    object_det = object_nfe.find('.//nfe:det', name_space)
    return object_det

###### --- SCENARIO WHERE DATA IS MISSING (<xProd></xProd> TAG MISSING)--- #######
@pytest.fixture(scope = 'module')
def object_det_missing() -> ET.Element:
    det_string = '''
        <NFe xmlns="http://www.portalfiscal.inf.br/nfe">    
            <infNFe>    
                <det nItem="1">
                    <prod>
                        <cProd>12345</cProd>
                        <cEAN>7891020304050</cEAN>
                        <qCom>20.0000</qCom>
                        <vUnCom>8.50</vUnCom>
                    </prod>
                </det>
            </infNFe>
        </NFe>        
    '''
    object_nfe = ET.fromstring(det_string)
    name_space = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
    object_det = object_nfe.find('.//nfe:det', name_space)
    return object_det

####### --- SCENARIO OF THE DATA MALFORMED (<qCom></qCom> CONTENT IS AS TEXT NOT FLOAT) --- #######
@pytest.fixture(scope = 'module')
def object_det_malformed() -> ET.Element:
    det_string = '''
        <NFe xmlns="http://www.portalfiscal.inf.br/nfe">    
            <infNFe>    
                <det nItem="1">
                    <prod>
                        <cProd>12345</cProd>
                        <cEAN>7891020304050</cEAN>
                        <xProd>DIPIRONA 500MG COM 10 COMPRIMIDOS</xProd>
                        <qCom>TWENTY UNITS</qCom>
                        <vUnCom>8.50</vUnCom>
                    </prod>
                </det>
            </infNFe>
        </NFe>        
    '''
    object_nfe = ET.fromstring(det_string)
    name_space = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
    object_det = object_nfe.find('.//nfe:det', name_space)
    return object_det

##############
@pytest.fixture(scope = 'module')
def root_element(functional_xml) -> ET.Element:
        root_element: ET.Element = ET.fromstring(functional_xml)
        return root_element

##############
@pytest.fixture(scope = 'module')
def extracts_dets(root_element: ET.Element) -> list[ET.Element]:
        name_space = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
        list_dets: list[ET.Element] = root_element.findall('.//nfe:det', name_space)
        return list_dets

##############
@pytest.fixture(scope = 'module')
def dict_tags(object_det: ET.Element):
        
    name_space: dict = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
    supplier_code_xml: ET.Element = object_det.find('.//nfe:cProd', name_space)           
    ean_xml: ET.Element = object_det.find('.//nfe:cEAN', name_space)
    name_xml: ET.Element = object_det.find('.//nfe:xProd', name_space)
    quantity_xml: ET.Element = object_det.find('.//nfe:qCom', name_space)    
    cost_price_xml: ET.Element = object_det.find('.//nfe:vUnCom', name_space)
    
    dict_tags: dict = {
        'cProd': supplier_code_xml,
        'cEAN': ean_xml,
        'xProd': name_xml, 
        'qCom': quantity_xml, 
        'vUnCom': cost_price_xml
    }
    
    return dict_tags

##############
@pytest.fixture(scope = 'module')
def tuple_product(dict_tags):

    ean = None
    supplier_code: str = dict_tags['cProd'].text
    
    if dict_tags['cEAN'] is not None:
        ean = dict_tags['cEAN'].text        
    
    name: str = dict_tags['xProd'].text
    quantity: float = float(dict_tags['qCom'].text)
    cost_price: float = float(dict_tags['vUnCom'].text)
    tuple_product: tuple = (supplier_code, ean, name, quantity, cost_price,)
    return tuple_product

####################################################################
### PRODUCTs, FISCAL PROFILE, PURCHASE TAX DETAILS AND BATCH, INSTANCES ###
@pytest.fixture(scope = 'module')
def dipirona_product(object_today, object_date) -> Product:
    product_instance = Product (
        id = None,
        supplier_code = '12345',
        ean = '7891020304050',
        name = 'DIPIRONA 500MG COM 10 COMPRIMIDOS',
        sale_price = None        
    )
    batch_instance = Batch (
        id = 1,
        physical_id = 'ABC123HI',
        product_id = product_instance.id,
        quantity = float(20.0),
        unit_cost_amount = float(8.50),
        use_by_date = object_date,
        received_date = object_today
    )
    product_instance.batch.append(batch_instance)
    dipirona_instance = product_instance    
    return dipirona_instance
    
############################################################
# --- EXCLUSIVE VARIANT FOR THE TEST REGISTER BATCH ALERT ---
@pytest.fixture(scope = 'module')
def dipirona_product_2(object_today, object_date_2) -> Product:
    product_instance = Product (
        id = 2,
        supplier_code = '12345',
        ean = '7891020304051',
        name = 'DIPIRONA 500MG COM 11 COMPRIMIDOS',
        sale_price = None        
    )
    batch_instance = Batch (
        id = 2,
        physical_id = 'ABC123HJ',
        product_id = product_instance.id,
        quantity = float(20.0),
        unit_cost_amount = float(8.50),
        use_by_date = object_date_2,
        received_date = object_today
    )
    product_instance.batch.append(batch_instance)
    dipirona_instance = product_instance    
    return dipirona_instance

############################################################
# --- EXCLUSIVE VARIANT FOR TESTING OF THE NEW FUNCTION MANUFACTURE PRODUCT --- #
@pytest.fixture(scope = 'module')
def dipirona_product_manufacture() -> Product:
    product_instance = Product (
        id = None,
        supplier_code = '12345',
        ean = '7891020304050',
        name = 'DIPIRONA 500MG COM 10 COMPRIMIDOS',
        sale_price = None        
    )
    batch_instance = Batch (
        id = None,
        physical_id = None,
        product_id = product_instance.id,
        quantity = float(20.0),
        unit_cost_amount = float(8.50),
        use_by_date = None,
        received_date = date.today()
    )
    product_instance.batch.append(batch_instance)
    dipirona_instance = product_instance    
    return dipirona_instance

#############################################################
@pytest.fixture(scope = 'module')
def dipirona_product_manufacture_unstable() -> Product:
    product_instance = Product (
        id = None,
        supplier_code = '12345',
        ean = None,
        name = 'DIPIRONA 500MG COM 10 COMPRIMIDOS',
        sale_price = None        
    )
    batch_instance = Batch (
        id = None,
        physical_id = None,
        product_id = product_instance.id,
        quantity = float(20.0),
        unit_cost_amount = float(8.50),
        use_by_date = None,
        received_date = date.today()
    )
    product_instance.batch.append(batch_instance)
    dipirona_instance = product_instance    
    return dipirona_instance

#############################################################
@pytest.fixture(scope = 'module')
def dipirona_product_manufacture_missing_tags() -> Product:
    product_instance = Product (
        id = None,
        supplier_code = '12345',
        ean = '7891020304050',
        name = 'DIPIRONA 500MG COM 10 COMPRIMIDOS',
        sale_price = None        
    )
    batch_instance = Batch (
        id = None,
        physical_id = None,
        product_id = product_instance.id,
        quantity = float(20.0),
        unit_cost_amount = float(8.50),
        use_by_date = None,
        received_date = date.today()
    )
    product_instance.batch.append(batch_instance)
    dipirona_instance = product_instance    
    return dipirona_instance

#############################################################
@pytest.fixture(scope = 'module')
def vitamina_product(object_today, object_date) -> Product:
    product_instance = Product (
        id = 2,
        supplier_code = '67890',
        ean = '7895040302010',
        name = 'VITAMINA C EFERVESCENTE',
        sale_price = None
    )
    batch_instance = Batch (
        id = None,
        physical_id = 'ABC123DE',
        product_id = product_instance.id,
        quantity = float(15.0),
        unit_cost_amount = float(12.75),
        use_by_date = object_date,
        received_date = object_today
    )
    product_instance.batch.append(batch_instance)
    vitamina_instance = product_instance
    return vitamina_instance

#############################################################
@pytest.fixture(scope = 'module')
def vitamina_product_manufacture() -> Product:
    product_instance = Product (
        id = None,
        supplier_code = '67890',
        ean = '7895040302010',
        name = 'VITAMINA C EFERVESCENTE',
        sale_price = None
    )
    batch_instance = Batch (
        id = None,
        physical_id = None,
        product_id = product_instance.id,
        quantity = float(15.0),
        unit_cost_amount = float(12.75),
        use_by_date = None,
        received_date = date.today()
    )
    product_instance.batch.append(batch_instance)
    vitamina_instance = product_instance
    return vitamina_instance

#############################################################
@pytest.fixture(scope = 'module')
def vitamina_product_manufacture_unstable() -> Product:
    product_instance = Product (
        id = None,
        supplier_code = '67890',
        ean = '7895040302010',
        name = 'VITAMINA C EFERVESCENTE',
        sale_price = None
    )
    batch_instance = Batch (
        id = None,
        physical_id = None,
        product_id = product_instance.id,
        quantity = float(15.0),
        unit_cost_amount = float(12.75),
        use_by_date = None,
        received_date = date.today()
    )
    product_instance.batch.append(batch_instance)
    vitamina_instance = product_instance
    return vitamina_instance

#############################################################
@pytest.fixture(scope = 'module')
def vitamina_product_manufacture_missing_tags() -> Product:
    product_instance = Product (
        id = None,
        supplier_code = '67890',
        ean = '7895040302010',
        name = None,
        sale_price = None
    )
    batch_instance = Batch (
        id = None,
        physical_id = None,
        product_id = product_instance.id,
        quantity = float(15.0),
        unit_cost_amount = float(12.75),
        use_by_date = None,
        received_date = date.today()
    )
    product_instance.batch.append(batch_instance)
    vitamina_instance = product_instance
    return vitamina_instance

#############################################################
@pytest.fixture(scope = 'module')
def algodao_product(object_today, object_date) -> Product:
    product_instance = Product (
        id = 3,
        supplier_code = '101112',
        ean = '7895040302015',
        name = 'ALGODÃO HIDRÓFILO 50G',
        sale_price = None
    )
    batch_instance = Batch (
        id = None,
        physical_id = 'ABC123FG',
        product_id = product_instance.id,
        quantity = float(30.0),
        unit_cost_amount = float(3.20),
        use_by_date = object_date,
        received_date = object_today
    )
    product_instance.batch.append(batch_instance)
    algodao_instance = product_instance
    return algodao_instance

#############################################################
@pytest.fixture(scope = 'module')
def algodao_product_manufacture() -> Product:
    product_instance = Product (
        id = None,
        supplier_code = '101112',
        ean = '7895040302015',
        name = 'ALGODÃO HIDRÓFILO 50G',
        sale_price = None
    )
    batch_instance = Batch (
        id = None,
        physical_id = None,
        product_id = product_instance.id,
        quantity = float(30.0),
        unit_cost_amount = float(3.20),
        use_by_date = None,
        received_date = date.today()
    )
    product_instance.batch.append(batch_instance)
    algodao_instance = product_instance
    return algodao_instance

#############################################################
@pytest.fixture(scope = 'module')
def algodao_product_manufacture_unstable() -> Product:
    product_instance = Product (
        id = None,
        supplier_code = '101112',
        ean = None,
        name = 'ALGODÃO HIDRÓFILO 50G',
        sale_price = None
    )
    batch_instance = Batch (
        id = None,
        physical_id = None,
        product_id = product_instance.id,
        quantity = float(30.0),
        unit_cost_amount = float(3.20),
        use_by_date = None,
        received_date = date.today()
    )
    product_instance.batch.append(batch_instance)
    algodao_instance = product_instance
    return algodao_instance

#############################################################
@pytest.fixture(scope = 'module')
def algodao_product_manufacture_missing_tags() -> Product:
    product_instance = Product (
        id = None,
        supplier_code = None,
        ean = None,
        name = 'ALGODÃO HIDRÓFILO 50G',
        sale_price = None
    )
    batch_instance = Batch (
        id = None,
        physical_id = None,
        product_id = product_instance.id,
        quantity = None,
        unit_cost_amount = None,
        use_by_date = None,
        received_date = date.today()
    )
    product_instance.batch.append(batch_instance)
    algodao_instance = product_instance
    return algodao_instance

####### --- THIS FIXTURES WERE CREATED FOR NEW UPSERT LOGIC IN THE TEST_SAVE_PRODUCTS --- #######
@pytest.fixture(scope = 'module')
def product_A(object_date: date) -> Product:

    product_A = Product (
        id = None,
        supplier_code = '12345',
        ean = 'TESTSAVEPRODUCTS123',
        name = 'PRODUCT A',
        sale_price = None
    )

    batch_A = Batch (
        id = None,
        physical_id = 'ABC123D',
        product_id = 1,
        quantity = 1,
        unit_cost_amount = float(10.99),
        use_by_date = object_date,
        received_date = date.today()
    )

    product_A.batch.append(batch_A)
    return product_A

#############
@pytest.fixture(scope = 'module')
def product_B(object_date: date) -> Product:

    product_B = Product (
        id = None,
        supplier_code = '123456',
        ean = 'TESTSAVEPRODUCTS123',
        name = 'PRODUCT B',
        sale_price = None
    )

    batch_B = Batch (
        id = None,
        physical_id = 'ABC123D',
        product_id = 2,
        quantity = 1,
        unit_cost_amount = float(10.99),
        use_by_date = object_date,
        received_date = date.today()
    )

    product_B.batch.append(batch_B)
    return product_B

#############
@pytest.fixture(scope = 'module')
def product_A_copy_diff(object_date: date) -> Product:

    product_A = Product (
        id = None,
        supplier_code = '12345',
        ean = 'TESTSAVEPRODUCTS123',
        name = 'PRODUCT A COPY',
        sale_price = None
    )

    batch_A = Batch (
        id = None,
        physical_id = 'ABC123E',
        product_id = 3,
        quantity = 2,
        unit_cost_amount = float(11.99),
        use_by_date = object_date,
        received_date = date.today()
    )

    product_A.batch.append(batch_A)
    return product_A

################
# --- SESSION TO UNIQUE INSTANCES FROM FISCAL PROFILES AND PURCHASE TAX DETAILS
@pytest.fixture(scope = 'module')
def fiscal_profile() -> FiscalProfile:
    fiscal_profile = FiscalProfile (
        id = 1,
        ncm = '1234',
        cest = '1234',
        origin_code = '1234' 
    )
    return fiscal_profile
##############
@pytest.fixture(scope = 'module')
def purchase_tax_details() -> PurchaseTaxDetails:
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
    return purchase_tax_details

#############################################################
### LIST OF INSTANCE PRODUCTS ####
@pytest.fixture(scope = 'module')
def expected_list_products(dipirona_product: Product, vitamina_product: Product, algodao_product: Product) -> list[Product]:
    list = [
        dipirona_product, vitamina_product, algodao_product
    ]
    return list

############################################################
# --- EXCLUSIVE VARIANT FOR THE TEST REGISTER BATCH ALERT ---
@pytest.fixture(scope = 'module')
def expected_list_products_2(dipirona_product: Product, dipirona_product_2: Product, vitamina_product: Product, algodao_product: Product) -> list[Product]:
    list = [
        dipirona_product, dipirona_product_2, vitamina_product, algodao_product
    ]
    return list

############################################################
# --- EXCLUSIVE VARIANTS FOR THE TEST EXTRACT DETS ---
@pytest.fixture(scope = 'module')
def expected_list_products_manufacture(dipirona_product_manufacture: Product, vitamina_product_manufacture: Product, algodao_product_manufacture: Product) -> list[Product]:
    list = [
        dipirona_product_manufacture, vitamina_product_manufacture, algodao_product_manufacture
    ]
    return list

################
@pytest.fixture(scope = 'module')
def expected_list_products_manufacture_unstable(dipirona_product_manufacture_unstable: Product, vitamina_product_manufacture_unstable: Product, algodao_product_manufacture_unstable: Product) -> list[Product]:
    list = [
        dipirona_product_manufacture_unstable, vitamina_product_manufacture_unstable, algodao_product_manufacture_unstable
    ]
    return list
################
@pytest.fixture(scope = 'module')
def expected_list_products_manufacture_missing_tags(dipirona_product_manufacture_missing_tags: Product) -> list[Product]:
    list = [
        dipirona_product_manufacture_missing_tags
    ]
    return list

#############
# --- EXCLUSIVE VARIANTS HAS BEEN CREATED FOR THE TEST OF THE FUNCTION SAVE_ PRODUCTS --- #
@pytest.fixture(scope = 'module')
def inicial_products_list(product_A: Product, product_B: Product) -> list[Product]:

    list = [
        product_A, product_B
    ]

    return list

#############
@pytest.fixture(scope = 'module')
def upsert_product_list(product_A_copy_diff: Product) -> list[Product]:

    list = [
        product_A_copy_diff
    ]

    return list

############################################################
### INSTANCE USER ###
@pytest.fixture(scope = 'module')
def user_test() -> User:
    user = User (
        user_id = 1,
        user_name = 'JoaoVitor',
        user_pin = '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4'
    )
    return user

### THIS SESSION I AM TRYING CREATE AN CLASS CALLED 'ALERT' AS FIXTURE, FOR BE WITHIN TEST FUNCTION REGISTER_BATCH_ALERT
class Alert:
    def __init__(self,
        alert_id: int,
        order_id: int,  
        user: User, 
        product: Product,
        batch_id_sold: Batch,
        batch_id_correct: Batch, 
        today: str, 
        neglect: int
        ):
        
        self.alert_id = alert_id
        self.order_id = order_id
        self.user_id = user
        self.product_id = product
        self.batch_id_sold = batch_id_sold
        self.batch_id_correct = batch_id_correct
        self.today = today
        self.neglect = neglect

    def __repr__(self):
        'technical representation of type Alert'

        return f'''
        --- Data Alert ---
        1. Alert ID: {self.alert_id}
        2. Order ID: {self.order_id}
        3. User ID: {self.user_id}
        4. Product ID: {self.product_id}
        5. Batch ID Sold: {self.batch_id_sold}
        6. Batch ID Correct: {self.batch_id_correct}
        7. Date: {self.today}
        8. Neglect: {self.neglect}
    '''

    def __eq__(self, other):
        'dunder method for comparassion between types Alert'

        if isinstance(other, type(self)):
            return (
                other.order_id == self.order_id
                and other.product_id == self.product_id
                and other.user_id == self.user_id
                and other.batch_id_sold == self.batch_id_sold
                and other.batch_id_correct == self.batch_id_correct
            )
        else:
            return False
        
### INSTANCE ALERT ###
@pytest.fixture(scope = 'function')
def alert(dipirona_product: Product, dipirona_product_2: Product, user_test: User):
    
    object_datetime_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    alert_type = Alert (
        alert_id = 2,
        order_id = 1,
        user = user_test.user_id,
        product = int(dipirona_product_2.id),        
        batch_id_sold = dipirona_product_2.batch[0].id,
        batch_id_correct = dipirona_product.batch[0].id,
        today = object_datetime_str,
        neglect = 1
    )
    return alert_type

### --- HASH FOR TESTING IN THE FUNCTION -> PASSWORD FOR HASH CONVERSOR --- ###
@pytest.fixture(scope = 'function')
def hash_list_test() -> list[str]:

    hash_list = [
        '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4', # HASH OF: 1234
        'f296867839c8befafed32b55a7c11ab4ad14387d2434b970a55237d537bc9353', # HASH OF: 1020
        '4ee813262a515c9aace96ef879e65667855c4ec290ca31f5bd49eb69a5e05ae7', # HASH OF: 3040
        '8a5edab282632443219e051e4ade2d1d5bbc671c781051bf1437897cbdfea0f1', # HASH OF: /
        '7ad8dbe5dbed0dcda5e2fa713de5ddb5b6db23d8b7f4fc0ed2650b5b071107c7'  # HASH OF: letters
    ]
    return hash_list