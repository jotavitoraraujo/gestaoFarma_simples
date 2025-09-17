### --- IMPORTS --- ###
from system.utils import converters, validators, io_collectors, exceptions
from system import security
from unittest.mock import patch, ANY
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

@pytest.mark.parametrize('public_func, conversor_func, validator_func', 
        [
            (
                io_collectors.collect_price, 
                converters.price_str_conversor,
                validators.price_validator,
            ),

            (
                io_collectors.collect_expiration_date,
                converters.expiration_date_str_conversor,
                validators.batch_expiration_date_validator,
            ),

            (
                io_collectors.collect_user_name,
                converters.user_name_conversor,
                validators.user_name_validator,
            ),

            (
                io_collectors.collect_quantity,
                converters.batch_quantity_conversor,
                validators.batch_quantity_validator,
            ),

            (
                io_collectors.collect_batch_physical,
                io_collectors.return_value,
                validators.batch_physical_validator,
            )
        ]
    )
@patch('system.utils.io_collectors._collector_generic_input')
def test_public_functions(mock_generic_input, public_func, conversor_func, validator_func):

    public_func()
    assert mock_generic_input.assert_called_once_with(ANY, conversor_func, validator_func)