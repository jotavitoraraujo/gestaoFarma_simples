### --- IMPORTS --- ###
from sqlite3 import Connection, Cursor
from system.models.user import User
from system.models.rbac import Role, Permission
############################

class UserRepository:
######################## -- DUNDER METHODS   
    def __init__(self, connection_db: Connection):
        self.connection_db = connection_db
        self.cursor: Cursor = self.connection_db.cursor()

########################  -- SELECTS
    def _select_table_user_by_id(self, id: int) -> tuple | None:
        'select the username of user using ID'

        self.cursor.execute('''
            SELECT user_name
            FROM users
            WHERE id = ?
        ''',
            (
                id,
            )    
        )
        response: tuple | None = self.cursor.fetchone()
        return response

    def _select_table_user_by_username(self, username: str) -> tuple | None:
        'select the username of user using username'

        self.cursor.execute('''
            SELECT user_name
            FROM users
            WHERE user_name = ?
        ''',
            (
                username,
            )    
        )
        response: tuple | None = self.cursor.fetchone()
        return response

    def _select_table_users_pin_hash(self, username: str) -> str | None:
        'selelct the pin_hash of user using username'

        self.cursor.execute('''
            SELECT pin_hash
            FROM users
            WHERE user_name = ?
        ''',
            (
                username,
            )
        )
        response: tuple | None = self.cursor.fetchone()
        return response
    
    def _select_table_users_salt(self, username: str) -> bytes | None:
        'select the salt of user using username'

        self.cursor.execute('''
            SELECT salt
            FROM users
            WHERE user_name = ?
        ''',
            (
                username,
            )
        )
        response: tuple | None = self.cursor.fetchone()
        return response

    def _select_table_roles_id(self, role_name: str) -> tuple | None:
        'select from roles table the column id using the role name'

        self.cursor.execute('''
            SELECT id
            FROM roles
            WHERE role_name = ?
        ''',
            (
                role_name,
            )
        )
        response: tuple | None = self.cursor.fetchone()
        return response

######################## -- INSERTS
    def _insert_table_user(self, user: User, pin_hash: str, salt: bytes) -> int:
        'insert a user data in table users within database'

        self.cursor.execute('''
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
        user_id: int = self.cursor.lastrowid
        return user_id
    
    def _insert_table_user_roles(self, user_id: int, role_id: int):
        'insert the user_id and role_id in user_roles table'

        self.cursor.execute('''
            INSERT INTO user_roles (
                user_id,
                role_id
            )
            VALUES (?, ?)
        ''',
            (
                user_id,
                role_id,
            )
        )

######################## -- JOINS
    def _join_tables_to_get_roleID_and_name(self, user_id: int) -> list[tuple[int, str]] | None:
        'join multiple tables and get the id and function name using user_id'

        self.cursor.execute('''
            SELECT roles.id, roles.role_name
            FROM users
            JOIN user_roles ON users.id = user_roles.user_id
            JOIN roles ON user_roles.role_id = roles.id
            WHERE users.id = ?
        ''',
            (
                user_id,
            )
        )
        response: list[tuple[int, str]] | None = self.cursor.fetchall()
        return response

    def _join_table_to_get_all_permissions(self, user_id: int) -> list[tuple[int, str]] | None:
        'join multiple tables and get the id and permission name using user_id'

        self.cursor.execute('''
            SELECT permissions.id, permissions.permission_name
            FROM users
            JOIN user_roles ON users.id = user_roles.user_id
            JOIN roles ON user_roles.role_id = roles.id
            JOIN role_permissions ON roles.id = role_permissions.role_id
            JOIN permissions ON role_permissions.permission_id = permissions.id
            WHERE users.id = ?
        ''',
            (
                user_id,
            )
        )
        response: list[tuple[int, str]] | None = self.cursor.fetchall()
        return response

######################## -- PUBLIC METHODS
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
    
    def assign_user_role(self, role_name: str, user_id: int):
        'assign a role into determinaded user'

        response: tuple | None = self._select_table_roles_id(role_name)
        if response is not None: 
            role_id: int = response[0]
            self._insert_table_user_roles(user_id, role_id)
        else: return None

    def find_roles_by_userID(self, user_id: int) -> list[Role]:
        'find the roles the an user using user_id'

        response: list[tuple[int, str]] = self._join_tables_to_get_roleID_and_name(user_id)
        role_data: list[Role] = [(Role(id, name)) for id, name in response]
        return role_data
    
    def find_all_permissions_by_userID(self, user_id: int) -> list[Permission]:
        'find all permission that user have'

        response: list[tuple[int, str]] = self._join_table_to_get_all_permissions(user_id)
        permission_data: list[Permission] = [Permission(id, name) for id, name in response]
        return permission_data
########################
