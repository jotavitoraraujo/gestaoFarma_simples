### --- IMPORTS --- ###
from sqlite3 import Connection
from sistema import database, security
from sistema.modulos import validators
from sistema.modelos.user import User

def register_user():
    print('=' * 30)
    print(' CADASTRO DE NOVO USUÁRIO')
    print('=' * 30)
           
    user_name = validators.collect_user_name()
    user_pin = validators.collect_user_pin()
    
    if isinstance(user_pin, str):
        bool = validators.password_length_validator(user_pin)
        
        if bool == True:
            pin_hash = security.password_for_hash(user_pin)
            
            user_instance = User(
                user_id = None,
                user_name = user_name,
                user_pin = pin_hash
            )
            
            connect_db: Connection = database.connect_db()
            database.register_user_database(connect_db, user_instance)

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
                #pin = pwinput(f'SENHA: ')             
                #pin_numeros = pin.isdigit()
                #if pin_numeros is True:                        
                    #if len(pin) != 4:
                        print('[ERRO] A senha deve conter 4 digitos. Tente novamente.')                   
                    #else:
                        break
                #else:
                    #print(f'[ERRO] A senha deve conter apenas números. Tente novamente.')
        
            #pin_bytes = pin.encode()
            #pin_critpo = sha256(pin_bytes).hexdigest()
            
            #if pin_critpo == resposta_db[2]:
                
                #usuario = User(
                #    user_id = resposta_db[0],
                #    user_name = resposta_db[1],
                #    user_pin = resposta_db[2]
                #)

                #print(f'\nSEJA BEM VINDO {resposta_db[1]} - GESTÃO FARMA LHE DESEJA UM BOM TRABALHO!')
                #return usuario
            else:
                print(f'Senha incorreta, tente novamente.')


