### --- IMPORTS --- ###
from system.utils.exceptions import ConversionError
from pandas import DataFrame, ExcelFile, Series
from numpy import dtype
from pathlib import Path
import pandas as pd
import pyarrow as pa
import logging as log

###############################
### --- FOLDER TO TABLE --- ###
root_folder: Path = Path(__file__).parent.parent.parent
excel_folder: Path = root_folder/'data'/'cmed_table.xlsx'
excel_file: ExcelFile = ExcelFile(excel_folder)

### --- SETUP BACKEND PANDAS --- ###
pd.options.mode.dtype_backend = 'pyarrow'
###############################

def to_pyarrow(dataframe: DataFrame) -> DataFrame:

    LIST_COLUMNS: list[Series] = [
        'PRODUTO', 
        'SUBSTÂNCIA', 
        'APRESENTAÇÃO',
        'CLASSE TERAPÊUTICA',
        'TIPO DE PRODUTO (STATUS DO PRODUTO)',
        'LABORATÓRIO',
        'EAN 1',
        'REGISTRO'
    ]
    
    for column in LIST_COLUMNS:
        if column in dataframe.columns:
            dataframe[column] = dataframe[column].astype('string[pyarrow]')
    return dataframe

def load_cmed(excel_file: ExcelFile) -> DataFrame:
    
    dataframe_main: DataFrame = pd.read_excel(
        excel_file,
        header = 41,
        dtype = 
        {
            'PRODUTO': str,
            'SUBSTÂNCIA': str,
            'APRESENTAÇÃO': str,
            'CLASSE TERAPÊUTICA': str,
            'TIPO DE PRODUTO (STATUS DO PRODUTO)': str,
            'LABORATÓRIO': str,
            'EAN 1': str,
            'REGISTRO': str        
        }
    )

    dataframe_main: DataFrame = to_pyarrow(dataframe_main)
    dataframe_clean: DataFrame = dataframe_main.dropna(subset = ['EAN 1'])
    return dataframe_clean