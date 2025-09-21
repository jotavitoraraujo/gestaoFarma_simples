import sqlite3
from system.utils import converters, validators, exceptions
from hashlib import sha256
from datetime import date
import sys
import logging
from pwinput import pwinput
from typing import Callable, TypeVar

###############################################################################
print('\n')
print(f'=' * 25, '--- PYTHON AND SQLITE3 VERSION ---', '=' * 25)
print(f'Python Version: {sys.version}')
print(f'Sqlite3 Version: {sqlite3.sqlite_version_info}')
print(f'=' * 50)
###############################################################################

#################### --- ADAPTERS AND CONVERSORS --- ####################
def date_adapter(object_date: date) -> str:
    'receives an object_date in the date adapter for adaptation to the new pattern of sqlite3'
    #print('Adapter Called')
    adapter_format_str = object_date.isoformat()
    return adapter_format_str

def date_conversor(object_bytes: bytes) -> date:
    'receives an object_bytes from database for the converting in a object_date to python'
    #print('Conversor Called')
    convert_object_str = object_bytes.decode()
    adapter_format_date = date.fromisoformat(convert_object_str)
    return adapter_format_date

####### --- DATE OBJECT -> BYTES (STR) OBJECT --- #######
sqlite3.register_adapter(date, date_adapter)
####### --- BYTES (STR) OBJECT -> DATE OBJECT --- #######
sqlite3.register_converter('date', date_conversor)

####### --- CREATING AN DB WITHIN MEMORY --- #######
test_conn = sqlite3.connect(':memory:', detect_types = sqlite3.PARSE_DECLTYPES)
cursor = test_conn.cursor()
object_today = date.today()

###############################################################################
print(f'=' * 25, '--- TYPE INPUT ---', '=' * 25)
print(f'[DEBUG] Type Object Input in Database: {type(object_today)}')
print(f'=' * 50)
print('\n')
print(f'#' * 25, '--- WARNING HERE ---', '#' * 25)
###############################################################################

####### --- CREATING TABLE, INSERTING VALUE AND SELECTING THE OBJECT--- #######
cursor.execute('''
        CREATE TABLE IF NOT EXISTS test (
        id INTEGER PRYMARY KEY,
        date_today DATE NOT NULL
        )
    ''')
cursor.execute('''
        INSERT INTO test (date_today)
        VALUES (?)
    ''',
    (
        object_today,
    ))

cursor.execute('''
        SELECT *
        FROM test
    ''')
return_database = cursor.fetchall()
test_conn.commit()
test_conn.close()

###############################################################################
print(f'#' * 25, '--- WARNING HERE ---', '#' * 25)
print('\n')
print(f'=' * 25, '--- TYPE OUTPUT ---', '=' * 25)
print(f'[DEBUG] Type Object Output from Database: {type(return_database[0][1])}')
print(f'=' * 50)
###############################################################################

######## --- THIS SESSION IS RESPONSABLE FOR ENCRYPTING A TEST PASSWORD --- #########

pin_input = '1234'
pin_bytes = pin_input.encode()
pin_cripto = sha256(pin_bytes).hexdigest()
print('\n')
print('=' * 50)
print(f'Encrypting Password Hash: {pin_cripto}')
print(f'Type for object hash: {type(pin_cripto)}')
print('=' * 50)

######## --- THIS SESSION IS AN EXPERIMENT FOR A NEW FUCTION --- ########

######## --- TYPE HINT EXPERIMENT WITH TYPEVAR --- ########
joker_type = TypeVar('joker_type')

######## --- FUNCTION --- ########
def _collector_generic_input(ask: str, 
    func_conv: Callable[[str], joker_type], 
    func_valid: Callable[[joker_type], bool], 
    func_input: Callable = input):

    while True:
        ask_input = func_input(f'{ask}')
        try:
            conversion_result = func_conv(ask_input)
            validated_result = func_valid(conversion_result)
            if validated_result is True:
                return conversion_result
            else:
                logging.error(f'[ERRO] Os dados inseridos são inválidos. Tente novamente.')
        except exceptions.ConversionError:
            logging.error(f'[ERRO] Os dados inseridos são inválidos. Tente novamente.')

def return_value(value):
    return value

def collect_price() -> float:
    print('=' * 30)
    print('APLICAR PREÇO')
    print('=' * 30)


    converter = return_value
    validator = validators.price_validator

    ask_price = f'[ALERTA] Insira o preço: '
    result = _collector_generic_input(ask_price, converter, validator)
    return result 