import pytest
from unittest.mock import patch
from sistema.modulos import validadores_input
from datetime import date

@patch('builtins.input')
def test_validador_qtd(mock_input):

    mock_input.return_value = '5'
    resultado = validadores_input.validador_qtd()
    assert resultado == 5

def date_instance():
    date_object = date(2026, 1, 1)
    return date_object

@patch('builtins.input')
def test_date_validator(mock_date_input):
    mock_date_input.return_value = '01/01/2026'
    result = validadores_input.date_validator()
    date_object = date_instance()
    assert result == date_object
    