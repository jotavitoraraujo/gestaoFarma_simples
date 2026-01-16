### --- IMPORTS --- ###

from system.repositories.product_repository import ProductRepository
from system.repositories.sales_repository import SalesRepository
from system.repositories.event_repository import EventRepository
from system.repositories.user_repository import UserRepository
from system.services.dispatcher_service import DispatcherService
from system.repositories.cmed_repository import CMEDRepository
from system.services.pricing_service import PricingService
from system.services.product_service import ProductService
from system.services.sales_service import SalesService
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
    'main menu'
    try:
        with database.connect_db() as connection_start:
            database.starter_schema(connection_start)
            
        user_auth = None
        while user_auth is None:
            dispatcher = DispatcherService()
            ui = ConsoleUI(dispatcher)
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
            print(user_auth)
            print(user_auth.user_id)
            print(user_auth.user_name)
            dispatcher = DispatcherService()
            ui = ConsoleUI(dispatcher)
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

            elif choice == '3':
                with database.connect_db() as connection_sales:
                    event_repo_sales = EventRepository(connection_sales)
                    prod_repo_sales = ProductRepository(connection_sales)
                    prod_service_sales = ProductService(prod_repo_sales, event_repo_sales)
                    sales_repo = SalesRepository(connection_sales)
                    sales_service = SalesService(prod_service_sales, sales_repo, dispatcher)
                    sales_service.start_new_sale()

                    while True:
                        ean_code: str = ui.get_ean()
                        if ean_code is None: break
                        qty: int = ui.get_quantity()
                        try:
                            sales_service.add_item(ean_code, qty)
                            ui.info_sale(sales_service.get_total())
                        except Exception as error:
                            log.warning(f'[ALERTA] O Produto buscado não possui estoque ou não existe. Tente novamente')
                            log.warning(f'[MOTIVO] {error}')
                    
                    if sales_service.cart:
                        sales_service.finish_sale(user_auth.user_id)
                        log.info(f'[INFO] Venda finalizada com sucesso!')
                    else: log.info(f'[INFO] Venda cancelada: Nenhum item adicionado.')

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