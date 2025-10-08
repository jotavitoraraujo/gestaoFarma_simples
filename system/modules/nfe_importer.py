###############################################
### --- IMPORTS --- ###
from system.modules.xml_parser import XMLParser
from typing import Callable
import logging
###############################################

class NFEImporter:
    '''
    NFEImporter is an object with single responsability
    execute the process of importation
    '''
    def __init__(self, parser: XMLParser, persistence: Callable):
        self.parser = parser
        self.persistence = persistence

    def run_import(self, xml_file_path: str):
        'starts the process of importation'
        try:
            # -- OPEN FILE
            with open(xml_file_path, encoding = 'UTF-8') as xml_file_open:
                xml_content = xml_file_open.read()
            ############################################################################### 
            # -- INSTANCIATED PARSER, EXECUTE IMPORTATIN AND GET PRODUCTS COMPLETE/INCOMPLETE AND ERROS
            parser_instance: XMLParser = self.parser(xml_content)
            parser_instance.execute_process()
            list_complete_products: list = parser_instance.get_complete_products()
            list_quarantine_products: list = parser_instance.get_quarantine_products()
            list_errors_raised: list = parser_instance.get_errors()
            ###############################################################################
            # -- SAVE THE PRODUCTS COMPLETE IN DATABASE USING DATABASE.SAVE_PRODUCTS(*ARG, COMPLETE PRODUCTS)
            if list_complete_products:
                self.persistence(list_complete_products)
                logging.info(f'[INFO] Produtos importados com sucesso!')
            else:
                logging.warning(f'[ALERTA] Nenhum produto foi importado. Verifique o log de ocorrências.')
            ###############################################################################
            # -- SAVE THE PRODUCTS INCOMPLETE IN DATABASE TABLE OF QUARANTINE USING DATABASE.SAVE_PRODUCTS_QUARANTINE
            if list_quarantine_products:
                # -> AQUI VIRÁ A FUNÇÃO QUE SALVARÁ ESSES PRODUTOS NA TABELA produtos_pendentes
                logging.warning(f'[ALERTA] Foram importados {len(list_quarantine_products)} para a quarentena. Favor completar o cadastro.')
            else:
                logging.info(f'[INFO] Nenhum produto foi enviado a quarentena.')
            ###############################################################################
            if list_errors_raised:
                logging.error(f'[ERRO] Foram detectados {len(list_errors_raised)} erros. Detalhes abaixo.')
                for index, erros in enumerate(list_errors_raised):
                    logging.error(f'[ERRO] {index}: {erros}')
            else:
                pass
            ###############################################################################
        except FileNotFoundError:
            logging.error(f'[ERRO] O Arquivo inserido não existe. Tente novamente.')
        except PermissionError:
            logging.error(f'[ERRO] O Arquivo inserido não pode ser processado devido a permissões na importação. Tente novamente.')



