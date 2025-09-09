####### --- IMPORTS --- #######
import pytest
from unittest.mock import patch
from sqlite3 import Connection
from system import database
from system.modules import users
from system.models.user import User

@patch('builtins.input')
def test_register_user(mock_user_name_input):
    sss = sss