### --- IMPORTS --- ###
from system.repositories.user_repository import UserRepository
from system.services.auth_service import AuthService
from system.models.user import User
from unittest.mock import MagicMock, ANY
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
    
