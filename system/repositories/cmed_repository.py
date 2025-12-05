### --- IMPORTS --- ###
from sqlite3 import Connection
from typing import Callable, Any
#######################

class CMEDRepository:
    def __init__(self, connection_db: Connection):
        self.connection_db = connection_db

    def save_cmed(self, persist_method: Callable[[Any]] = None):
        'this function uses the persist method of your choice to save in db, currently df.tosql()'

        persist_method(
            name = 'cmed_table',
            con = self.connection_db,
            if_exists = 'replace',
            index = False
        )

