### --- IMPORTS --- ###
from system.utils import converters, validators, io_collectors, exceptions
from unittest.mock import patch
from datetime import date
import pytest

### --- TEST COLLECT PRICE INPUT --- ###

@patch('builtins.input')
@patch('system.utils.converters.price_str_conversor')
@patch('system.utils.validators.price_validator')
def test_collect_gerenic_input(mock_validator, mock_conversor, mock_input):
    'test for function collect_price()'

    ask_test: str = f'[TEST] THIS STRING IS AN TEST TEXT: '
    
    mock_validator.return_value = True
    mock_conversor.return_value = 10.99
    mock_input.return_value = '10,99'

    result = io_collectors._collector_generic_input(ask_test, mock_conversor, mock_validator, mock_input)
    expected_result = 10.99

    if isinstance(result, float):
        assert result == expected_result
        assert mock_validator.call_count == 1
        assert mock_conversor.call_count == 1

@patch('builtins.input')
@patch('system.utils.converters.price_str_conversor')
@patch('system.utils.validators.price_validator')
def test_collect_gerenic_input_2(mock_validator, mock_conversor, mock_input):

    ask_test: str = f'[TEST] THIS STRING IS AN TEST TEXT: '
    
    mock_validator.return_value = True
    mock_conversor.side_effect = exceptions.ConversionError('ERROR'), 10.99
    mock_input.side_effect = '-1', '10,99'

    result = io_collectors._collector_generic_input(ask_test, mock_conversor, mock_validator, mock_input)
    expected_result = 10.99

    if isinstance(result, float):
        assert result == expected_result
        assert mock_validator.call_count == 1
        assert mock_conversor.call_count == 2