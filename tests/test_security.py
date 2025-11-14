### --- IMPORTS --- ###
from system import security
from typing import Callable
import hashlib
import secrets
import pytest
###

def test_security_generate_salt():

    ### --- PHASE ARRANGE --- ###
    func_salt: Callable = security.generate_salt
    ### --- PHASE ACT --- ###
    result: bytes = func_salt()
    ### --- PHASE ASSERT --- ###
    assert type(result) == bytes and len(result) == 16

@pytest.mark.parametrize('pin, salt', 
    
    [
        ### --- PHASE ARRANGE --- ###
        ('0000', b'TEST_SALT'),
        ('TEST_HASH', b'SALT_TEST'),
        ('A1B2', b'TEST_TEST_SALT'),
        ('C3D4', b'SALT_SALT_TEST')
    ] 
)
def test_security_hash_pin(pin: str, salt: bytes):


    ### --- PHASE ACT --- ###
    direct_hash: bytes = hashlib.pbkdf2_hmac('sha256', pin.encode('utf-8'), salt, 100000).hex()
    result_func: bytes = security.hash_pin(pin, salt)

    ### --- PHASE ASSERT --- ###
    assert direct_hash == result_func

def test_security_compare_pin():

    ### --- PHASE ARRANGE --- ###
    hash_A: str = 'HASH_A'
    hash_B: str = 'HASH_B'

    ### --- PHASE ACT --- ###
    result: bool = security.compare_pin(hash_A, hash_A)
    result2: bool = security.compare_pin(hash_A, hash_B)
    ### --- PHASE ASSERT --- ###
    assert result is True
    assert result2 is False

def test_security_verify_pin():

    ### --- PHASE ARRANGE --- ###
    true_pin: str = '0000'
    false_pin: str = '9999'
    salt: bytes = security.generate_salt()
    hash_stored: str = security.hash_pin(true_pin, salt)
    func_compare: function[Callable] = security.compare_pin

    ### --- PHASE ACT --- ###
    result: bool = security.verify_pin(hash_stored, salt, true_pin, func_compare)
    result2: bool = security.verify_pin(hash_stored, salt, false_pin, func_compare)

    ### --- PHASE ASSERT --- ###
    assert result is True
    assert result2 is False