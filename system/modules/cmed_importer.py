### --- IMPORTS --- ###
from system.modules.cmed_parser import CMEDParser
from pandas import DataFrame
from typing import Callable, Any
from pathlib import Path
import logging as log
#######################

class CMEDImporter:
    def __init__(self, parser: type[CMEDParser], save_cmed: Callable[[Any], None]):
        'CMEDImporter depending on your persistence strategy, he accepts a callable'
        self.parser = parser
        self.save_cmed = save_cmed

    def run_import(self, cmed_file_path: Path) -> None:
        'start the importation of cmed table'

        try:
            parser_instance: CMEDParser = self.parser(cmed_file_path)
            dataframe: DataFrame = parser_instance.get_dataframe()
            self.save_cmed(dataframe.to_sql, dataframe)
            log.info(f'[INFO] Tabela CMED importada com sucesso! {cmed_file_path.name}')

        except Exception as error:
            log.error(f'[ERRO] Falha na importação da CMED.')
            log.error(f'[ERRO] Algo inexperado aconteceu. Contate o Administrador ou tente novamente.')
            log.error(f'[ERRO] Causa raiz: {error}')
            raise error