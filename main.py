### --- IMPORTS --- ###
from system.modules.xml_parser import XMLParser
from system.modules.nfe_importer import NFEImporter
from system.ui import console_ui
from system import database
import logging



def display_menu():
    'Exibe o menu principal e retorna a escolha do usuário.'
    print('\n--- Sistema de Gestão da Farmácia ---')
    print('1. Importar Nota Fiscal (XML)')
    print('2. Registrar Venda')
    print('3. Ver Relátorios')
    print('4. Cadastrar Novo Usuário')
    print('0. Sair')
    return input('Escolha uma opção: ')
    

def main():
    'main menu'
    with database.connect_db() as connection:
        database.create_tables(connection)
        while True:
            choice = display_menu()
            
            if choice == '1':
                persistence_func = lambda list: database.save_products(connection, list)
                importer = NFEImporter(XMLParser, persistence_func)
                xml_path = console_ui.get_xml_path()            
                if xml_path is not None:
                    importer.run_import(xml_path)
                else:
                    logging.warning(f'[ALERTA] O XML fornecido não foi encontrado ou não existe. Tente novamente.')
        
        # elif escolha == '2':
        #     item = sales.adicionar_item()
        #     if item is not None:
        #         pass
        #     else:
        #         logging.error('[ERRO] Nenhum item encontrado. Tente novamente.' )            
        
        # elif escolha == '3':
        #     print('\n [INFO] Função de relátorios ainda não implementada.')
       
        # elif escolha == '4':
        #     #users.register_user(connect_db)            
       
        # elif escolha == '0':
        #     logging.info('\n[INFO] Sistema finalizado.')
        #     break
       
        # else:
        #     logging.error('\n [ERRO] Opção inválida. Tente novamente')

if __name__ == '__main__':
    main()