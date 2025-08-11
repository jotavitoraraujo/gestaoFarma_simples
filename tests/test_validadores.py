import pytest
from unittest.mock import patch
from sistema.modulos import validadores_input

@patch('builtins.input')
def test_validador_qtd(mock_input):

    mock_input.return_value = '5'
    resultado = validadores_input.validador_qtd()
    assert resultado == 5