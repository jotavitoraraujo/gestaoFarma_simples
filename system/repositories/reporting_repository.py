### --- IMPORTS --- ###
from sqlite3 import Connection, Cursor

class ReportingRepository:
    __slots__ = ('connection_db')
    
    def __init__(self, connection_db: Connection):
        self.connection_db = connection_db
