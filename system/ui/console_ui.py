### --- IMPORTS --- ###
from system.services.dispatcher_service import DispatcherService
from system.models.payloads import ImportationFinishedPayload
from system.models.event_types import EventType
from system.utils import io_collectors as io
from typing import Callable, Any
from decimal import Decimal
from datetime import date
from pathlib import Path
import threading as th
import logging as log
import time as t
import sys
#######################

class ConsoleUI:
    def __init__(self, dispatcher: DispatcherService):
            self.dispatcher = dispatcher
            self.processing: bool = False
            dispatcher.subscribe(EventType.IMPORTATION_FINISHED, self._handle_importation_event)

    def _handle_importation_event(self, payload: ImportationFinishedPayload) -> None:
        'verify the instance of payload and sets the variable .processing to false'

        if isinstance(payload, ImportationFinishedPayload):
            self.processing = False

    def _wait_loop(self, side_thread: th.Thread) -> None:

        while self.processing:
            if not side_thread.is_alive():
                break

            for dots in ['. ', '.. ', '...']:
                sys.stdout.write(f'\rProcessando{dots}')
                sys.stdout.flush()
                t.sleep(0.5)

    def run_async_task(self, task_method: Callable[[Any], None], *args, **kwargs) -> None:
        'create an engine to make the terminal wait'

        log.info(f'[AGUARDE] A tarefa {task_method.__name__} está sendo processada.')
        sys.stdout.write(f'\nIniciando processamento... \n')
        self.processing = True
        side_thread: th.Thread = task_method(*args, **kwargs)
        self._wait_loop(side_thread)
        sys.stdout.write(f'\r' + ' ' * 80 + '\r')

        if not side_thread.is_alive() and self.processing:
            log.error(f'[ERRO] A importação foi interrompida inesperadamente. Comunique ao administrador.')
        else: log.info(f'[SUCESSO] A importação foi concluída com sucesso.')

    def display_submenu_reports(self) -> str | None:
        'display submenu to print the reports'

        print(' --- Sistema de Gestão da Farmácia ---')
        print('Relátorios e Indicadores')
        print('1. Faturamento Diário (Visão Analítica)')
        print('2. Faturamento Mensal (Visão Sintética)')
        print('3. Curva ABC de Produtos (Giro de Estoque)')
        print('0. Voltar')
        return input('Escolha uma opção: ')

    def display_menu(self) -> str | None:
        'display main menu'
        
        print('\n--- Sistema de Gestão da Farmácia ---')
        print('1. Importar Nota Fiscal (.XML)')
        print('2. Importar Tabela CMED (.XLSX)')
        print('3. Registrar Venda')
        print('4. Relatórios e Indicadores')
        print('5. Cadastrar Novo Usuário')
        print('0. Sair')
        return input('Escolha uma opção: ')

    def display_menu_auth(self) -> str | None:
        'display menu to authenticated in the system'

        print('\n --- Sistema de Gestão da Farmácia ---')
        print('Autenticação no Sistema')
        print('1. Login')
        print('2. Registrar')
        print('0. Sair')
        return input('Escolha uma opção: ')

    def get_file_path(self) -> Path | None:
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
            log.info(f'=' * 30)
            log.warning(f'[ERRO] O nome do arquivo não existe ou não foi encontrado. Tente novamente.')
            log.info(f'=' * 30)

    def get_username_to_register(self) -> str:

        print('=' * 30)
        print('NOME DE USUÁRIO')
        print('[ALERTA] O padrão para nomes de usuário no GestãoFarma Simples é: NOMESOBRENOME [EX: MARIASILVA]')
        print('=' * 30)
        user_name: str = io.collect_user_name()
        print('[INFO] Nome de usuário inserido com sucesso.')
        return user_name

    def get_pin_to_register(self) -> str:

        print('=' * 30)
        print('DEFINIÇÃO DE SENHA')
        print('[ALERTA] O padrão de definição de senhas do GestãoFarma Simples é: 4 digitos numéricos [EX: 1234]')
        print('=' * 30)
        pin: str = io.collect_user_pin()
        print('[INFO] Senha cadastrada com sucesso.')
        return pin

    def get_username_to_auth(self) -> str:

        print('=' * 30)
        print('--- GESTÃO FARMA LOGIN ---')
        print('=' * 30)
        user_name: str = io.collect_user_name()
        return user_name

    def get_pin_to_auth(self) -> str:

        print('\n')
        print('=' * 30)
        print('--- GESTÃO FARMA LOGIN --- ')
        pin: str = io.collect_user_pin()
        return pin
    
    def get_ean(self) -> str:

        print('=' * 30)
        print('--- GESTÃO FARMA VENDA ---')
        ean: str = io.collect_EAN()
        return ean
    
    def get_quantity(self) -> int:

        print('=' * 30)
        print('--- GESTÃO FARMA VENDA ---')
        qty: int = io.collect_quantity()
        return qty
    
    def info_sale(self, total: Decimal):

        print(f'[INFO] Total: R$ {total:.2f}')

    def get_dates(self) -> tuple[date, date] | None:

        print('=' * 30)
        print('--- GESTÃO FARMA RELATÓRIOS ---')
        print('Data Inicial | Formato: DD/MM/AAAA')
        start_date: date = io.collect_date()
        print('Data Final | Formato: DD/MM/AAAA')
        end_date: date = io.collect_date()
        return start_date, end_date