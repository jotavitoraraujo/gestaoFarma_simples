### --- IMPORTS --- ###
from system.utils import converters, validators
from system.utils.exceptions import ConversionError
from system import security
from datetime import date
from typing import Callable, Any
from pwinput import pwinput
import logging

### --- JOKER FOR CONVERTER --- ###
def return_value(x):
    return x

### --- INTERNAL FUNCTION RESPONSABLE BY INPUT CONTROLLER WORKFLOW --- ###
def _collector_generic_input(ask: str, func_conv: Callable[[str], Any], func_valid: Callable[[Any], bool], func_input: Callable = input) -> Any | None:

    logging.warning(f'[ALERTA] Para cancelar pressione "Q".')
    while True:
        ask_input: str = func_input(f'{ask}')
        if ask_input.strip() == '' or ask_input.lower() == 'q': return None
        try:
            conversion_result: Any = func_conv(ask_input)
            validated_result: bool = func_valid(conversion_result)
            if validated_result is True:
                return conversion_result
            else:
                logging.error(f'[ERRO] Os dados inseridos são inválidos. Tente novamente.')
        except ConversionError:
            logging.error(f'[ERRO] Os dados inseridos são inválidos. Tente novamente.')
   

### --- INPUT/OUTPUT COLLECTORS FUNCTIONS --- ###
def collect_price() -> float:

    converter: Callable = converters.price_str_conversor
    validator: Callable = validators.price_validator

    ask_price: str = f'[ALERTA] Insira o preço: '
    price: float = _collector_generic_input(ask_price, converter, validator)
    return price

def collect_date() -> date:

    converter: Callable = converters.date_str_conversor
    validator: Callable = validators.date_validator

    ask_date: str = f'[ALERTA] Insira a data: '
    expiration: date = _collector_generic_input(ask_date, converter, validator)
    return expiration

def collect_user_name() -> str: 

    converter: Callable = converters.user_name_conversor
    validator: Callable = validators.user_name_validator

    ask_user_name: str = f'[ALERTA] Insira o Nome de Usuário: '
    user_name: str = _collector_generic_input(ask_user_name, converter, validator)
    return user_name

def collect_user_pin() -> str:

    converter: Callable = converters.return_value
    validator: Callable = validators.user_pass_validator
    mask_pass: Callable = pwinput

    ask_pass: str = f'[ALERTA] Insira a senha: '
    user_pass: str = _collector_generic_input(ask_pass, converter, validator, mask_pass)
    return user_pass

def collect_quantity() -> int:

    conversor: Callable = converters.batch_quantity_conversor
    validator: Callable = validators.batch_quantity_validator

    ask_quantity: str = f'[ALERTA] Insira a quantidade deste item: '
    quantity: int = _collector_generic_input(ask_quantity, conversor, validator)
    return quantity

def collect_batch_physical() -> str:

    conversor: Callable = return_value
    validator: Callable = validators.batch_physical_validator    

    ask_batch_physical: str = f'[ALERTA] Insira o Lote Fisico: '
    batch_physical: str = _collector_generic_input(ask_batch_physical, conversor, validator)
    return batch_physical

def collect_EAN() -> str:

    conversor: Callable = return_value
    validator: Callable = validators.EAN_validator
    ask_ean_code: str = f'[ALERTA] Insira o Codigo de Barras (EAN): '
    ean: str = _collector_generic_input(ask_ean_code, conversor, validator)
    return ean