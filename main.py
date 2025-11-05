### --- IMPORTS --- ###
from system.repositories.product_repository import ProductRepository
from system.repositories.event_repository import EventRepository
from system.repositories.user_repository import UserRepository
from system.services.auth_service import AuthService
from system.modules.nfe_importer import NFEImporter
from system.modules.xml_parser import XMLParser
from system.modules import settings_log
from system.models.user import User
from system.ui import console_ui
from system import database
import logging
######################################################
def display_menu():
    'Exibe o menu principal e retorna a escolha do usuário.'
    print('\n--- Sistema de Gestão da Farmácia ---')
    print('1. Importar Nota Fiscal (XML)')
    print('2. Registrar Venda')
    print('3. Ver Relátorios')
    print('4. Cadastrar Novo Usuário')
    print('0. Sair')
    return input('Escolha uma opção: ')
######################################################

def main():
    settings_log.log_system()
    'main menu'
    try:
        ######################################################
        with database.connect_db() as connection_start:
            database.starter_schema(connection_start)
            # event_repo = EventRepository(connection)
        #     prod_repo = ProductRepository(connection, event_repo)
        #     user_repo = UserRepository(connection)
        #     auth_service = AuthService (user_repo)
        #     importer = NFEImporter(XMLParser, prod_repo.save_products)
        ######################################################
            
        user_auth = None
        while user_auth is None:
            choice = console_ui.display_menu_auth()
            if choice == '1':
                with database.connect_db() as connection_auth:
                    user_repo_login = UserRepository(connection_auth)
                    auth_service_login = AuthService(user_repo_login)
                    user_name: str = console_ui.get_username_to_auth()
                    pin: str = console_ui.get_pin_to_auth()
                    user_auth: User = auth_service_login.authenticate(user_name, pin)
                    if user_auth is not None:
                        print('=' * 30)
                        logging.info(f'[INFO] Seja bem vindo {user_auth.user_name}, tenha um bom trabalho!')
                        print('=' * 30)
                        break
                    else:
                        logging.warning('[ALERTA] Nome de usuário ou PIN incorretos. Tente novamente.')
            
            if choice == '2':
                with database.connect_db() as connection_register:
                    user_repo_register = UserRepository(connection_register)
                    auth_service_register = AuthService(user_repo_register)
                    user_name: str = console_ui.get_username_to_register()
                    pin: str = console_ui.get_pin_to_register()
                    auth_service_register.register(user_name, pin)
            
            if choice == '0':
                logging.info('=' * 30)
                logging.info('[INFO] Sistema finalizado.')
                logging.info('=' * 30)
                break
    
        while user_auth is not None:
            choice = display_menu()
            if choice == '1':
                with database.connect_db() as connection_import:    
                    event_repo_import = EventRepository(connection_import)
                    prod_repo_import = ProductRepository(connection_import, event_repo_import)
                    importer = NFEImporter(XMLParser, prod_repo_import.save_products)
                    xml_path: str = console_ui.get_xml_path()
                    if xml_path is not None:
                        importer.run_import(xml_path)
    ######################################################
            # elif escolha == '2':
            #     item = sales.adicionar_item()
            #     if item is not None:
            #         pass
            #     else:
            #         logging.error('[ERRO] Nenhum item encontrado. Tente novamente.' )
    ######################################################
            # elif escolha == '3':
            #     print('\n [INFO] Função de relátorios ainda não implementada.')
    ######################################################
            # elif choice == '4':
            #     user_name: str = console_ui.get_username()
            #     pin: str = console_ui.get_pin()
            #     auth_service.register(user_name, pin)
    ######################################################
            elif choice == '0':
                logging.info('=' * 30)
                logging.info('[INFO] Sistema finalizado.')
                logging.info('=' * 30)
                break
    ######################################################
            else:
                logging.error('[ERRO] Opção inválida. Tente novamente')
    ######################################################
    except Exception as error:
        logging.error(f'[FATAL ERROR] :: Ocorreu um erro inesperado e a operação não pode ser concluída. O programa será finalizado.')
        logging.error(f'[FATAL ERROR] :: Verifique o log de erros para mais detalhes. {error}')
######################################################
if __name__ == '__main__':
    main()