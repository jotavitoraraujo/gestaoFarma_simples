from sistema.modelos.user import User
from datetime import datetime, date
from pwinput import pwinput
import logging

######## --- THIS SESSION CONTAINS ONLY FUNCTIONS WITH PURPOSE OF CONVERT SOMETHING --- #######
def _convert_price_str(price_str: str) -> float:
    'convert str price in float price'

    price_converted = float(price_str.replace(',', '.'))   
    if price_converted > 0:
        pass
    else:
        raise ValueError
    return price_converted

######## --- THIS SESSION CONTAINS ONLY FUNCTIONS FOR THE PURPOSE OF VALIDATED SOMETHING --- #######
def quantity_validator() -> int:
    'check if a number is positive integer'
    
    while True:        
        quantity_ask = f'Quantidade: '
        quantity_input = input(f'{quantity_ask}')

        try:            
            quantity_formated = int(quantity_input)           
                            
            if quantity_formated > 0:
                break                                             
            else:
                logging.error(f'[ERRO] Entrada inválida, insira apenas números. Tente novamente.')
        
        except ValueError:
            logging.error(f'[ERRO] Dados inválidos. Tente novamente.')

    return quantity_formated

def batch_physical_validator() -> str:
    'valiate the input of the physical batch printed on the product'

    while True:
        batch_ask = f'Qual o lote impresso fisicamente neste item? (EX: AB123CD): '
        batch_input = input(f'{batch_ask}')
        print(f'O lote informado é ***{batch_input.upper()}***.')
        print(f'Você confirma que o lote ***{batch_input.upper()}*** está correto? ')
        batch_confirmation = input(f'Digite 1 para confirmar ou 0 para corrigir: ')
        
        if len(batch_confirmation) > 1:
            logging.error(f'[ERRO] Digite apenas 1 ou 0. Tente novamente')
        elif len(batch_confirmation) < 1:
            logging.error(f'[ERRO] Digite apenas 1 ou 0. Tente novamente.')
        else:
            if batch_confirmation == '1':
                batch_physical = batch_input
            elif batch_confirmation == '0':
                continue
            else:
                logging.error(f'[ERRO] Opção inválida. Tente novamente.')
        return batch_physical

def password_length_validator(pin_digit) -> bool:
    'this function verify if length of the a password is equal 4 digits'
    
    if len(pin_digit) != 4:
        print('[ERRO] A senha deve conter 4 digitos. Tente novamente.')                
    else:
        print('\n[SUCESSO] Senha cadastrada.')
        return True

def _expiration_date_conversor_validator(date_str: str) -> str:
    'convert and validate expiration date to acceptance in sql'

    expiration_list = date_str.split('/')
    if len(expiration_list) == 3:
        pass
    else:
        raise ValueError
    expiration_formated = f'{expiration_list[2]}-{expiration_list[1]}-{expiration_list[0]}'
    expiration_digited = datetime.strptime(expiration_formated, '%Y-%m-%d').date()

    if expiration_digited > datetime.now().date():
        expiration_str = datetime.strftime(expiration_digited, '%Y-%m-%d')
    else:
        raise ValueError
    return expiration_str

def SaleItem_date_validator() -> date:
    '''receives the date through user input and converts it into a date type object.
     This function is for the exclusive use of the SaleItem class, for now '''

    while True:

        try:
            date_input = input(f'[INFO] Insira a data (EX: DD/MM/AAAA): ')
            date_list = date_input.split('/')
            
            if len(date_list) == 3:
                pass
            else:
                logging.error(f'[ERRO] Formato de data inválido ({date_input}). Tente novamente.')
                continue                
            
            date_object = date(int(date_list[2]), int(date_list[1]), int(date_list[0]))
            
            if date_object < date.today():
                logging.warning(f'[ALERTA] A data inserida "{date_object}" é menor que a data de hoje. Tente novamente')
            else:
                break
        except (ValueError, IndexError):
            logging.error(f'[ERRO] Entrada inválida. Tente novamente.')
        
    return date_object

######## --- THIS SESSION CONTAINS ONLY FUNCTIONS FOR THE PURPOSE OF COLLETING USER INPUT --- #######
def collect_price_input() -> float:    
    'receive input the price'
    while True:                                         
        price_ask = f'Qual preço de venda deste novo item?: '
        price_input = input(f'{price_ask}')
        try:
            price_converted = _convert_price_str(price_input)
            break
        except ValueError:
            logging.error('\n [ERRO] Entrada inválida. Por favor, digite apenas números.')
    return price_converted

def collect_date_input() -> str:
    'receive input the expiration date'

    while True:                        
        expiration_date = f'Qual a validade deste novo item? (DIA/MÊS/ANO): '
        expiration_input = input(f'{expiration_date}')                        
        
        try:
            expiration_str = _expiration_date_conversor_validator(expiration_input)
            break
        except ValueError:
            logging.error('[ERRO] Data inválida. Tente novamente.')
    
    return expiration_str

def collect_user_name() -> str:
    'this function is responsable by collect input of user_name of client'
   
    while True:
        user_name = (input('\nInforme nome de usuário para cadastro (EXEMPLO: MARIA SILVA): '))
        user_name_formated = user_name.replace(' ', '')
        bool_user_name = user_name_formated.isalpha()
        
        if bool_user_name == True:
            break
        else:
            print('\n[ERRO] O nome de usuário deve conter apenas letras. Tente novamente.')
    return user_name_formated

def collect_user_pin() -> str:
    'this function is an validator of string that client input send to create the password'

    while True:
        pin_input = pwinput('Informe uma senha de 4 digitos para cadastro (EXEMPLO: 1234): ')
        bool_user_pin = pin_input.isdigit()

        if bool_user_pin == True:
            pin_digit = pin_input
            break
        else:
            logging.error('[ERRO] A senha deve conter apenas numeros. Tente novamente.')
    return pin_digit
















