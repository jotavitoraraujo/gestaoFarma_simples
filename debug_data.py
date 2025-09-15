import sqlite3
from system.utils import converters, validators
from hashlib import sha256
from datetime import date
import sys
import logging

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

def collector_input(option: str = None) -> str:
    'collect all data send by the user'

    print('= ' * 15, 'MENU', ' =' * 15)
    print(f'1. Preço')
    print(f'2. Data de Validade')
    print(f'3. Nome de Usuário')
    print(f'4. PIN')
    print(f'5. Quantidade')
    print(f'6. Lote Fisíco')
    print(f'0. Sair')

    if isinstance(option, str) or option == None:
        while True:

            ask_menu = f'[ALERTA] Selecione uma opção e insira os dados: '
            
            if option is not None:
                ask_menu_option = option 
            else:
                ask_menu_input = input(f'{ask_menu}')

            if ask_menu_input == '1' or ask_menu_option == '1':
                ask_price = f'[ALERTA] Insira o preço desejado: '
                price_input = input(f'{ask_price}')
                
                if price_input.isdigit():
                    return price_input
                else:
                    logging.error(f'[ERRO] Entrada inválida. Tente novamente.')
            
            elif ask_menu_input == '2' or ask_menu_option == '2':
                ask_date = f'[ALERTA] Insira a data de validade impressa no item: EX: (DD/MM/AAAA)'
                expiration_date_input = input(f'{ask_date}')
                
                result = converters.expiration_date_str_conversor(expiration_date_input)
                if isinstance(result, date):
                    return expiration_date_input
                else:
                    logging.error(f'[ERRO] Data de Validade inválida. Tente novamente.')
                
            elif ask_menu_input == '3' or ask_menu_option == '3':
                ask_user_name = f'[ALERTA] Insira o nome de usuário: '
                user_name_input = input(f'{ask_user_name}')

                if user_name_input.isalpha():
                    return user_name_input
                else:
                    logging.error(f'[ERRO] Nome de usuário inválido. Tente novamente.')

            elif ask_menu_input == '4' or ask_menu_option == '4':
                ask_pin = f'[ALERTA] Insira o PIN de 4 digitos: '
                pin_input = (f'{ask_pin}')

                result = validators.user_pass_validator(pin_input)
                if result is True:
                    return pin_input
                else:
                    logging.error(f'[ERRO] PIN inválido. Tente novamente.')
                
            elif ask_menu_input == '5' or ask_menu_option == '5':
                ask_quantity = f'[ALERTA] Insira a quantidade deste item: '
                quantity_input = input(f'{ask_quantity}')

                result = validators.batch_quantity_validator(quantity_input)
                if result is True:
                    return quantity_input
                else:
                    logging.error(f'[ERRO] Quantidade inserida inválida. Tente novamente.')
            
            elif ask_menu_input == '6' or ask_menu_option == '6':
                ask_pyshical_batch = f'[ALERTA] Insira o Lote Fisico impresso neste item: '
                physical_batch_input = input(f'{ask_pyshical_batch}')

                if physical_batch_input.isalnum():
                    result = str(input(
                    f'''
                    [ALERTA] O Lote Fisico informado é {physical_batch_input.upper()}. 
                    \n1. Confirmar
                    \n2.Corrigir
                    \nSelecione uma opção: 
                    '''
                    ))
                    if result != '0':
                        return physical_batch_input
                
                else:
                    logging.error(f'[ERRO] O Lote Fisico inserido é inválido. Tente novamente.')
            
            elif ask_menu_input == '0' or ask_menu_option == '0':
                    logging.info(f'[INFO] Saindo do Menu...')
                    break
            else:
                logging.error(f'[ERRO] Opção inválida. Tente novamente.')
    else:
        logging.error(f'[ERRO] O valor inserido não é valido ou está corrompido.')
        return None
    
collector_input()