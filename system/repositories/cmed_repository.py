### --- IMPORTS --- ###
from sqlite3 import Connection, Cursor, sqlite_version_info
from typing import Callable, Any, Final
from pandas import DataFrame
from decimal import Decimal
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

    def _get_pmc_chunk(self, chunks_ean: list[str]) -> list[tuple]:
        'get pmc from table CMED'

        cursor: Cursor = self.connection_db.cursor()
        placeholders: str = ', '.join(['?'] * len(chunks_ean))
        query: str = (f'''
            SELECT "EAN 1", "PMC 18 %", "TIPO DE PRODUTO (STATUS DO PRODUTO)"
            FROM cmed_table
            WHERE "EAN 1" IN ({placeholders})
        ''')
        cursor.execute(query, chunks_ean)
        result: list[tuple] = cursor.fetchall()
        return result
        
    def _cleaning(self, result: list[tuple]) -> list[tuple[str, Decimal, str]] | None:
        'clean the result from the db'

        clean_result: list[tuple[str, Decimal, str]] = [   
            (
                str(ean), 
                Decimal(str(pmc.replace(',', '.'))), 
                str(prod_type) if prod_type is not None else 'DEFAULT'
            ) 
            for ean, pmc, prod_type in result
        ]
        if clean_result: return clean_result
        else: return []
    
    def get_pmc_map_by_eans(self, ean_list: list[str]) -> dict[str, tuple[Decimal, str]]:
        'get pmc using a chunk of the list of eans provides by database'

        version_db: tuple[int, int, int] = self._get_version_db()
        chunksize: int = self._define_chunksize(version_db)
        fullmap_pmc: dict[str, tuple[Decimal, str]] = {}
        
        for ean in range(0, len(ean_list), chunksize):
            chunks_ean: list[str] = ean_list[ean: ean + chunksize]
            if chunks_ean: 
                result: list[tuple] = self._get_pmc_chunk(chunks_ean)
                list_ean: list[tuple[str, Decimal, str]] | None = self._cleaning(result)
                pmc_map: dict[str[Decimal, str]] = {ean: (pmc, prod_type) for ean, pmc, prod_type in list_ean if list_ean}
                fullmap_pmc.update(dict(pmc_map))
        return fullmap_pmc

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