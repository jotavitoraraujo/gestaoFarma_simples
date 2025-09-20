### --- IMPORTS --- ###
from system.utils.exceptions import ConversionError
from system  import security
from hashlib import sha256
import pytest

### --- HASH EXPECTED --- ###
@pytest.mark.parametrize('pin_input, hash_expected', 

    [
        ('1234', '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4',),
        ('1020', 'f296867839c8befafed32b55a7c11ab4ad14387d2434b970a55237d537bc9353',),
        ('3040', '4ee813262a515c9aace96ef879e65667855c4ec290ca31f5bd49eb69a5e05ae7',),
        ('/', '8a5edab282632443219e051e4ade2d1d5bbc671c781051bf1437897cbdfea0f1',),
        ('letters', '7ad8dbe5dbed0dcda5e2fa713de5ddb5b6db23d8b7f4fc0ed2650b5b071107c7',),
        (1234, ConversionError,),
        (4321, ConversionError,)
    ]
)
def test_password_for_hash_conversor(pin_input: str, hash_expected):

    if isinstance(pin_input, str):
        result = security.password_for_hash_conversor(pin_input)
        assert result == hash_expected
    else:
        with pytest.raises(hash_expected):
            security.password_for_hash_conversor(pin_input)