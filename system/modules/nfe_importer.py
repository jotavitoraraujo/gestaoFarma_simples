###############################################
### --- IMPORTS --- ###
from system.modules.xml_parser import XMLParser
from system.models.product import Product
from typing import Callable
import logging
###############################################

class NFEImporter:
    '''
    NFEImporter is an object with single responsability
    execute the process of importation
    '''
    def __init__(self, object_parser: XMLParser, repo_save_products: Callable):
        self.object_parser = object_parser
        self.repo_save_products = repo_save_products

    def run_import(self, xml_file_path: str):
        'starts the process of importation'
        try:
            # -- OPEN FILE
            with open(xml_file_path, encoding = 'UTF-8') as xml_file_open:
                xml_content = xml_file_open.read()
            ############################################################################### 
            # -- INSTANCIATED PARSER, EXECUTE IMPORTATIN AND GET PRODUCTS COMPLETE/INCOMPLETE AND ERROS
            parser_instance: XMLParser = self.object_parser(xml_content)
            parser_instance.execute_process()
            list_complete_products: list[Product] = parser_instance.get_products()
            list_errors_raised: list = parser_instance.get_errors()
            ###############################################################################
            # -- SAVE THE PRODUCTS COMPLETE IN DATABASE USING DATABASE.SAVE_PRODUCTS(*ARG, COMPLETE PRODUCTS)
            if list_complete_products:
                ######################################################
                dict_status: dict = self.repo_save_products(list_complete_products)
                ######################################################
                logging.info(f'=' * 30)
                logging.info(f'[INFO] O processo de importação foi concluido com sucesso!')
                logging.info(f'=' * 30)
                logging.info(f'[INFO] {len(list_complete_products)} produtos foram importados.')
                logging.info(f'=' * 30)
                logging.warning(f'[INFO] {dict_status['ACTIVE']} produto(s) estão com status *ATIVOS*.')
                logging.warning(f'[INFO] {dict_status['QUARANTINE']} produto(s) estão com status *QUARENTENA*.')
                logging.info(f'=' * 30)
                ######################################################
                if dict_status['QUARANTINE'] > 0:
                    logging.warning(f'[ALERTA] O sistema recomenda verificar a integridade dos dados dos produtos em Quarentena.')
            else:
                logging.warning(f'[ALERTA] Nenhum produto foi importado. Verifique o log de ocorrências.')
            ###############################################################################
            if list_errors_raised:
                logging.error(f'[ERRO] Foram detectados {len(list_errors_raised)} erros. Detalhes abaixo.')
                ######################################################
                for index, erros in enumerate(list_errors_raised):
                    logging.error(f'[ERRO] {index}: {erros}')
            else:
                pass
            ###############################################################################
        except FileNotFoundError:
            logging.error(f'[ERRO] O Arquivo inserido não existe. Tente novamente.')
        except PermissionError:
            logging.error(f'[ERRO] O Arquivo inserido não pode ser processado devido a permissões na importação. Tente novamente.')



