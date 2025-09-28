###### --- IMPORTS --- ######
from debug_data import extract_xml_data 
from debug_data import extract_dets
from debug_data import find_tags
from debug_data import verify_integrity_tags
from debug_data import convertion_tags
from debug_data import manufacture_product
from debug_data import manager_import
import xml.etree.ElementTree as ET

###### --- NEW SESSION OF THE XML_PARSER.PY TESTS FOR RECEIVE THE NEW ARCHTECTURE --- ######
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

##### --- TESTING FINAL PART OF DATA FLOW TO PARSING A XML, THE MANAGER --- #####
def test_manager_import(functional_xml, expected_list_products_manufacture):

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


    

