### --- IMPORTS --- ###
from system import database
from system.repositories.user_repository import UserRepository
from system.models.user import User
from system.models.rbac import Role, Permission
import sqlite3
import pytest
####################

def test_add_user_and_find_id(db_connection):

    ### --- PHASE ARRANGE --- ###
    database.starter_schema(db_connection)
    user_repo = UserRepository(db_connection)
    user = User (user_id = None, user_name = 'TEST')
    pin_hash: str = 'TEST_HASH'
    salt: bytes = b'TEST_BYTE'

    ### --- PHASE ACT --- ###
    user_id: int = user_repo.add(user, pin_hash, salt)
    if isinstance(user_id, int):
        result: str = user_repo.find_by_id(user_id)
    
    ### --- PHASE ASSERT --- ###
    assert result == 'TEST'

def test_find_by_id_none(db_connection):

    ### --- PHASE ARRANGE --- ###
    database.starter_schema(db_connection)
    user_repo = UserRepository(db_connection)
    user_id = None

    ### --- PHASE ACT --- ###
    result = user_repo.find_by_id(user_id)
    
    ### --- PHASE ASSERT --- ###
    assert result == None

def test_find_by_id_non_existent(db_connection):
    
    ### --- PHASE ARRANGE --- ###
    database.starter_schema(db_connection)
    user_repo = UserRepository(db_connection)
    user_id = 999999999
    
    ### --- PHASE ACT --- ###
    result = user_repo.find_by_id(user_id)
    
    ### --- PHASE ASSERT --- ###
    assert result is None


def test_add_user_violates_not_null_constraint(db_connection):

    ### --- PHASE ARRANGE --- ###
    database.starter_schema(db_connection)
    user_repo = UserRepository(db_connection)
    user = User(user_id = None, user_name = 'TEST')
    pin_hash = None
    salt: bytes = b'TEST_BYTE'

    ### --- PHASE ACT/ARRANGE --- ###
    with pytest.raises(sqlite3.IntegrityError):
        user_repo.add(user, pin_hash, salt)
    
def test_add_duplicate_user_name(db_connection):

    ### --- PHASE ARRANGE --- ###
    database.starter_schema(db_connection)
    user_repo = UserRepository(db_connection)
    user1 = User (user_id = None, user_name = 'TEST')
    user2 = User (user_id = None, user_name = 'TEST')
    pin_hash1 = 'TEST_HASH'
    pin_hash2 = 'TEST_HASH'
    salt1 = b'TEST_BYTES'
    salt2 = b'TEST_BYTES'

    ### --- PHASE ACT/ASSERT --- ###
    result = user_repo.add(user1, pin_hash1, salt1)

    if isinstance(result, int):
        assert result == 1
        with pytest.raises(sqlite3.IntegrityError):
            user_repo.add(user2, pin_hash2, salt2)

def test_assign_user_role_and_find_roles(db_connection):

    ### --- PHASE ARRANGE --- ###
    database.starter_schema(db_connection)
    user_repo = UserRepository(db_connection)
    user = User (user_id = None, user_name = 'TEST')
    pin_hash: str = 'TEST_HASH'
    salt: bytes = b'TEST_SALT'

    ### --- PHASE ACT --- ###
    result: int = user_repo.add(user, pin_hash, salt)
    user_repo.assign_user_role('Admin', result)
    roles_result: list[Role] = user_repo.find_roles_by_userID(result)



    if isinstance(roles_result[0], Role) and not None:
        assert roles_result[0].id == 1
        assert roles_result[0].name == 'Admin'

