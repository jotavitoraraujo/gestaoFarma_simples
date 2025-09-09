### --- IMPORTS --- ###
from hashlib import sha256

def password_for_hash(pin_digit: str) -> str:
    'this function will encrypt a password with sha256'

    pin_bytes = pin_digit.encode()
    pin_cripto = sha256(pin_bytes).hexdigest()
    
    return pin_cripto