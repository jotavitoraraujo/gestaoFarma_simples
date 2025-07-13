from hashlib import sha256
from sistema import database


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
        
        pin_input = input('Informe uma senha de 4 digitos para cadastro (EXEMPLO: 1234): ')
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
    nome_usuario = nome_formatado
    return database.inserir_usuario(nome_usuario, pin_cripto)
