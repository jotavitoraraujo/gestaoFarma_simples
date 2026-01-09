### --- IMPORTS --- ###

from system.repositories.product_repository import ProductRepository
from system.repositories.event_repository import EventRepository
from system.repositories.user_repository import UserRepository
from system.services.dispatcher_service import DispatcherService
from system.repositories.cmed_repository import CMEDRepository
from system.services.pricing_service import PricingService
from system.services.product_service import ProductService
from system.modules.cmed_importer import CMEDImporter
from system.services.auth_service import AuthService
from system.modules.nfe_importer import NFEImporter
from system.modules.cmed_parser import CMEDParser
from system.modules.xml_parser import XMLParser
from system.models.event_types import EventType
from system.ui.console_ui import ConsoleUI
from system.modules import settings_log
from system.models.user import User
from system import database
from typing import Callable
from pathlib import Path
import logging as log
######################################################

def main():
    settings_log.log_system()
    dispatcher = DispatcherService()
    ui = ConsoleUI(dispatcher)
    'main menu'
    try:
        with database.connect_db() as connection_start:
            database.starter_schema(connection_start)
            
        user_auth = None
        while user_auth is None:
            choice = ui.display_menu_auth()
            if choice == '1':
                with database.connect_db() as connection_auth:
                    user_repo_login = UserRepository(connection_auth)
                    auth_service_login = AuthService(user_repo_login)
                    user_name: str = ui.get_username_to_auth()
                    pin: str = ui.get_pin_to_auth()
                    user_auth: User = auth_service_login.authenticate(user_name, pin)
                    if user_auth is not None:
                        print('=' * 30)
                        log.info(f'[INFO] Seja bem vindo {user_auth.user_name}, tenha um bom trabalho!')
                        print('=' * 30)
                        break
                    else:
                        log.warning('[ALERTA] Nome de usuário ou PIN incorretos. Tente novamente.')
            
            if choice == '2':
                with database.connect_db() as connection_register:
                    user_repo_register = UserRepository(connection_register)
                    auth_service_register = AuthService(user_repo_register)
                    user_name: str = ui.get_username_to_register()
                    pin: str = ui.get_pin_to_register()
                    auth_service_register.register(user_name, pin)
            
            if choice == '0':
                log.info('=' * 30)
                log.info('[INFO] Sistema finalizado.')
                log.info('=' * 30)
                break
    
        while user_auth is not None:
            choice = ui.display_menu()
            if choice == '1':
                with database.connect_db() as connection_import_nfe:                      
                    event_repo_import = EventRepository(connection_import_nfe)
                    cmed_repo_import = CMEDRepository(connection_import_nfe)
                    prod_repo_import = ProductRepository(connection_import_nfe)
                    prod_service = ProductService(prod_repo_import, event_repo_import)
                    dispatcher.subscribe(EventType.QUARANTINE, prod_service.handle_quarantine_event)
                    pricing = PricingService(cmed_repo_import)
                    importer = NFEImporter(XMLParser, dispatcher, pricing, prod_repo_import.save_products)
                    xml_path: str = ui.get_file_path()
                    if xml_path is not None:
                        importer.run_import(xml_path)
            
            elif choice == '2':
                with database.connect_db() as connection_import_cmed:
                    cmed_repo = CMEDRepository(connection_import_cmed)
                    save_cmed: Callable = cmed_repo.save_cmed
                    cmed_path: Path = ui.get_file_path()
                    if cmed_path is not None:
                        importer = CMEDImporter(CMEDParser, dispatcher, save_cmed)
                        ui.run_async_task(importer.run_import, cmed_path)

            elif choice == '0':
                log.info('=' * 30)
                log.info('[INFO] Sistema finalizado.')
                log.info('=' * 30)
                break
    ######################################################
            else:
                log.error('[ERRO] Opção inválida. Tente novamente')
    ######################################################
    except Exception as error:
        log.error(f'[FATAL ERROR] :: Ocorreu um erro inesperado e a operação não pode ser concluída. O programa será finalizado.')
        log.error(f'[FATAL ERROR] :: Verifique o log de erros para mais detalhes. {error}')
######################################################
if __name__ == '__main__':
    main()