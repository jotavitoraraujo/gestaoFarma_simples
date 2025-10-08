###### --- IMPORTS --- ######
from system.modules.xml_parser import XMLParser
from system.utils.exceptions import ConversionError
import xml.etree.ElementTree as ET

######################################################################################
##### --- TESTING FINAL PART OF DATA FLOW TO PARSING A XML, THE MANAGER. WITHIN SCOPE HAPPY PATH --- #####
def test_manager_import(functional_xml_real, rich_products_list):
    'the result it must be an list of products, where each product be perfectly instantiated'

    parser = XMLParser(functional_xml_real)
    parser.execute_process()
    result = parser.get_complete_products()
    
    assert len(result) == 3
    assert len(parser.get_quarantine_products()) == 0
    assert len(parser.get_errors()) == 0
    assert result == rich_products_list

######################################################################################
###### --- SESSION OF THE XML_PARSER.PY TESTS TO THE UNSTABLE PATH --- ######
def test_manager_import_unstable(unstable_xml_real, rich_products_list_EAN_None):
    '''the result it must be a list of products completes containing 2 items and a list of incomplete products containing 1 item,
    the knot number 3 (most specifically the content in <cEAN></cEAN>) it is empty'''
    
    parser = XMLParser(unstable_xml_real)
    parser.execute_process()
    result = parser.get_complete_products()
    result_2 = parser.get_quarantine_products()
    list_result = [result[0], result[1], result_2[0]]

    assert len(result) == 2
    assert len(result_2) == 1
    assert len(parser.get_errors()) == 0
    assert list_result == rich_products_list_EAN_None

######################################################################################
###### --- SESSION OF THE XML_PARSER.PY TESTS TO THE MISSING TAGS PATH --- ######
def test_manager_import_missing_tags(missing_tags_xml_real, rich_products_list_only_one):
    'the result it must be an list with only a product where is instantiated perfectly, because the remaining data is completly absent'
    parser = XMLParser(missing_tags_xml_real)
    parser.execute_process()
    result = parser.get_complete_products()
    errors = parser.get_errors()

    assert len(result) == 1
    assert parser.get_quarantine_products() == []
    assert len(errors) == 2
    assert result == rich_products_list_only_one

######################################################################################
###### --- SESSION OF THE XML_PARSER.PY TESTS TO THE MISSING DETS PATH --- ######
def test_manager_import_missing_all_dets(missing_dets_xml_real):
    'the result it must be an empty list, because data in knot det dont exist'
    
    parser = XMLParser(missing_dets_xml_real)
    parser.execute_process()
    result = parser.get_complete_products()
    result_2 = parser.get_quarantine_products()
    errors = parser.get_errors()

    assert result == []
    assert result_2 == []
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
    result = parser.get_complete_products()
    result_2 = parser.get_quarantine_products()
    errors = parser.get_errors()

    assert len(result) == 2
    assert len(result_2) == 0
    assert len(errors) == 1
    assert isinstance(errors[0], ConversionError) 

######################################################################################
###### --- SESSION OF THE XML_PARSER.PY TESTS TO THE BROKEN PATH --- ######
def test_manager_import_broken(broken_xml):
    'the result it must raised and captured an instance of ET.ParserError in case of the tags broken'

    parser = XMLParser(broken_xml)
    parser.execute_process()
    result = parser.get_complete_products()
    result_2 = parser.get_quarantine_products()
    errors = parser.get_errors()

    assert len(result) == 0
    assert len(result_2) == 0
    assert len(errors) == 1
    assert isinstance(errors[0], ET.ParseError)

######################################################################################
# ---> THE CONCLUSION THIS IT SUITE OF UNIT/INTEGRATION TESTS FOR THE MODULE XML_PARSER.PY AFTER A NEW ARCHTECTURE IS DEFINED IT HAPPENED AT SEPT 28, 2025.