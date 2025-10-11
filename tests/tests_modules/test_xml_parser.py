###### --- IMPORTS --- ######
from system.modules.xml_parser import XMLParser
from system.utils.exceptions import ConversionError
from system.models.product import Product
import xml.etree.ElementTree as ET

######################################################################################
##### --- TESTING FINAL PART OF DATA FLOW TO PARSING A XML, THE MANAGER. WITHIN SCOPE HAPPY PATH --- #####
def test_manager_import(functional_xml_real, rich_products_list):
    'the result it must be an list of products, where each product be perfectly instantiated'

    parser = XMLParser(functional_xml_real)
    parser.execute_process()
    result = parser.get_products()
    
    assert len(result) == 3
    assert len(parser.get_errors()) == 0
    assert result == rich_products_list

######################################################################################
###### --- SESSION OF THE XML_PARSER.PY TESTS TO THE UNSTABLE PATH --- ######
def test_manager_import_unstable(unstable_xml_real, rich_products_list_EAN_None):
    '''the result it must be a list of products containing 3 items, but index 2 it has the attribute .ean absent
    det number 3 (most specifically, the content in <cEAN></cEAN>) it is empty'''
    
    parser = XMLParser(unstable_xml_real)
    parser.execute_process()
    result = parser.get_products()
    list_result = [result[0], result[1], result[2]]

    assert len(result) == 3
    assert len(parser.get_errors()) == 0
    assert list_result == rich_products_list_EAN_None

######################################################################################
###### --- SESSION OF THE XML_PARSER.PY TESTS TO THE MISSING TAGS PATH --- ######
def test_manager_import_missing_tags(missing_tags_xml_real):
    'the result it must be an list complete where is instantiated perfectly, same with mandatory data absent'
    parser = XMLParser(missing_tags_xml_real)
    parser.execute_process()
    result: tuple[Product] = parser.get_products()
    errors = parser.get_errors()

    assert len(result) == 3
    assert len(errors) == 0
    assert result[1].name == None
    assert result[2].name == None

######################################################################################
###### --- SESSION OF THE XML_PARSER.PY TESTS TO THE MISSING DETS PATH --- ######
def test_manager_import_missing_all_dets(missing_dets_xml_real):
    'the result it must be an empty list, because data in knot det dont exist'
    
    parser = XMLParser(missing_dets_xml_real)
    parser.execute_process()
    result = parser.get_products()
    errors = parser.get_errors()

    assert result == []
    assert errors == []

######################################################################################
###### --- SESSION OF THE XML_PARSER.PY TESTS TO THE BROKEN PATH --- ######
def test_manager_import_malformed_xml(malformed_xml_real):
    '''
    the result it must raised and captured an instance of ConversionError 
    in case the tags contain data with the correct intent but in a format unsuitable for conversion
    example: DET: NITEM = 1  
    WRONG: <qCom>TWO UNITS</qCom> -> DONT ACCEPT THE USE OF LETTERS
    CORRECT: <qCom>2.000</qCom> -> A FLOAT TYPE NUMBER
    '''
    parser = XMLParser(malformed_xml_real)
    parser.execute_process()
    result = parser.get_products()
    errors = parser.get_errors()

    assert len(result) == 2
    assert len(errors) == 1
    assert isinstance(errors[0], ConversionError) 

######################################################################################
###### --- SESSION OF THE XML_PARSER.PY TESTS TO THE BROKEN PATH --- ######
def test_manager_import_broken(broken_xml):
    'the result it must raised and captured an instance of ET.ParserError in case of the tags broken'

    parser = XMLParser(broken_xml)
    parser.execute_process()
    result = parser.get_products()
    errors = parser.get_errors()

    assert len(result) == 0
    assert len(errors) == 1
    assert isinstance(errors[0], ET.ParseError)

######################################################################################
# ---> THE CONCLUSION THIS IT SUITE OF UNIT/INTEGRATION TESTS FOR THE MODULE XML_PARSER.PY AFTER A NEW ARCHTECTURE IS DEFINED IT HAPPENED AT SEPT 28, 2025.