### --- IMPORTS --- ###
from system.utils import io_collectors
from unittest.mock import patch
from datetime import date
import pytest

### --- INSTANCES --- ###
true = True
object_date = date.today()
### --- TEST COLLECT PRICE INPUT --- ###
@pytest.mark.parametrize('mock_return, expected_result', 
    [
        ### ---> SUCESSFULL SCENARIOS
        ('letters', 'letters',),
        ('1', '1',),
        ('-1', '-1',),
        ('1.1', '1.1',),
        ('/', '/',),
        ('1   ', '1   ',),
        ('  1', '  1',),
        (' ', ' ',),
        ('', '',),
        (f'{true}', 'True',),
        (f'{object_date}', '2025-09-13'),
        (None, None,)    
    ]
)
@patch('builtins.input')
def test_collect_price_input(mock_input, mock_return, expected_result):
    mock_input.return_value = mock_return
    result = io_collectors.collect_price_input()
    print(type(result))
    assert result == expected_result