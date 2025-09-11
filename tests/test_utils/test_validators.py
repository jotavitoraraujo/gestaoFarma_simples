### --- IMPORTS --- ###
from system.utils import validators
from datetime import date
import pytest

### --- TEST BATCH QUANTITY VALIDATOR --- ###
@pytest.mark.parametrize('input, expected_result', 
    [
        ### --- > TRUE SCENARIO
        (1, True,),
        (11111111111111, True,),
        
        ### --- > FALSE SCENARIO
        (0, False,),
        (-1, False,),
        (0000000, False,),
        (1.1, False,),
        (0.1, False,),
        (-1.1, False,),
        ('letters', False,),
        ('1', False,),
        ('@', False,)
    ])
def test_batch_quantity_validator(input, expected_result):
    
    result = validators.batch_quantity_validator(input)
    assert result == expected_result

### --- TEST BATCH PHYSICAL VALIDATOR --- ###
@pytest.mark.parametrize('input_tuple, expected_result', 
    [
        ### ---> TRUE SCENARIO
        (('BATCH123A', '1',), True,),
        (('12345678910', '1',), True,),
        (('letters', '1',), True,),

        ### --- > FALSE SCENARIO
        (('-1', '1',), False,),
        (('/', '1',), False,),
        (('', '1',), False,),
        ((' ', '1',), False,),        
        (('BATCH123A', '0',), False,),
        (('1', '0',), False,),
        (('-1', '0',), False,),
        (('/', '0',), False,),
        (('', '0',), False,),
        ((' ', '0',), False,),
        (('BATCH123B', '2',), False,),
        (['BATCH123C', '1',], False,),
        (('BATCH123D',), False),
        ('BATCH123E', False,)
        
])
def test_batch_physical_validator(input_tuple, expected_result):

    result = validators.batch_physical_validator(input_tuple)
    assert result == expected_result

### --- TEST USER PASS VALIDATOR --- ###
@pytest.mark.parametrize('input, expected_result', 
    [
        ### --- > TRUE SCENARIO
        ('1234', True,),

        ### --- > FALSE SCENARIO
        ('12345', False,),
        ('12345678', False,),
        ('love', False,),
        ('LOVE', False,),
        ('    ', False,),
        ('', False,),
        ('****', False,),
        ('12AB', False,),
        ('AB12', False,),
        (('1', '2', '3', '4',), False,),
        (['1', '2', '3', '4',], False,),
        ((1, 2, 3, 4), False,),
        ([1, 2, 3, 4], False,),
        (1234, False,)
    ]
)
def test_user_pass_validator(input, expected_result):

    result = validators.user_pass_validator(input)
    assert result == expected_result

### --- TEST BATCH EXPIRATION DATE VALIDATOR --- ###
def object_past() -> date:
    object_date_past = date(2015, 8, 31)
    return object_date_past
def object_today() -> date:
    today = date.today()
    return today
def object_future() -> date:
    object_date_future = date(2035, 8, 31)
    return object_date_future

date_past = object_past()
date_today = object_today()
date_future = object_future()

@pytest.mark.parametrize('date, expected_result', 
    [
        ### --- > TRUE SCENARIO
        (date_future, True,),

        ### --- > FALSE SCENARIO
        (date_past, False,),
        (date_today, False,)
    ]
)
def test_batch_expiration_date_validator(date, expected_result):

    result = validators.batch_expiration_date_validator(date)
    assert result == expected_result

### --- TEST PRICE VALIDATOR --- ###
@pytest.mark.parametrize('price, expected_result', 
    [
        ### --- > TRUE SCENARIOS
        (0.1, True,),
        (0.01, True,),
        (0.001, True,),
        (1., True,),
        (1.1, True,),
        (123 * 3.12, True,),
        (123.1 ** 2.2, True,),
        (123.1 // 3.3, True,),
        (123.1 * 2, True,),
        

        ### --- > FALSE SCENARIOS
        (0, False,),
        (-1, False,),
        (-1., False),
        (-1.1, False),
        ('0', False,),
        ('1.0', False,),
        ('1.', False,),
        ('1.1', False,),
        ('-1.', False,),
        ((1.0,), False,),
        ((-1,), False,),
        ((1,), False,),
        ((0,), False,),
        ((1.0, 2.0, -3,), False,),
        ([1.0], False,),
        ([-1], False,),
        ([1], False,),
        ([0], False,),
        ([1.0, 2.0, -3], False,),
        (('1', '1.0', '-1',), False,),
        (['1', '1.0', '-1'], False,),
        ('oneDOTone', False,),
        (True, False,),
        (False, False,),
        (date_today, False,),
        (123 ** 2, False,),
        (123 // 2, False,),
        ({'one' : 1, '2': 2}, False,)

    ]
)
def test_price_validator(price, expected_result):

    result = validators.price_validator(price)
    assert result == expected_result