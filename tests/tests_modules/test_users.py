####### --- IMPORTS --- #######
import pytest
from unittest.mock import patch
from sqlite3 import Connection
from system import database
from system.modules import users
from system.models.user import User
