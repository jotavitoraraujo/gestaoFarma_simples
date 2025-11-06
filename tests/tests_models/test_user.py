### --- IMPORTS --- ###
from system.models.user import User

### --- ARRANGE/ACT PHASE --- ###
user_test_a = User (
    user_id = '123',
    user_name = 'TEST',
)

user_test_b = User (
    user_id = '123',
    user_name = 'TEST',
)

user_test_c = User (
    user_id = '456',
    user_name = 'TEST',
)

repr_string = f'''
        --- User Stats ---
        1. ID: {user_test_a.user_id}
        2. Name: {user_test_a.user_name}
        '''
repr_real = repr(user_test_a)

### --- ASSERT PHASE __init__ --- ###
def test_user_construition():
    assert user_test_a.user_id == '123'
    assert user_test_a.user_name == 'TEST'

### --- ASSERT PHASE __eq__ --- ###
def test_user_equality():
    assert user_test_a == user_test_a
    assert user_test_a == user_test_b
    assert user_test_a != user_test_c

### --- ASSERT PHASE __repr__ --- ###
def test_user_representation():
    assert repr_string == repr_real
