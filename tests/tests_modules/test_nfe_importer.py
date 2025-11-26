### --- IMPORTS --- ###
from system.modules.nfe_importer import NFEImporter
from system.models.product import Product
from unittest.mock import Mock, MagicMock, patch, mock_open

### --- TEST SUITE TO NFE_IMPORTER FUNCTION --- ###
@patch('builtins.open', new_callable = mock_open)
def test_nfe_importer(mock_file_handle: Mock, rich_products_list: list[Product], functional_xml_real):

    ### --- PHASE ARRANGE --- ###
    mock_file_handle.return_value.read.return_value = functional_xml_real # MOCK TO KEYWORD OPEN
    mock_xml_parser = MagicMock() # XMLPARSER CLASS
    mock_xml_parser_instance = MagicMock() # XMLPARSER Instance
    mock_xml_parser.return_value = mock_xml_parser_instance # RETURN OF CLASS = INSTANCE
    #########################
    mock_xml_parser_instance.get_products.return_value = rich_products_list # CALL AND RETURN OF METHOD
    #########################
    mock_persistence = MagicMock() # INSTANCE PRODUCT_REPOSITORY
    mock_persistence.return_value = ({'ACTIVE': 3, 'QUARANTINE': 0}, [])
    #########################
    mock_dispatcher = MagicMock()
    #########################
    
    ### --- PHASE ACT --- ###
    importer = NFEImporter(mock_xml_parser, mock_dispatcher, mock_persistence) # INSTANCE: NFE IMPORTER WITH THE MOCKS
    importer.run_import('fake/path.xml') # FAKE PATH TO CALL PUBLIC METHOD OF NFEIMPORTER

    ### --- PHASE ASSERTION --- ###
    mock_xml_parser.assert_called_once_with(functional_xml_real) == 1 # LINE 27 NFE_IMPORTER.PY = VALIDATED
    mock_xml_parser_instance.execute_process.assert_called_once() == 1 # LINE 30 NFE_IMPORTER.PY = VALIDATED
    mock_persistence.assert_called_once_with(rich_products_list) == 1 # LINE 32 NFE_IMPORTER.PY = VALIDATED
    mock_dispatcher.publish.assert_not_called() == 0 # LINE 42 NFE_IMPORTER.PY = VALIDATED