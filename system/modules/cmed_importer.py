### --- IMPORTS --- ###
from system.services.dispatcher_service import DispatcherService
from system.models.payloads import ImportationFinishedPayload
from system.modules.cmed_parser import CMEDParser
from system.models.audit_event import AuditEvent
from system.models.event_types import EventType
from system.utils import decorators as d
from datetime import datetime
from pandas import DataFrame
from typing import Callable, Any
from pathlib import Path
import logging as log
#######################

class CMEDImporter:
    def __init__(self, parser: type[CMEDParser], dispatcher: type[DispatcherService], save_cmed: Callable[[Any], None]):
        'CMEDImporter depending on your persistence strategy, he accepts a callable'
        self.parser = parser
        self.dispatcher = dispatcher
        self.save_cmed = save_cmed
    
    def _create_audit_event(self, cmed_file_path: str, dataframe: DataFrame) -> AuditEvent:

        event = AuditEvent (
            id = None,
            timestamp = datetime.now(),
            event_type = EventType.IMPORTATION_FINISHED,
            payload = ImportationFinishedPayload (
                status = 'SUCESS',
                file_name = cmed_file_path.__name__,
                total_records = len(dataframe)
            )
        )
        return event

    @d.run_background
    def run_import(self, cmed_file_path: Path) -> None:
        'start the importation of cmed table'

        try:
            parser_instance: CMEDParser = self.parser(cmed_file_path)
            dataframe: DataFrame = parser_instance.get_dataframe()
            self.save_cmed(dataframe.to_sql, dataframe)
            event: AuditEvent = self._create_audit_event(cmed_file_path, dataframe)
            self.dispatcher.publish(event.event_type, event.payload)
            log.info(f'[STATUS] Importação finalizada no backend para: {cmed_file_path.name}')

        except Exception as error:
            log.error(f'[ERRO] Falha na importação da CMED.')
            log.error(f'[ERRO] Algo inexperado aconteceu. Contate o Administrador ou tente novamente.')
            log.error(f'[ERRO] Causa raiz: {error}')
            raise error