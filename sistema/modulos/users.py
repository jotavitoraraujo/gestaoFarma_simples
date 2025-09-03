from hashlib import sha256
from sistema import database
from pwinput import pwinput
from sistema.modelos.user import User

def cadastro_usuario():
    print('=' * 30)
    print(' CADASTRO DE NOVO USUÁRIO')
    print('=' * 30)
    while True:
        
        nome_input = (input('\nInforme nome de usuário para cadastro (EXEMPLO: MARIA SILVA): '))
        nome_formatado = nome_input.replace(' ', '')
        
        if nome_formatado.isalpha():
            break
        else:
            print('\n[ERRO] O nome de usuário deve conter apenas letras. Tente novamente.')
            
        
    while True:
        
        pin_input = pwinput('Informe uma senha de 4 digitos para cadastro (EXEMPLO: 1234): ')
        print('-' * 10)
        pin_formatado = pin_input.isdigit()
        
        if pin_formatado is True:        
            if len(pin_input) > 4:
                print('[ERRO] A senha deve conter 4 digitos. Tente novamente.')                
            elif len(pin_input) < 4:
                print('[ERRO] A senha deve conter 4 digitos. Tente novamente.')
            else:
                print('\n[SUCESSO] Senha cadastrada.')
                break
        else:
            print('[ERRO] A senha deve conter apenas números. Tente novamente.')

    pin_bytes = pin_input.encode()
    pin_cripto = sha256(pin_bytes).hexdigest()
    name_usuario = nome_formatado
    usuario = User (
        
        user_id = None,
        user_name = name_usuario,
        user_pin = pin_cripto
        
        )
    return database.register_user(usuario)

def login():
    print('=' * 30)
    print('\n---GESTÃO FARMA SIMPLES---')
    print('=' * 30)           
    
    while True:
        usuario_input = input(f'USUÁRIO: ')
        resposta_db = database.search_user(usuario_input)
    
    
        if resposta_db == None:
            print(f'[ERRO] Usuário {usuario_input} não existe ou não é cadastrado.')           
        else:
            while True:
                pin = pwinput(f'SENHA: ')             
                pin_numeros = pin.isdigit()
                if pin_numeros is True:                        
                    if len(pin) != 4:
                        print('[ERRO] A senha deve conter 4 digitos. Tente novamente.')                   
                    else:
                        break
                else:
                    print(f'[ERRO] A senha deve conter apenas números. Tente novamente.')
        
            pin_bytes = pin.encode()
            pin_critpo = sha256(pin_bytes).hexdigest()
            
            if pin_critpo == resposta_db[2]:
                
                usuario = User(
                    user_id = resposta_db[0],
                    user_name = resposta_db[1],
                    user_pin = resposta_db[2]
                )

                print(f'\nSEJA BEM VINDO {resposta_db[1]} - GESTÃO FARMA LHE DESEJA UM BOM TRABALHO!')
                return usuario
            else:
                print(f'Senha incorreta, tente novamente.')


