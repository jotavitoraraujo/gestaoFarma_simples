### --- IMPORTS --- ###
from sqlite3 import Connection

class SalesRepository:
    def __init__(self, connection_db: Connection):
        self.connection_db = connection_db