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
        user_id: int = self.user_repository.add(user, pin_hash, salt)
        self.user_repository.assign_user_role('Admin', user_id)

    def authenticate(self, user_name: str, provided_pin: str) -> User | None:
        'authenticate the user in system'

        user_name: str = self.user_repository.find_by_username(user_name)
        
        if user_name is not None:
            stored_hash: str = self.user_repository.get_pin_hash(user_name)
            stored_salt: bytes = self.user_repository.get_salt(user_name)
        
        if isinstance(provided_pin, str):
            func_compare: Callable = security.compare_pin
            result: bool = security.verify_pin(stored_hash, stored_salt, provided_pin, func_compare)
        
        if result is True:
            user = self._create_user(user_name)
            return user
        
        #### -> ENVIAR MENSAGEM GENERICA NA UI QUANDO CHAMADO COMO METODO DE SEGURANÇA
        #### -> "NOME DE USUARIO OU SENHA INCORRETOS."
        
