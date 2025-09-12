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

def object_date() -> date:
    object_date = date(2035, 9, 12)
    return object_date
test_date = object_date()

### --- TEST PRICE STR CONVERSOR --- ###
@pytest.mark.parametrize('price_str, expected_result', 
    [
        ### ---> FLOAT SCENARIO
        ('10,99', 10.99,),
        ('10.99', 10.99,),

        ### ---> EXCEPTIONS'S SCENARIO
        (None, ConversionError,),
        (10.1, ConversionError,),
        (10, ConversionError,),
        ('ten,dollars', ConversionError,),
        ('ten.dollars', ConversionError,),
        (('ten', ',', 'dollars',), ConversionError,),
        (('ten', '.', 'dollars',), ConversionError,),
        (['ten', ',', 'dollars'], ConversionError,),
        (['ten', '.', 'dollars'], ConversionError,),
        ({'ten': 10, '.': '.', 'dollars': 'dollars'}, ConversionError,),
        (today, ConversionError,)
    ]
)
def test_price_str_conversor(price_str, expected_result):

    if isinstance(expected_result, float):
        result = converters.price_str_conversor(price_str)
        assert result == expected_result

    else:
        with pytest.raises(expected_result):
            converters.price_str_conversor(price_str)

### --- TEST EXPIRATION DATE STR CONVERSOR --- ###
@pytest.mark.parametrize('date_str, expected_result', 
    [
        ### --- > SUCESSFULL SCENARIO
        ('12/09/2035', test_date,),

        ### --- > FAIL SCENARIOS
        ('2035/09/35', ValueError,),
        ('09/2035/12', ValueError,),
        ('12-09-2035', ValueError,),
        ('2035-09-12', ValueError,),
        ('year/month/day', ValueError,),
        ('  /  /    ', ValueError,),
        ('///', ValueError,),
        ('', ValueError,),
        (12/9/2035, AttributeError,),
        (1, AttributeError,),
        (test_date, AttributeError,),        
        (('12/', '09/', '2035',), AttributeError,),
        (['12/', '09/', '2035'], AttributeError,),
        (None, AttributeError,),
        (True, AttributeError,),
        (False, AttributeError,),
        ('09/2035', ValueError,),
        ('09/', ValueError,),
        ('12/09/20/25', ValueError,)
    ]   
)
def test_expiration_date_str_conversor(date_str, expected_result):

    if isinstance(expected_result, date):
        result = converters.expiration_date_str_conversor(date_str)
        assert result == expected_result
    
    else:
        with pytest.raises(expected_result):
            converters.expiration_date_str_conversor(date_str)