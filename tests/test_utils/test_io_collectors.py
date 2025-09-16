### --- IMPORTS --- ###
from system.utils import io_collectors, exceptions
from unittest.mock import patch
from datetime import date
import pytest

### --- TEST COLLECT PRICE INPUT --- ###

@patch('builtins.input')
@patch('system.utils.converters.price_str_conversor')
@patch('system.utils.validators.price_validator')
def test_collect_price(mock_validators, mock_converters, mock_input):

    mock_input.return_value = '10,99'
    mock_converters.return_value = 10.99
    mock_validators.return_value = True
    result = io_collectors.collect_price()

    if isinstance(result, float):
        assert result == 10.99

@patch('builtins.input')
@patch('system.utils.converters.price_str_conversor')
@patch('system.utils.validators.price_validator')
def test_collect_price_2(mock_validators, mock_converters, mock_input):

    mock_input.side_effect = 'letters', '10,99'
    mock_converters.side_effect = exceptions.ConversionError('[ERRO] MESSAGE TEST'), 10.99
    mock_validators.return_value = True
    result = io_collectors.collect_price()

    if isinstance(result, float):
        assert result == 10.99
        assert mock_converters.call_count == 2
        assert mock_validators.call_count == 1

@patch('builtins.input')
@patch('system.utils.converters.price_str_conversor')
@patch('system.utils.validators.price_validator')
def test_collect_price_3(mock_validators, mock_conversor, mock_input):

    mock_input.side_effect = '0,0', '10,99'
    mock_conversor.side_effect = 0.0, 10.99
    mock_validators.side_effect = False, True
    result = io_collectors.collect_price()

    if isinstance(result, float):
        assert result == 10.99
        assert mock_conversor.call_count == 2
        assert mock_validators.call_count == 2
