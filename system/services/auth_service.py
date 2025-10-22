### --- IMPORTS --- ###
from system.repositories.user_repository import UserRepository
from system.models.user import User
from system import security
from typing import Callable
###########################

class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def _create_user(self, user_name: str) -> User:
        'instanciated an object User'

        user = User (
            user_id = None,
            user_name = user_name
        )
        return user

    def register(self, user_name: str, pin: str):
        'register an user in system'

        salt: bytes = security.generate_salt()
        pin_hash: str = security.hash_pin(pin, salt)
        user: User = self._create_user(user_name)
        self.user_repository.add(user, pin_hash, salt)

    def authenticate(self, user_name: str, pin: str) -> User | None:
        'authenticate the user in system'

        response: tuple = self.user_repository.find_by_username(user_name)
        
        if response is not None:
            user_id: int | None = response[0]
            user_name: str | None = response[1]
            pin_hash: str | None = response[2]
            salt: bytes | None = response[3]
            func_compare: Callable = security.compare_pin
            result: bool = security.verify_pin(pin_hash, salt, pin, func_compare())
        
        if result:
            user = User (
                user_id = user_id,
                user_name = user_name
            )
            return user
        else:
            return None