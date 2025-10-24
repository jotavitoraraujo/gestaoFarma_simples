### --- IMPORTS --- ###
from system.repositories.product_repository import ProductRepository
from system.repositories.event_repository import EventRepository
from system.modules.nfe_importer import NFEImporter
from system.modules.xml_parser import XMLParser
from system.modules import settings_log
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
        with database.connect_db() as connection:
            database.starter_schema(connection)
            event_repo = EventRepository(connection)
            prod_repo = ProductRepository(connection, event_repo)
            importer = NFEImporter(XMLParser, prod_repo.save_products)
        ######################################################   
            while True:
                choice = display_menu()
                
                if choice == '1':
                    xml_path = console_ui.get_xml_path()            
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
                # elif escolha == '4':
                #     #users.register_user(connect_db)            
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