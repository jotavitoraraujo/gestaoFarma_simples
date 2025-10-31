### --- IMPORTS --- ###
from system.utils import io_collectors as io
from pathlib import Path
import logging
#######################

# PURE FUNCTION
def get_xml_path() -> str | None:
    'get the path of a xml file by an input from user'
    
    print('=' * 30)
    print('[INFO] Por favor insira o nome do arquivo .xml abaixo. [EXEMPLO]: nome_arquivo.xml')
    print('=' * 30)
    name_xml: str = input('[INFO] Arquivo: ')
    root_folder: Path = Path(__file__).parent.parent.parent #### FROM .PY -> GO TO UI FOLDER -> GO TO SYSTEM -> GET TO THE ROOT FOLDER
    xml_file_path: Path = root_folder/'data'/f'{name_xml}'
    if xml_file_path.exists():
        xml_file_path = str(xml_file_path)
        return xml_file_path
    else:
        logging.info(f'=' * 30)
        logging.warning(f'[ERRO] O nome do arquivo não existe ou não foi encontrado. Tente novamente.')
        logging.info(f'=' * 30)

def get_username() -> str:

    user_name: str = io.collect_user_name()
    if user_name:
        print('[INFO] Nome de usuário inserido com sucesso.')
        return user_name

def get_pin() -> str:

    pin: str = io.collect_user_pin()
    if pin:
        print('[INFO] Senha cadastrada com sucesso.')
        return pin



    

