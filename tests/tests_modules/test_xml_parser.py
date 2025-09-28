###### --- IMPORTS --- ######
from system.modules.xml_parser import extract_xml_data
from system.modules.xml_parser import extract_dets
from system.modules.xml_parser import find_tags
from system.modules.xml_parser import verify_integrity_tags
from system.modules.xml_parser import convertion_tags
from system.modules.xml_parser import manufacture_product
from system.modules.xml_parser import manager_import
import xml.etree.ElementTree as ET
import pytest

######################################################################################
###### --- SESSION OF THE XML_PARSER.PY UNIT TESTS ISOLATEDS WITH FUNCTIONAL CONTENT OF THE XML --- ######
def test_extract_xml_data(functional_xml):
    result = extract_xml_data(functional_xml)
    assert isinstance(result, ET.Element)

######## --- EXTRACT LIST OF DETS FOR THE TEST --- ########
def test_extract_dets(root_element):
    result = extract_dets(root_element)
    assert isinstance(result, list) and len(result) >= 1

####### --- EXTRACT TAGS FROM A UNIQUE KNOT DET --- ########
def test_find_tags(object_det):
    result = find_tags(object_det)
    assert isinstance(result, dict)

####### --- VERIFY INTEGRITY OF THE TAGS --- #########
def test_verify_integrity_tags(dict_tags, object_det):
    result = verify_integrity_tags(dict_tags, object_det)
    assert result is None

###### --- CONVERT THE TAGS IN TYPES STRING AND FLOAT --- ########
def test_convertion_tags(dict_tags):
    result = convertion_tags(dict_tags)
    assert isinstance(result, tuple)

###### --- PRODUCTING A PRODUCT FROM THE FUNCTION MANUFACTURE OF PRODUCT --- #####
def test_manufacture_product(tuple_product, dipirona_product_manufacture):
    result = manufacture_product(tuple_product)
    assert result == dipirona_product_manufacture

######################################################################################
##### --- TESTING FINAL PART OF DATA FLOW TO PARSING A XML, THE MANAGER. WITHIN SCOPE HAPPY PATH --- #####
def test_manager_import(functional_xml, expected_list_products_manufacture):
    'the result it must be an list of products, where each product be perfectly instantiated'
    result = manager_import(functional_xml, 
        extract_xml_data,
        extract_dets,
        find_tags,
        verify_integrity_tags,
        convertion_tags,
        manufacture_product
        )
    
    if isinstance(result, list) and len(result) == 3:
        assert result == expected_list_products_manufacture
        assert result[0] == expected_list_products_manufacture[0]
        assert result[1] == expected_list_products_manufacture[1]
        assert result[2] == expected_list_products_manufacture[2]

######################################################################################
###### --- SESSION OF THE XML_PARSER.PY TESTS TO THE UNSTABLE PATH --- ######
def test_manager_import_unstable(unstable_xml, expected_list_products_manufacture_unstable):
    'the result it must be an list of products, where the data of knot number 3 (most specifically the content in <cEAN></cEAN>) it is empty'
    result = manager_import(unstable_xml,
        extract_xml_data,
        extract_dets,
        find_tags,
        verify_integrity_tags,
        convertion_tags,
        manufacture_product
    )

    if isinstance(result, list) and len(result) == 3:
        assert result == expected_list_products_manufacture_unstable
        assert result[0] == expected_list_products_manufacture_unstable[0]
        assert result[1] == expected_list_products_manufacture_unstable[1]
        assert result[2] == expected_list_products_manufacture_unstable[2]

######################################################################################
###### --- SESSION OF THE XML_PARSER.PY TESTS TO THE MISSING TAGS PATH --- ######
def test_manager_import_missing_tags(missing_tags_xml, expected_list_products_manufacture_missing_tags):
    'the result it must be an list with only a product where is instantiated perfectly, because the remaining data is completly absent'
    result = manager_import(missing_tags_xml,
        extract_xml_data,
        extract_dets,
        find_tags,
        verify_integrity_tags,
        convertion_tags,
        manufacture_product
    )

    if isinstance(result, list) and len(result) == 1:
        assert result == expected_list_products_manufacture_missing_tags
        assert result[0] == expected_list_products_manufacture_missing_tags[0]

######################################################################################
###### --- SESSION OF THE XML_PARSER.PY TESTS TO THE MISSING DETS PATH --- ######
def test_manager_import_missing_all_dets(missing_dets_xml_data):
    'the result it must be an empty list, because data in knot det dont exist'
    result = manager_import(missing_dets_xml_data,
        extract_xml_data,
        extract_dets,
        find_tags,
        verify_integrity_tags,
        convertion_tags,
        manufacture_product
    )

    if isinstance(result, tuple) and len(result) == 0:
        assert result == ()

######################################################################################
###### --- SESSION OF THE XML_PARSER.PY TESTS TO THE BROKEN PATH --- ######
def test_manager_import_malformed_xml(malformed_xml_data):
    '''
    the result it must raised and captured an instance of ConversionError 
    in case the tags contain data with the correct intent but in a format unsuitable for conversion
    example:    WRONG: <qCom>TWENTY UNITS</qCom>    -> DONT ACCEPT THE USE OF LETTERS
                CORRECT: <qCom>20.000</qCom>        -> A FLOAT TYPE NUMBER
    '''
    result = manager_import(malformed_xml_data,
        extract_xml_data,
        extract_dets,
        find_tags,
        verify_integrity_tags,
        convertion_tags,
        manufacture_product
    )
    if isinstance(result, tuple) and len(result) == 0:
        assert result == ()

######################################################################################
###### --- SESSION OF THE XML_PARSER.PY TESTS TO THE BROKEN PATH --- ######
def test_manager_import_broken(broken_xml):
    'the result it must raised and captured an instance of ET.ParserError in case of the tags broken'

    result = manager_import(broken_xml,
            extract_xml_data,
            extract_dets,
            find_tags,
            verify_integrity_tags,
            convertion_tags,
            manufacture_product
        )
    if isinstance(result, tuple) and len(result) == 0:
        assert result == ()

######################################################################################
# ---> THE CONCLUSION THIS IT SUITE OF UNIT/INTEGRATION TESTS FOR THE MODULE XML_PARSER.PY AFTER A NEW ARCHTECTURE IS DEFINED IT HAPPENED AT SEPT 28, 2025.