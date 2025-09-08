####### --- IMPORTS --- #######
import pytest
from unittest.mock import patch
from sqlite3 import Connection
from sistema import database
from sistema.modulos import users
from sistema.modelos.user import User

@patch('builtins.input')
def test_register_user(mock_user_name_input):
    