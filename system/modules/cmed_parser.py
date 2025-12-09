### --- IMPORTS --- ###
from system.utils import decorators as d
from pandas import DataFrame
from typing import Final
from pathlib import Path
import pandas as pd
###############################

class CMEDParser:
    def __init__(self, excel_file: Path):
        self.excel_file = excel_file
        self.CURRENT_ICMS_ZONE: Final = '18 %'
        self.COLUMNS: Final = {
            'PRODUTO': str,
            'SUBSTÂNCIA': str,
            'APRESENTAÇÃO': str,
            'CLASSE TERAPÊUTICA': str,
            'TIPO DE PRODUTO (STATUS DO PRODUTO)': str,
            'LABORATÓRIO': str,
            'EAN 1': str,
            'REGISTRO': str,
            f'PMC {self.CURRENT_ICMS_ZONE}': str 
        }

    def _to_pyarrow(self, dataframe: DataFrame) -> DataFrame:
        'transform the columns in the object more efficient in memory -> pyarrow'

        for column in self.COLUMNS.keys():
            if column in dataframe.columns:
                dataframe[column] = dataframe[column].astype('string[pyarrow]')
        return dataframe

    def _load_cmed(self) -> DataFrame:
        'load a sheet cmed of an ExcelFile to a Dataframe'

        dataframe_main: DataFrame = pd.read_excel(
            self.excel_file,
            header = 41,
            dtype = self.COLUMNS,
            usecols = list(self.COLUMNS.keys())
        )

        dataframe_main: DataFrame = self._to_pyarrow(dataframe_main)
        dataframe_clean: DataFrame = dataframe_main.dropna(subset = ['EAN 1'])
        return dataframe_clean
    
    @d.timer
    def get_dataframe(self) -> DataFrame:
        'get a already clean dataframe'

        dataframe: DataFrame = self._load_cmed()
        return dataframe