###############################################
### --- IMPORTS --- ###
from system.services.dispatcher_service import DispatcherService
from system.services.pricing_service import PricingService
from system.models.payloads import QuarantinePayload
from system.models.event_types import EventType
from system.models.audit_event import AuditEvent
from system.modules.xml_parser import XMLParser
from system.models.product import Product
from decimal import Decimal
from typing import Callable
from pathlib import Path
import logging
###############################################

class NFEImporter:
    '''
    NFEImporter is an object with single responsability
    execute the process of importation
    '''
    def __init__(self, xml_parser: XMLParser, dispatcher: type[DispatcherService], pricing: type[PricingService], save_prod: Callable):
        self.xml_parser = xml_parser
        self.dispatcher = dispatcher
        self.pricing = pricing
        self.save_prod = save_prod

    def _hashmap_temp(self, products: list[Product]) -> dict[str, Product] | None:

        if not products:
            return None
        
        product_map: dict[str, Product] = {prod.ean: prod for prod in products}
        return product_map

    def _apply_pricing_rules(self, products: list[Product]) -> None:
        '''Enriches the product objects with the calculated sale price via PricingService.
        This operation happens in-memory (Reference Update)'''

        if not products:
            return None
        
        data: list[dict] = self.pricing.price_all_prod(products)
        product_map: dict[str, Product] = self._hashmap_temp(products)

        for result in data:
            ean: str = result['ean']
            final_price: Decimal = result['final_price']

            if ean in product_map.keys():
                product_map[ean].sale_price = final_price

                if result.get('capped'):
                    logging.warning(f'[PRECIFICAÇÃO] O EAN: {ean} teve o preço teto aplicado: R$ {final_price}')


    def run_import(self, xml_file_path: Path):
        'starts the process of importation'
        
        try:
            with open(xml_file_path, encoding = 'UTF-8') as xml_file_open:
                xml_content = xml_file_open.read()

            parser_instance: XMLParser = self.xml_parser(xml_content)
            parser_instance.execute_process()
            list_complete_products: list[Product] = parser_instance.get_products()
            list_errors_raised: list = parser_instance.get_errors()

            if list_complete_products:
                
                try:
                    self._apply_pricing_rules(list_complete_products)
                    logging.info(f'[PRECIFICAÇÃO] Precificação automática aplicada para {len(list_complete_products)} itens.')
                except Exception as error:
                    logging.error(f'[PRICING CRITICAL] Failed to calculate prices. Products will be saved without a price. Error: {error}')

                result: tuple = self.save_prod(list_complete_products)
                status_count: dict = result[0]
                list_payloads: list[AuditEvent] = result[1]
                
                for audit_event in list_payloads:
                    payload: QuarantinePayload = audit_event.payload
                    self.dispatcher.publish(EventType.QUARANTINE, payload)
                
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



