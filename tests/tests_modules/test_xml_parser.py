import debug_data
import pytest
import xml.etree.ElementTree as ET
from system.modules import xml_parser



######################################### --- TEST SUIT FROM EXTRACT DATA NFE FUNCTION --- ########################################
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
    object_det = ET.fromstring(det_string)
    return object_det

def test_manufacture_product(object_det, dipirona_product_manufacture):

    product = debug_data.manufacture_product(object_det)
    assert product == dipirona_product_manufacture

