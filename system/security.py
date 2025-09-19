### --- IMPORTS --- ###
from system.utils.exceptions import ConversionError
from hashlib import sha256

### --- PASS CONVERSOR --- ###
def password_for_hash_conversor(pin_digit: str) -> str:
    'this function will encrypt a password with sha256'
    
    try:
        
        if not isinstance(pin_digit, str): 
            raise TypeError    
        pin_bytes = pin_digit.encode()    
        
        if not isinstance(pin_bytes, bytes):
            raise TypeError
        
        pin_cripto = sha256(pin_bytes).hexdigest()
        return pin_cripto 
    
    except (ValueError, TypeError, AttributeError) as conversion_error:
        raise ConversionError('[ERRO] Os dados inseridos estão corrompidos ou são inválidos.', conversion_error, pin_digit) from conversion_error