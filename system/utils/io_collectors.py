### --- IMPORTS --- ###
from system.utils import converters, validators
from system.utils.exceptions import ConversionError
from system import security
from datetime import date
from typing import Callable, TypeVar
from pwinput import pwinput
import logging

### --- DEFINITION JOKER_TYPE WITH TYPEVAR TYPE HINT --- ###
joker_type = TypeVar('joker_var')

### --- JOKER FOR CONVERTER --- ###
def return_value(x):
    return x

### --- INTERNAL FUNCTION RESPONSABLE BY INPUT CONTROLLER WORKFLOW --- ###
def _collector_generic_input(ask: str, 
    func_conv: Callable[[str], joker_type], 
    func_valid: Callable[[joker_type], bool], 
    func_input: Callable = input) -> joker_type:

    while True:
        ask_input = func_input(f'{ask}')
        try:
            conversion_result = func_conv(ask_input)
            validated_result = func_valid(conversion_result)
            if validated_result is True:
                return conversion_result
            else:
                logging.error(f'[ERRO] Os dados inseridos são inválidos. Tente novamente.')
        except ConversionError:
            logging.error(f'[ERRO] Os dados inseridos são inválidos. Tente novamente.')
   

### --- INPUT/OUTPUT COLLECTORS FUNCTIONS --- ###
def collect_price() -> float:
    # print('=' * 30)
    # print('APLICAR PREÇO')
    # print('=' * 30)

    converter = converters.price_str_conversor
    validator = validators.price_validator

    ask_price = f'[ALERTA] Insira o preço: '
    price = _collector_generic_input(ask_price, converter, validator)
    return price    

def collect_expiration_date() -> date:
    # print('=' * 30)
    # print('DEFINIÇÃO DE DATA')
    # print('[ALERTA] O padrão para definições de data no GestãoFarma Simples é: DD/MM/AAAA')
    # print('=' * 30)

    converter = converters.expiration_date_str_conversor
    validator = validators.batch_expiration_date_validator

    ask_date = f'[ALERTA] Insira a data: '
    expiration = _collector_generic_input(ask_date, converter, validator)
    return expiration

def collect_user_name() -> str: 
    # print('=' * 30)
    # print('NOME DE USUÁRIO')
    # print('[ALERTA] O padrão para nomes de usuário no GestãoFarma Simples é: NOMESOBRENOME [EX: MARIASILVA]')
    # print('=' * 30)

    converter = converters.user_name_conversor
    validator = validators.user_name_validator

    ask_user_name = f'[ALERTA] Insira o Nome de Usuário: '
    user_name = _collector_generic_input(ask_user_name, converter, validator)
    return user_name

def collect_user_pin() -> str:
    # print('=' * 30)
    # print('DEFINIÇÃO DE SENHA')
    # print('[ALERTA] O padrão de definição de senhas do GestãoFarma Simples é: 4 digitos numéricos [EX: 1234]')
    # print('=' * 30)

    converter = converters.return_value
    validator = validators.user_pass_validator
    mask_pass = pwinput

    ask_pass = f'[ALERTA] Insira a senha: '
    user_pass = _collector_generic_input(ask_pass, converter, validator, mask_pass)
    return user_pass

def collect_quantity() -> int:
    # print('=' * 30)
    # print('INSERÇÃO DE QUANTIDADE')
    # print('=' * 30)

    conversor = converters.batch_quantity_conversor
    validator = validators.batch_quantity_validator

    ask_quantity = f'[ALERTA] Insira a quantidade deste item: '
    quantity = _collector_generic_input(ask_quantity, conversor, validator)
    return quantity

def collect_batch_physical() -> str:
    # print('=' * 30)
    # print('REGISTRO DE LOTE FISICO')
    # print('''[ALERTA] O lote físico solicitado é o lote impresso na caixa do produto.
    # \nGeralmente em um padrão Alphanumerico [EX: LOTE123FISICO]' 
    # ''')
    # print('=' * 30)

    conversor = return_value
    validator = validators.batch_physical_validator    

    ask_batch_physical = f'[ALERTA] Insira o Lote Fisico: '
    batch_physical = _collector_generic_input(ask_batch_physical, conversor, validator)
    return batch_physical

### --- COLLECTOR MENU ADMINISTRATION --- ###
def collector_menu(option: str = None) -> joker_type:
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