import pytest
from unittest.mock import patch
from sistema.modulos import validators
from datetime import date


######################################### --- TEST FUNCTION _convert_price_str ---############################################################
@pytest.mark.parametrize('input, expected_result', [
    ('letters', ValueError,), # input letters 
    ('/', ValueError,), # input special caracters
    ('10,99', 10.99,), # input price format brazilian
    ('10.99', 10.99,), # correct
    (' ', ValueError,), # none input
    ('-1', ValueError,) # negative price input            
])
def test_convert_str_to_price(input, expected_result):
    
    if isinstance(expected_result, float):
        result = validators._convert_price_str(input)
        assert result == expected_result
    else:
        with pytest.raises(expected_result):
            validators._convert_price_str(input)

######################################### --- TEST FUNCTION quantity_validator ---############################################################
@patch('builtins.input')
def test_quantity_validator(mock_input):
    mock_input.return_value = '5'
    resultado = validators.quantity_validator()
    assert resultado == 5

######################################### --- TEST FUNCTION batch_physical_validator ---############################################################
@patch('builtins.input')
def test_batch_physhical_validator(mock_batch_input):
    mock_batch_input.side_effect = ['ABC123CD', '0', 'ABC234CD', '1']
    result = validators.batch_physical_validator()
    true_result = 'ABC234CD'
    assert result == true_result

#########################################
@patch('builtins.input')
def test_batch_physhical_validator_two(mock_batch_input):
    mock_batch_input.side_effect = ['ABC123CD', '1']
    result = validators.batch_physical_validator()
    true_result = 'ABC123CD'
    assert result == true_result

######################################### --- TEST FUNCTION _expiration_date_validator ---############################################################
@pytest.mark.parametrize('input, expected_result', [
    ('19/08/2035', '2035-08-19',), # correct
    ('19-08-2025', ValueError,), # error invalid format
    ('17/08/2025', ValueError,), # error date in the past (bussiness rule)
    ('18/08/2025', ValueError,), # error date in the present (bussiness rule)
    ('abc', ValueError,), # '' format
    ('19082025', ValueError,), # '' format
    ('19 08 2025', ValueError,), # '' format
    ('31/02/2026', ValueError,)  # '' error impossible date
])
def test_expiration_date_conversor_validator(input, expected_result):

    if isinstance(expected_result, str):
        result = validators._expiration_date_conversor_validator(input)
        assert result == expected_result
    else:
        with pytest.raises(expected_result):
            validators._expiration_date_conversor_validator(input)

######################################### --- TEST FUNCTION date_validador ---############################################################
def date_instance():
    date_object = date(2026, 1, 1)
    return date_object

@patch('builtins.input')
def test_date_validator(mock_date_input):
    mock_date_input.return_value = '01/01/2026'
    result = validators.SaleItem_date_validator()
    date_object = date_instance()
    assert result == date_object


            



