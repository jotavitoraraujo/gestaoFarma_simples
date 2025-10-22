### --- IMPORTS --- ###
from sqlite3 import Connection
from system.models.user import User
############################

class UserRepository:
    def __init__(self, connection_db: Connection):
        self.connection_db = connection_db

    def _insert_table_user(self, user: User, pin_hash: str, salt: bytes) -> int:
        'insert a user data in table users within database'

        cursor = self.connection_db.cursor()
        cursor.execute('''
            INSERT INTO users (
                user_name,
                pin_hash,
                salt            
            )
            VALUES (?, ?, ?)
        ''',
            (
                user.user_name,
                pin_hash,
                salt,
            )
        )
        user_id: int = cursor.lastrowid
        return user_id
    
    def _select_table_user_by_username(self, username: str) -> tuple | None:
        'select the data of user using username'

        cursor = self.connection_db.cursor()
        cursor.execute('''
            SELECT *
            FROM users
            WHERE user_name = ?
        ''',
            (
                username,
            )    
        )
        response: tuple = cursor.fetchone()
        return response
    
    def _select_table_user_by_id(self, id: int) -> tuple | None:
        'select the data of user using ID'

        cursor = self.connection_db.cursor()
        cursor.execute('''
            SELECT *
            FROM users
            WHERE user_name = ?
        ''',
            (
                id,
            )    
        )
        response: tuple = cursor.fetchone()
        return response

    def add(self, user: User, pin_hash: str, salt: bytes) -> int:
        'public method responsable by call the private method _insert_table_users to save an user in database'

        user_id: int = self._insert_table_user(user, pin_hash, salt)
        return user_id
    
    def find_by_username(self, user_name: str) -> tuple | None:
        'find an user by username to login'

        user: tuple = self._select_table_user_by_username(user_name)
        return user

    def find_by_id(self, id: int) -> tuple | None:
        'find an user by ID to internal uses'

        user: tuple = self._select_table_user_by_id(id)
        return user