### --- IMPORTS --- ###
from datetime import date
from system.utils import converters, validators
import logging
import pwinput


### --- INPUT/OUTPUT COLLECTORS FUNCTIONS --- ###

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
                return price_input
            
            elif ask_menu_input == '2' or ask_menu_option == '2':
                ask_date = f'[ALERTA] Insira a data de validade impressa no item: EX: (DD/MM/AAAA)'
                expiration_date_input = input(f'{ask_date}')
                return expiration_date_input
                
            elif ask_menu_input == '3' or ask_menu_option == '3':
                ask_user_name = f'[ALERTA] Insira o nome de usuário: '
                user_name_input = input(f'{ask_user_name}')
                return user_name_input

            elif ask_menu_input == '4' or ask_menu_option == '4':
                ask_pin = f'[ALERTA] Insira o PIN de 4 digitos: '
                pin_input = (f'{ask_pin}')
                return pin_input
                
            elif ask_menu_input == '5' or ask_menu_option == '5':
                ask_quantity = f'[ALERTA] Insira a quantidade deste item: '
                quantity_input = input(f'{ask_quantity}')
                return quantity_input
            
            elif ask_menu_input == '6' or ask_menu_option == '6':
                ask_pyshical_batch = f'[ALERTA] Insira o Lote Fisico impresso neste item: '
                physical_batch_input = input(f'{ask_pyshical_batch}')
                result = str(input(
                f'''
                [ALERTA] O Lote Fisico informado é {physical_batch_input.upper()}. 
                \n1. Confirmar
                \n0. Corrigir
                \nSelecione uma opção: 
                '''
                ))
                if result != '0':
                    return physical_batch_input
            
            elif ask_menu_input == '0' or ask_menu_option == '0':
                    logging.info(f'[INFO] Saindo do Menu...')
                    break
            else:
                logging.error(f'[ERRO] Opção inválida. Tente novamente.')
    else:
        logging.error(f'[ERRO] O valor inserido não é valido ou está corrompido.')
        return None