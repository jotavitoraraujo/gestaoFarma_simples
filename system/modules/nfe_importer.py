###############################################
### --- IMPORTS --- ###
from system.services.dispatcher_service import DispatcherService
from system.models.payloads import QuarantinePayLoad
from system.models.event_types import EventType
from system.models.audit_event import AuditEvent
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
    def __init__(self, parser: XMLParser, service: DispatcherService, save_prod: Callable):
        self.parser = parser
        self.service = service
        self.save_prod = save_prod

    def run_import(self, xml_file_path: str):
        'starts the process of importation'
        
        try:
            with open(xml_file_path, encoding = 'UTF-8') as xml_file_open:
                xml_content = xml_file_open.read()

            parser_instance: XMLParser = self.parser(xml_content)
            parser_instance.execute_process()
            list_complete_products: list[Product] = parser_instance.get_products()
            list_errors_raised: list = parser_instance.get_errors()

            if list_complete_products:
                result: tuple = self.save_prod(list_complete_products)
                status_count: dict = result[0]
                list_payloads: list[AuditEvent] = result[1]
                
                for audit_event in list_payloads:
                    payload: QuarantinePayLoad = audit_event.payload
                    self.service.publish(EventType.QUARANTINE, payload)
                
                logging.info(f'=' * 30)
                logging.info(f'[INFO] O processo de importação foi concluido com sucesso!')
                logging.info(f'=' * 30)
                logging.info(f'[INFO] {len(list_complete_products)} produtos foram importados.')
                logging.info(f'=' * 30)
                logging.warning(f'[INFO] {status_count['ACTIVE']} produto(s) estão com status *ATIVOS*.')
                logging.warning(f'[INFO] {status_count['QUARANTINE']} produto(s) estão com status *QUARENTENA*.')
                logging.info(f'=' * 30)
                
                if status_count['QUARANTINE'] > 0:
                    logging.warning(f'[ALERTA] O sistema recomenda verificar a integridade dos dados dos produtos em Quarentena.')
            else:
                logging.warning(f'[ALERTA] Nenhum produto foi importado. Verifique o log de ocorrências.')
            
            if list_errors_raised:
                logging.error(f'[ERRO] Foram detectados {len(list_errors_raised)} erros. Detalhes abaixo.')
                for index, erros in enumerate(list_errors_raised):
                    logging.error(f'[ERRO] {index}: {erros}')
            else:
                pass
            
        except FileNotFoundError:
            logging.error(f'[ERRO] O Arquivo inserido não existe. Tente novamente.')
        except PermissionError:
            logging.error(f'[ERRO] O Arquivo inserido não pode ser processado devido a permissões na importação. Tente novamente.')



