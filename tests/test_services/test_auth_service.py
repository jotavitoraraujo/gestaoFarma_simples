### --- IMPORTS --- ###
from system.repositories.user_repository import UserRepository
from system.utils.exceptions import UserAlreadyExistsError
from system.services.auth_service import AuthService
from system.models.user import User
from unittest.mock import MagicMock, ANY, patch
from system import security
from system import database
import pytest
#######################

def test_auth_service_register(mock_user_repo, auth_service):

    ### --- PHASE ARRANGE --- ###
    mock_user_repo.add.return_value = 1
    
    ### --- PHASE ACT --- ###
    auth_service.register('TEST', '0000')

    ### --- PHASE ASSERT --- ###
    mock_user_repo.add.assert_called_once_with(ANY, ANY, ANY)
    mock_user_repo.assign_user_role.assert_called_once_with('Admin', 1)
    
def test_auth_service_register_raise_exception(mock_user_repo, auth_service):

    ### --- PHASE ARRANGE --- ###
    mock_user_repo.add.side_effect = UserAlreadyExistsError('TEST')

    ### --- PHASE ACT/ASSERT --- ###
    with pytest.raises(UserAlreadyExistsError):
        auth_service.register('TEST', '0000')

def test_auth_service_authenticate_sucess(mock_user_repo, auth_service):

    ### --- PHASE ARRANGE --- ###
    with patch('system.security.verify_pin') as mock_security:

        mock_user_repo.find_by_username.return_value = 'TEST'
        mock_user_repo.get_pin_hash.return_value = 'HASH_TEST'
        mock_user_repo.get_salt.return_value = b'SALT_TEST'
        mock_security.return_value = True

        user_name: str = 'TEST'
        provided_pin: str = '0000'

        ### --- PHASE ACT --- ###
        result: User | None = auth_service.authenticate(user_name, provided_pin)

        ### --- PHASE ASSERT --- ###
        assert result.user_name == 'TEST'

def test_auth_service_authenticate_user_not_found(mock_user_repo, auth_service):

    ### --- PHASE ARRANGE --- ###
    mock_user_repo.find_by_username.return_value = None
    user_name: str = 'TEST'
    provided_pin: str = '0000'

    ### --- PHASE ACT --- ###
    result: User | None = auth_service.authenticate(user_name, provided_pin)

    ### --- PHASE ASSERT --- ###
    assert result == None

def test_auth_service_authenticate_false_pin(mock_user_repo, auth_service):

    ### --- PHASE ARRANGE --- ###
    with patch('system.security.verify_pin') as mock_security:
        
        mock_user_repo.find_by_username.return_value = 'TEST'
        mock_user_repo.get_pin_hash.return_value = 'TEST_HASH'
        mock_user_repo.get_salt.return_value = b'TEST_SALT'
        mock_security.return_value = False

        user_name: str = 'TEST'
        provided_pin: str = '0000'

        ### --- PHASE ACT --- ###
        result: User | None | False = auth_service.authenticate(user_name, provided_pin)

        ### --- PHASE ASSERT --- ###
        assert result == None
