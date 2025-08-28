####### --- IMPORTS --- #######
from sqlite3 import Connection

####### --- TEST FUNCTIONS IN DATABASE.PY --- #######

def test_create_tables(db_connection: Connection):
    'test function responsable for creating many tables in database'

    db_cursor = db_connection.cursor()
    db_cursor.execute('''
        CREATE TABLE sqlite_schema (
            type TEXT,
            name TEXT,
            tbl_name TEXT,
            rootpage INTEGER,
            sqltext TEXT
            );
    ''')

    db_cursor.execute('''
        SELECT name
        FROM sqlite_schema
        WHERE type = 'table'
        AND name = 'produtos';
    ''')
