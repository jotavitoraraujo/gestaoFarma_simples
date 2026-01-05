### --- IMPORTS --- ###
from system.utils import decorators as d
from sqlite3 import Connection, Cursor, sqlite_version_info
from typing import Callable, Any, Final
from pandas import DataFrame
from decimal import Decimal
from collections.abc import Iterator
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

    def _get_pmc_chunk(self, chunk: list[str]) -> list[tuple[str, Decimal] | None]:
        'get pmc from table CMED'

        cursor: Cursor = self.connection_db.cursor()
        placeholders: str = ', '.join(['?'] * len(chunk))
        query: str = (f'''
            SELECT "EAN 1", "PMC 18 %"
            FROM cmed_table
            WHERE "EAN 1" IN ({placeholders})
        ''')
        cursor.execute(query, chunk)
        result: list[tuple] = cursor.fetchall()
        clean_result: list[tuple[str, Decimal]] = [(ean, Decimal(f'{price}')) for ean, price in result if price is not None]
        return clean_result
    
    def get_pmc_map_by_eans(self, ean_list: list[str]) -> dict[str, Decimal]:
        'get pmc using a chunk of the list of eans provides by database'

        version_db: tuple[int, int, int] = self._get_version_db()
        chunksize: int = self._define_chunksize(version_db)
        fullmap: dict[str, Decimal] = {}
        
        for ean in range(0, len(ean_list), chunksize): 
            chunk = ean_list[ean: ean + chunksize]
            if chunk: 
                list_pmc: list[tuple[str, Decimal]] = self._get_pmc_chunk(chunk)
                fullmap.update(dict(list_pmc))
        
        return fullmap

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