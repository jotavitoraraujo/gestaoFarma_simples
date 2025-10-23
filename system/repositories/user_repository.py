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
    
    def _select_table_user_by_id(self, id: int) -> tuple | None:
        'select the username of user using ID'

        cursor = self.connection_db.cursor()
        cursor.execute('''
            SELECT user_name
            FROM users
            WHERE id = ?
        ''',
            (
                id,
            )    
        )
        response: tuple | None = cursor.fetchone()
        return response

    def _select_table_user_by_username(self, username: str) -> tuple | None:
        'select the username of user using username'

        cursor = self.connection_db.cursor()
        cursor.execute('''
            SELECT user_name
            FROM users
            WHERE user_name = ?
        ''',
            (
                username,
            )    
        )
        response: tuple | None = cursor.fetchone()
        return response

    def _select_table_users_pin_hash(self, username: str) -> str | None:
        'selelct the pin_hash of user using username'

        cursor = self.connection_db.cursor()
        cursor.execute('''
            SELECT pin_hash
            FROM users
            WHERE user_name = ?
        ''',
            (
                username,
            )
        )
        response: tuple | None = cursor.fetchone()
        return response
    
    def _select_table_users_salt(self, username: str) -> bytes | None:
        'select the salt of user using username'

        cursor = self.connection_db.cursor()
        cursor.execute('''
            SELECT salt
            FROM users
            WHERE user_name = ?
        ''',
            (
                username,
            )
        )
        response: tuple | None = cursor.fetchone()
        return response

    def add(self, user: User, pin_hash: str, salt: bytes) -> int:
        'public method responsable by call the private method _insert_table_users to save an user in database'

        user_id: int = self._insert_table_user(user, pin_hash, salt)
        return user_id
    
    def find_by_id(self, id: int) -> str | None:
        'find an user by ID to internal uses'

        response: tuple | None = self._select_table_user_by_id(id)
        if response is not None:
            user_name: str = response[0]
            return user_name
    
    def find_by_username(self, user_name: str) -> str | None:
        'find an user by username to login'

        response: tuple | None = self._select_table_user_by_username(user_name)
        if response is not None:
            user_name: str = response[0]
            return user_name
    
    def get_pin_hash(self, user_name: str) -> str | None:
        'get the pin_hash using username of user'

        response: tuple | None = self._select_table_users_pin_hash(user_name)
        if response is not None:
            pin_hash: str = response[0]
            return pin_hash

    def get_salt(self, user_name: str) -> bytes | None:
        'get the salt using username of user'

        response: tuple | None = self._select_table_users_salt(user_name)
        if response is not None:
            salt: bytes = response[0]
            return salt

    
