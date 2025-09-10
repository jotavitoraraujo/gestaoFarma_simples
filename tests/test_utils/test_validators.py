### --- IMPORTS --- ###
from system.utils import validators
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