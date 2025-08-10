import logging
from pathlib import Path
caminho_arquivo_log = Path(__file__).parent.parent.parent / 'dados' / 'gestao_farma.log'

def sistema_logs():
    'cria e configura um sistema de logs, onde o usuario o enxerga no terminal e a função o registra internamente num arquivo .log'
    
    ######## ---USUARIO--- #########
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    
    terminal_controlador = logging.StreamHandler()
    terminal_formatado = logging.Formatter('%(message)s')

    terminal_controlador.setFormatter(terminal_formatado)

    logger.addHandler(terminal_controlador)

    ######## ---ARQUIVO .LOG--- #########

    arquivo_controlador = logging.FileHandler(caminho_arquivo_log, encoding = 'utf-8')
    arquivo_controlador.setLevel(logging.WARNING)

    arquivo_formatado = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(message)s')
    arquivo_controlador.setFormatter(arquivo_formatado)

    logger.addHandler(arquivo_controlador)