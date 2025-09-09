### --- IMPORTS --- ###
import logging
import pwinput

### --- INPUT/OUTPUT COLLECTORS FUNCTIONS --- ###
def collect_price_input() -> str:    
    'receive input the price'

    price_ask = f'Qual preço de venda deste novo item?: '
    price_input = input(f'{price_ask}')
    
    if price_input is not None:
        pass
    else:
        logging.error('\n [ERRO] Entrada inválida. Por favor, digite apenas números.')
    
    return price_input

def collect_date_input() -> str:
    'receive input the expiration date'

    expiration_date_str = f'Qual a validade deste novo item? (DIA/MÊS/ANO): '
    expiration_input = input(f'{expiration_date_str}')                        
    
    if expiration_input is not None:
        pass
    else:
        logging.error(f'[ERRO] Data de validade inválida. Tente novamente.')
    
    return expiration_input

def collect_user_name() -> str:
    'this function is responsable by collect input of user_name of client'
   
    user_name = (input('\nInforme nome de usuário para cadastro (EXEMPLO: MARIA SILVA): '))
    user_name_formated = user_name.replace(' ', '')
    bool_user_name = user_name_formated.isalpha()
    
    if bool_user_name == True:
        pass
    else:
        print('\n[ERRO] O nome de usuário deve conter apenas letras. Tente novamente.')
    
    return user_name_formated

def collect_user_pin() -> str:
    'this function is an validator of string that client input send to create the password'

    pin_input = pwinput.pwinput('Informe uma senha de 4 digitos para cadastro (EXEMPLO: 1234): ')
    bool_user_pin = pin_input.isdigit()

    if bool_user_pin == True:
        pass
    else:
        logging.error('[ERRO] A senha deve conter apenas numeros. Tente novamente.')
    
    return pin_input

def collect_quantity() -> str:
    'this function receives input of the number integer to add quantity in the batch'       
    
    quantity_ask = f'Quantidade: '
    quantity_input = input(f'{quantity_ask}')

    if quantity_input is not None:
        pass
    else: 
        logging.error(f'[ERRO] Entrada inválida, insira apenas números. Tente novamente.')
   
    return quantity_input

def collect_batch_physical() -> str:
    
    batch_ask = f'Qual o lote impresso fisicamente neste item? (EX: AB123CD): '
    batch_input = input(f'{batch_ask}')
    
    print(f'O lote informado é ***{batch_input.upper()}***.')
    print(f'Você confirma que o lote ***{batch_input.upper()}*** está correto? ')
    
    batch_confirmation = input(f'Digite 1 para confirmar ou 0 para corrigir: ')

    return batch_input, batch_confirmation