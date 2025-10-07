### --- IMPORTS --- ###
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
    xml_file: Path = root_folder/'data'/f'{name_xml}'
    if xml_file.exists():
        xml_file = str(xml_file)
        logging.info(f'[INFO] Arquivo importado com sucesso.')
        return xml_file
    else:
        logging.error(f'[ERRO] O nome do arquivo não existe ou não foi encontrado. Tente novamente.')