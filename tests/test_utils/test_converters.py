### --- IMPORTS --- ###
from system.utils import converters
from system.utils.exceptions import ConversionError
from datetime import date
import pytest

### --- OBJECT DATE --- ###
def object_today() -> date:
    today = date.today()
    return today
today = object_today()

### --- TEST PRICE STR CONVERSOR --- ###
@pytest.mark.parametrize('price_str, expected_result', 
    [
        ### ---> FLOAT SCENARIO
        ('10,99', 10.99,),
        ('10.99', 10.99,),

        ### ---> EXCEPTIONS'S SCENARIO
        (None, None,),
        (10.1, ValueError,),
        (10, ValueError,),
        ('ten,dollars', ValueError,),
        ('ten.dollars', ValueError,),
        (('ten', ',', 'dollars',), TypeError,),
        (('ten', '.', 'dollars',), TypeError,),
        (['ten', ',', 'dollars'], TypeError,),
        (['ten', '.', 'dollars'], TypeError,),
        ({'ten': 10, '.': '.', 'dollars': 'dollars'}, TypeError,),
        (today, TypeError,)
    ]
)
def test_price_str_conversor(price_str, expected_result):

    result = converters.price_str_conversor(price_str)
    assert result == expected_result