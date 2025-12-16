### --- IMPORTS --- ###
from system.utils import decorators as d
from sqlite3 import Connection, sqlite_version_info
from typing import Callable, Any, Final
from pandas import DataFrame
#######################

class CMEDRepository:
    def __init__(self, connection_db: Connection):
        self.connection_db = connection_db

    def _get_version_db(self) -> tuple[int, int, int]:
        'get the version of database installed on system'

        version: tuple[int, int, int] = sqlite_version_info
        return version

    def _define_chunksize(self, version_db: tuple[int, int, int]) -> int:
        'define the quantity of variables is loaded with based in the version db'

        if version_db >= (3, 32, 0):
            MAX_VARS: Final[int] = 32766
            return MAX_VARS
        else: 
            MAX_VARS: Final[int] = 999
            return MAX_VARS
        
    def _get_column_number(self, dataframe: DataFrame) -> int | None:
        'get length of the columns in dataframe and return this value as an integer'

        if dataframe is not None and len(dataframe.columns) > 0:
            result: int = len(dataframe.columns)
            return result
        
        else: return None

    def _calculate_chunksize(self, dataframe: DataFrame) -> int:
        'calculate the quantity of lines a chunk can load'

        version: tuple[int, int, int] = self._get_version_db()
        MAX_VARS: Final[int] = self._define_chunksize(version)
        column_number: int = self._get_column_number(dataframe)

        ### --- FORMULA = CHUNKSIZE = MAX VARIABLES // COLUMN NUMBER --- ###
        if column_number is None or column_number == 0:
            chunksize: int = 500
            return chunksize
        else: 
            chunksize: int = MAX_VARS // column_number
            return chunksize

    @d.timer
    def save_cmed(self, persist_method: Callable[[Any], None] = None, dataframe: DataFrame = None) -> None:
        'this function uses the persist method of your choice to save in db, currently df.tosql()'

        chunksize: int = self._calculate_chunksize(dataframe)
        persist_method(
            name = 'cmed_table',
            con = self.connection_db,
            if_exists = 'replace',
            chunksize = chunksize,
            index = False
        )

