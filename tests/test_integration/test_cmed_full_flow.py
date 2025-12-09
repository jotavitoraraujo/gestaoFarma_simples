### --- IMPORTS --- ###
from system.repositories.cmed_repository import CMEDRepository
from system.modules.cmed_importer import CMEDImporter
from system.modules.cmed_parser import CMEDParser
from pathlib import Path
from sqlite3 import Connection, Cursor


def test_cmed_happy_path(db_connection: Connection):

    ### --- PHASE ARRANGE --- ###
    func_save = CMEDRepository(db_connection).save_cmed
    path: Path = Path(__file__).parent.parent/'data_tests'/'test_cmed_table.xlsx'
    importer = CMEDImporter(CMEDParser, func_save)
    cursor: Cursor = db_connection.cursor()
    
    ### --- PHASE ACT --- ###
    importer.run_import(path)
    cursor.execute('''
        SELECT COUNT (*)
        FROM cmed_table
    ''')
    result: tuple[int | None] = cursor.fetchone()

    ### --- PHASE ASSERT --- ###
    assert result is not None
    total_lines: int = result[0]
    assert total_lines == 3

def test_cmed_EAN_return_string(db_connection: Connection):
        
    ### --- PHASE ARRANGE --- ###
    func_save = CMEDRepository(db_connection).save_cmed
    path: Path = Path(__file__).parent.parent/'data_tests'/'test_cmed_table.xlsx'
    importer = CMEDImporter(CMEDParser, func_save)
    cursor: Cursor = db_connection.cursor()

    ### --- PHASE ACT --- ###
    importer.run_import(path)
    cursor.execute('''
        SELECT "EAN 1"
        FROM cmed_table
        WHERE "EAN 1" = '07894916503754'
    ''')
    result: tuple[str | None] = cursor.fetchone()

    ### --- PHASE ASSERT --- ###
    assert result is not None
    ean: str = result[0]
    assert isinstance(ean, str)
    assert ean == '07894916503754'

def test_cmed_import_idempotency(db_connection: Connection):
    
    ### --- PHASE ARRANGE --- ###
    func_save = CMEDRepository(db_connection).save_cmed
    path: Path = Path(__file__).parent.parent/'data_tests'/'test_cmed_table.xlsx'
    importer = CMEDImporter(CMEDParser, func_save)
    cursor: Cursor = db_connection.cursor()

    ### --- PHASE ACT --- ###
    importer.run_import(path)
    cursor.execute('''
        SELECT COUNT (*)
        FROM cmed_table
    ''')
    result: tuple[int | None] = cursor.fetchone()
    
    ### --- PHASE ASSERT --- ###
    assert result is not None
    total_lines: int = result[0]
    assert total_lines == 3

    ### --- PHASE ACT 2 --- ###
    importer.run_import(path)
    cursor.execute('''
        SELECT COUNT (*)
        FROM cmed_table
    ''')
    result2: tuple[int | None] = cursor.fetchone()
    
    ### --- PHASE ASSERT 2 --- ###
    assert result2 is not None
    total_lines2: int = result2[0]
    assert total_lines2 == 3
