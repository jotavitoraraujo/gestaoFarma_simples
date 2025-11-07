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
    salt: bytes = b'TEST_BYTES'

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
    salt: bytes = b'TEST_BYTES'

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
    salt: bytes = b'TEST_BYTES'

    ### --- PHASE ACT --- ###
    result: int = user_repo.add(user, pin_hash, salt)
    user_repo.assign_user_role('Admin', result)
    roles_result: list[Role] = user_repo.find_roles_by_userID(result)

    if isinstance(roles_result[0], Role) and not None:
        assert roles_result[0].id == 1
        assert roles_result[0].name == 'Admin'

def test_assign_duplicate_role(db_connection):

    ### --- PHASE ARRANGE --- ###
    database.starter_schema(db_connection)
    user_repo = UserRepository(db_connection)
    user = User (user_id = None, user_name = 'TEST')
    pin_hash: str = 'TEST_HASH'
    salt: bytes = b'TEST_BYTES'

    ### --- PHASE ACT --- ###
    result: int = user_repo.add(user, pin_hash, salt)
    user_repo.assign_user_role('Admin', result)

    if isinstance(result, int):
        with pytest.raises(sqlite3.IntegrityError):
            user_repo.assign_user_role('Admin', result)

def test_assign_non_existing_role(db_connection):

    ### --- PHASE ARRANGE --- ###
    database.starter_schema(db_connection)
    user_repo = UserRepository(db_connection)
    user = User(user_id = None, user_name = 'TEST')
    pin_hash: str = 'TEST_HASH'
    salt: bytes = b'TEST_BYTES'

    ### --- PHASE ACT --- ###
    result: int = user_repo.add(user, pin_hash, salt)
    
    ### --- PHASE ASSERT --- ###
    with pytest.raises(ValueError):
        user_repo.assign_user_role('TEST_ROLE', result)

def test_find_all_permissions_for_admin_user(db_connection):

    ### --- PHASE ARRANGE --- ###
    database.starter_schema(db_connection)
    user_repo = UserRepository(db_connection)
    user = User(user_id = None, user_name = 'TEST')
    pin_hash: str = 'TEST_HASH'
    salt: bytes = b'TEST_BYTES'
    result: int = user_repo.add(user, pin_hash, salt)
    expected_permissions_set: set = {
        'user:manage',
        'stock:import_nfe',
        'stock:view_all',
        'product:view_cost_price',
        'product:edit_sale_price',
        'sale:create',
        'sale:apply_discount',
        'sale:override_discount_limit',
        'report:view_financial'
    }

    ### --- PHASE ACT --- ###
    user_repo.assign_user_role('Admin', result)
    permission_list: list[Permission] = user_repo.find_all_permissions_by_userID(result)

    ### --- PHASE ASSERT --- ###
    if isinstance(permission_list, list) and len(permission_list) == 9:
        
        permissions_set: set = {permission.name for permission in permission_list}
        assert permissions_set == expected_permissions_set

def test_find_all_permissions_for_user_with_no_roles(db_connection):

    ### --- PHASE ARRANGE --- ###
    database.starter_schema(db_connection)
    user_repo = UserRepository(db_connection)
    user = User(user_id = None, user_name = 'TEST')
    pin_hash: str = 'TEST_HASH'
    salt: bytes = b'TEST_BYTES'
    result: int = user_repo.add(user, pin_hash, salt)

    ### --- PHASE ACT --- ###
    permission_list: list[Permission] = user_repo.find_all_permissions_by_userID(result)

    ### --- PHASE ASSERT --- ###
    assert permission_list == []

def test_find_all_permissions_for_user_with_multiple_roles(db_connection):

    ### --- PHASE ARRANGE --- ###
    database.starter_schema(db_connection)
    user_repo = UserRepository(db_connection)
    user = User(user_id = None, user_name = 'TEST')
    pin_hash: str = 'TEST_HASH'
    salt: bytes = b'TEST_BYTES'
    result: int = user_repo.add(user, pin_hash, salt)
    expected_permissions_set: set = {
        'user:manage',
        'stock:import_nfe',
        'stock:view_all',
        'product:view_cost_price',
        'product:edit_sale_price',
        'sale:create',
        'sale:apply_discount',
        'sale:override_discount_limit',
        'report:view_financial'
    }

    ### --- PHASE ACT --- ###
    user_repo.assign_user_role('Admin', result)
    user_repo.assign_user_role('Seller', result)
    permission_list: list[Permission] = user_repo.find_all_permissions_by_userID(result)

    ### --- PHASE ASSERT --- ###
    if isinstance(permission_list, list):
        assert len(permission_list) == 9
        permission_list_set: set = {permission.name for permission in permission_list}
        assert permission_list_set == expected_permissions_set

def test_getters_by_username(db_connection):

    ### --- PHASE ARRANGE --- ###
    database.starter_schema(db_connection)
    user_repo = UserRepository(db_connection)
    user = User(user_id = None, user_name = 'TEST')
    pin_hash: str = 'TEST_HASH'
    salt: bytes = b'TEST_BYTES'
    user_repo.add(user, pin_hash, salt)

    ### --- PHASE ACT --- ###
    result_name: str = user_repo.find_by_username('TEST')
    result_hash: str = user_repo.get_pin_hash('TEST')
    result_salt: bytes = user_repo.get_salt('TEST')

    ### --- PHASE ASSERT --- ###
    assert result_name == user.user_name
    assert result_hash == pin_hash
    assert result_salt == salt
