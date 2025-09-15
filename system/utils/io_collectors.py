### --- IMPORTS --- ###
from system.utils import converters, validators
from system import security
from datetime import date
from pwinput import pwinput
import logging



### --- INPUT/OUTPUT COLLECTORS FUNCTIONS --- ###

def collect_price() -> float:
    while True:
        ask_price = f'[ALERTA] Insira o preço: [EX: 10,99]'
        price_str = input(f'{ask_price}')
        price_float = converters.price_str_conversor(price_str)
        price_validated = validators.price_validator(price_float)
        if price_validated is True:
            break
        else: 
            logging.error(f'[ERRO] O preço inserido não é válido. Tente novamente.')
    return price_float

def collect_expiration_date() -> date:
    while True:
        ask_date = f'[ALERTA] Insira a data de validade: [EX: DD/MM/AAAA]'
        date_str = input(f'{ask_date}')
        object_date = converters.expiration_date_str_conversor(date_str)
        date_validated = validators.batch_expiration_date_validator(object_date)
        if date_validated is True:
            break
        else:
            logging.error(f'[ERRO] Data de validade inválida. Tente novamente.')
    return object_date

def collect_user_name() -> str: 
    while True:
        print(f'[ALERTA] O padrão para nomes de usuário é utilizar nome e sobrenome sem espaços. Exemplo: MARIASILVA')
        ask_name = f'[ALERTA] Insira o nome de usuário: '
        user_name_input = input(f'{ask_name}')
        user_name = converters.user_name_conversor(user_name_input)
        user_name_validated = validators.user_name_validator(user_name)
        if user_name_validated is True:
            break
        else:
            logging.error(f'[ERRO] O nome de usuário inserido é inválido. Tente novamente.')
    return user_name

def collect_user_pin() -> str:
    while True:
        print(f'[ALERTA] O padrão para senha é utilizar 4 digitos númericos. Exemplo: 1234')
        ask_pin = f'[ALERTA] Insira a senha: '
        pin_input = pwinput(f'{ask_pin}')
        user_pin_validated = validators.user_pass_validator(pin_input)
        if user_pin_validated is True:
            user_pin = security.password_for_hash_conversor(pin_input)
            break
        else:
            logging.error(f'[ERRO] A senha inserida é inválida. Tente novamente.')
    return user_pin

def collect_quantity():
    while True:
        ask_quantity = f'[ALERTA] Insira a quantidade: '
        quantity_input = input(f'{ask_quantity}')
        quantity = converters.batch_quantity_conversor(quantity_input)
        quantity_validated = validators.batch_quantity_validator(quantity)
        if quantity_validated is True:
            break
        else:
            logging.error(f'[ALERTA] A quantidade inserida é inválida. Tente novamente.')
    return quantity

def collect_batch_physical() -> str:
    while True:
        ask_batch = f'[ALERTA] Insira o lote fisíco impresso na caixa deste item: '
        batch_input = input(f'{ask_batch}')
        print(f'[ALERTA] O lote fisíco digitado é: {batch_input}.')
        print(f'[ALERTA] Para confirmar digite: 1 | Para corrigir digite: 0')
        batch_confirmation = input(f'Insira a opção: ')
        batch_tuple: tuple = (batch_input, batch_confirmation,)
        batch_validated = validators.batch_physical_validator(batch_tuple)
        if batch_validated is True:
            break
        else:
            logging.error(f'[ERRO] O lote fisico inserido é inválido. Tente novamente ou contacte o administrador.')
    return batch_input

### --- COLLECTOR MENU ADMINISTRATION --- ###
def collector_menu(option: str = None) -> str:
    'collect all data send by the user'

    print('= ' * 15, 'MENU', ' =' * 15)
    print(f'1. Preço')
    print(f'2. Data de Validade')
    print(f'3. Nome de Usuário')
    print(f'4. PIN')
    print(f'5. Quantidade')
    print(f'6. Lote Fisíco')
    print(f'0. Sair')

    if isinstance(option, str) and option.isdigit() or option == None:
        while True:

            ask_menu = f'[ALERTA] Selecione uma opção e insira os dados: '
            
            if option is not None:
                ask_menu_option = option 
            else:
                ask_menu_input = input(f'{ask_menu}')

            if ask_menu_input == '1' or ask_menu_option == '1':
                price = collect_price()
                return price
            
            elif ask_menu_input == '2' or ask_menu_option == '2':
                expiration_date = collect_expiration_date()
                return expiration_date
                
            elif ask_menu_input == '3' or ask_menu_option == '3':
                user_name = collect_user_name()
                return user_name

            elif ask_menu_input == '4' or ask_menu_option == '4':
                user_pin = collect_user_pin()
                return user_pin
                
            elif ask_menu_input == '5' or ask_menu_option == '5':
                quantity = collect_quantity()
                return quantity
            
            elif ask_menu_input == '6' or ask_menu_option == '6':
                batch_physical = collect_batch_physical()
                return batch_physical
            
            elif ask_menu_input == '0' or ask_menu_option == '0':
                    logging.info(f'[INFO] Saindo do Menu...')
                    break
            else:
                logging.error(f'[ERRO] Opção inválida. Tente novamente.')
    else:
        logging.error(f'[ERRO] O valor inserido não é valido ou está corrompido.')
        return None