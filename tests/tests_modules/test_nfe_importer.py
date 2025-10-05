### --- IMPORTS --- ###
from system import database
from system.modules import nfe_importer
from sqlite3 import Connection
import pytest
pytestmark = pytest.mark.skip(reason = 'PAUSE')

### --- TEST SUITE TO NFE_IMPORTER FUNCTION --- ###
def test_nfe_importer(db_connection: Connection, unstable_xml):

    database.create_tables(db_connection)
    result: tuple = nfe_importer.importar_nfe(db_connection, unstable_xml)
    
    cursor = db_connection.cursor()
    cursor.execute('''
        SELECT COUNT (*)
        FROM produtos
    ''')
    product_count = cursor.fetchone()[0]
    cursor.execute('''
        SELECT COUNT (*) 
        FROM produtos_pendentes
    ''')
    pending_count = cursor.fetchone()[0]
    cursor.execute('''
        SELECT motivos_pendencia
        FROM produtos_pendentes
        WHERE motivos_pendencia = 'EAN ausente na NF-e'
    ''')
    string_return = cursor.fetchall()
    cursor.execute('''
        SELECT COUNT (*)
        FROM lotes  
    ''')
    batch_count = cursor.fetchone()[0]

    assert result == (1, 2)
    assert product_count == 1
    assert pending_count == 2
    assert batch_count == 1
    assert string_return == 'EAN ausente na NF-e'