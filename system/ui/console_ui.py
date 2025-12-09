### --- IMPORTS --- ###
from system.utils import io_collectors as io
from pathlib import Path
import pwinput
import logging
#######################

# PURE FUNCTION

def display_menu() -> str | None:
    'Exibe o menu principal e retorna a escolha do usuário.'
    print('\n--- Sistema de Gestão da Farmácia ---')
    print('1. Importar Nota Fiscal (.XML)')
    print('2. Importar Tabela CMED (.XLSX)')
    print('3. Registrar Venda')
    print('4. Ver Relátorios')
    print('5. Cadastrar Novo Usuário')
    print('0. Sair')
    return input('Escolha uma opção: ')

def display_menu_auth() -> str | None:
    'display menu to authenticated in the system'

    print('\n --- Sistema de Gestão da Farmácia ---')
    print('Autenticação no Sistema')
    print('1. Login')
    print('2. Registrar')
    print('0. Sair')
    return input('Escolha uma opção: ')

def get_file_path() -> Path | None:
    'get the path of a file by an input from user'
    
    print('=' * 30)
    print('[INFO] Por favor insira o nome do arquivo abaixo. [EXEMPLO]: nome_arquivo.xml | nome_arquivo.xlsx')
    print('=' * 30)
    file_name: str = input('[INFO] Arquivo: ')
    root_folder: Path = Path(__file__).parent.parent.parent #### FROM .PY -> GO TO UI FOLDER -> GO TO SYSTEM -> GET TO THE ROOT FOLDER
    file_path: Path = root_folder/'data'/f'{file_name}'
    if file_path.exists():
        return file_path
    else:
        logging.info(f'=' * 30)
        logging.warning(f'[ERRO] O nome do arquivo não existe ou não foi encontrado. Tente novamente.')
        logging.info(f'=' * 30)

def get_username_to_register() -> str:
    
    print('=' * 30)
    print('NOME DE USUÁRIO')
    print('[ALERTA] O padrão para nomes de usuário no GestãoFarma Simples é: NOMESOBRENOME [EX: MARIASILVA]')
    print('=' * 30)
    user_name: str = io.collect_user_name()
    print('[INFO] Nome de usuário inserido com sucesso.')
    return user_name

def get_pin_to_register() -> str:

    print('=' * 30)
    print('DEFINIÇÃO DE SENHA')
    print('[ALERTA] O padrão de definição de senhas do GestãoFarma Simples é: 4 digitos numéricos [EX: 1234]')
    print('=' * 30)
    pin: str = io.collect_user_pin()
    print('[INFO] Senha cadastrada com sucesso.')
    return pin

def get_username_to_auth() -> str:

    print('=' * 30)
    print('--- GESTÃO FARMA LOGIN ---')
    print('=' * 30)
    user_name: str = io.collect_user_name()
    return user_name

def get_pin_to_auth() -> str:

    print('\n')
    print('=' * 30)
    print('--- GESTÃO FARMA LOGIN --- ')
    pin: str = io.collect_user_pin()
    return pin