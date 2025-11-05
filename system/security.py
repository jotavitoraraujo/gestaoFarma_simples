### --- IMPORTS --- ###
from typing import Callable
from secrets import token_bytes
from hashlib import pbkdf2_hmac
from hmac import compare_digest
#############################

def generate_salt() -> bytes:
    'generete salt to use with 16 bytes'

    salt: bytes = token_bytes(16)
    return salt

def hash_pin(pin: str, salt: bytes) -> str:
    'convert a pin and salt in a hash hexadecimal'

    pin_bytes: bytes = pin.encode('utf-8')
    hash_bytes: bytes = pbkdf2_hmac('sha256', pin_bytes, salt, 100000)
    hash_hex: str = hash_bytes.hex()
    return hash_hex

def compare_pin(provided_hash_hex: str, stored_hash: str) -> bool:
    'compare the stored hex in databasbe with a new calculate hash hex'

    result: bool = compare_digest(provided_hash_hex, stored_hash)
    return result

def verify_pin(stored_hash: str,  stored_salt: bytes, provided_pin: str, func_compare: Callable[[bytes, bytes], bool]) -> bool:
    'verify if a pin is same the provided pin from user'

    provided_pin_bytes: bytes = provided_pin.encode('utf-8')
    provided_hash: bytes = pbkdf2_hmac('sha256', provided_pin_bytes, stored_salt, 100000)
    provided_hash_hex: str = provided_hash.hex()
    result: bool = func_compare(provided_hash_hex, stored_hash)

    return result


