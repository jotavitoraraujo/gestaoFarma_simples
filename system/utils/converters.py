### --- IMPORTS --- ###
from system.utils.exceptions import ConversionError
from datetime import date

### --- CONVERSORS FUNCTIONS --- ###
def price_str_conversor(price_str: str) -> float:
    'receives an object string and make convert in an float'

    try:
        price_converted = float(price_str.replace(',', '.'))
    except (ValueError, TypeError, AttributeError) as conversion_error:
        raise ConversionError(f'[ERRO] Os dados fornecidos estão corrompidos ou são incompativeis.') from conversion_error
    
    return price_converted

def expiration_date_str_conversor(date_str: str) -> date:
    'receives an object string and make convert to date_object for acceptance in sql'

    try:
        if isinstance(date_str, str):
            date_data_processing: list = date_str.split('/')
            if isinstance(date_data_processing, list) and len(date_data_processing) == 3:
                date_str_formated = f'{date_data_processing[2]}-{date_data_processing[1]}-{date_data_processing[0]}'
                date_object = date.fromisoformat(date_str_formated)
                return date_object
            else:
                raise ConversionError(f'[ERRO] O dado não é uma lista ou não possui a extensão requisitada.')
        else:
            raise ConversionError(f'[ERRO] O dado inserido não é do tipo correto. Ex: DD/MM/AAAA')
    except (ValueError, AttributeError, IndexError) as conversion_error:
        raise ConversionError(f'[ERRO] Os dados fornecidos estão corrompidos ou são imcompátiveis.') from conversion_error

def quantity_conversor(quantity_input: str) -> int:
    'receives an object string and make conversion to integer object'

    try:
        quantity_input = int(quantity_input)
        if isinstance(quantity_input, int):
            pass
    except ValueError:
        raise ValueError 
    
    return quantity_input
