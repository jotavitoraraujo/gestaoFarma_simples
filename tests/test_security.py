### --- IMPORTS --- ###
from system.utils.exceptions import ConversionError
from system  import security
from hashlib import sha256
import pytest

### --- HASH EXPECTED --- ###

@pytest.mark.parametrize('pin_input, expected_result', 

    [
        ('1234', None,),
        ('4321', None,),
        ('letters', None,),
        ('/', None,),
        (1234, ConversionError,),
        (4321, ConversionError,)
    ]

)
def test_password_for_hash_conversor(pin_input: str, expected_result):

    if expected_result is None:
        pin_bytes = pin_input.encode()
        pin_cripto = sha256(pin_bytes).hexdigest()
        result = security.password_for_hash_conversor(pin_input)
        assert result == pin_cripto
    
    else:
        with pytest.raises(expected_result):
            security.password_for_hash_conversor(pin_input)