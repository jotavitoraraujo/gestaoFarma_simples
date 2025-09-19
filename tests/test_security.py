### --- IMPORTS --- ###
from system.utils.exceptions import ConversionError
from system  import security
from hashlib import sha256
import pytest

### --- HASH EXPECTED --- ###
@pytest.mark.parametrize('pin_input, hash_expected', 

    [
        ('1234', None,),
        ('1020', None,),
        ('3040', None,),
        ('/', None,),
        ('letters', None,),
        (1234, ConversionError,),
        (4321, ConversionError,)
    ]

)
def test_password_for_hash_conversor(pin_input: str, hash_expected, hash_list_test):

    if hash_expected is None:
        for hash in hash_list_test:
            result = security.password_for_hash_conversor(pin_input)
            assert result == hash
    
    else:
        with pytest.raises(hash_expected):
            security.password_for_hash_conversor(pin_input)