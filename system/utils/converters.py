### --- IMPORTS --- ###
from system.utils.exceptions import ConversionError
from datetime import date

### --- CONVERSORS FUNCTIONS --- ###
def price_str_conversor(price_str: str) -> float:
    'receives an object string and make convert in an float'

    try:
        price_converted = float(price_str.replace(',', '.'))
    except (ValueError, TypeError, AttributeError) as conversion_error:
        raise ConversionError(f'[ERRO] Os dados fornecidos estão corrompidos ou são incompativeis.', conversion_error, price_str) from conversion_error
    
    return price_converted

def expiration_date_str_conversor(date_str: str) -> date:
    'receives an object string and make convert to date_object for acceptance in sql'

    try:
        if not isinstance(date_str, str):
            raise TypeError 
        date_data_processing: list = date_str.split('/')
        
        if not isinstance(date_data_processing, list) and len(date_data_processing) == 3:
            raise (ValueError, IndexError)
        
        date_str_formated = f'{date_data_processing[2]}-{date_data_processing[1]}-{date_data_processing[0]}'
        date_object = date.fromisoformat(date_str_formated)
        
        if not isinstance(date_object, date): 
            raise TypeError
        return date_object
    
    except (TypeError, ValueError, IndexError) as conversion_error:
        raise ConversionError(f'[ERRO] Os dados estão corrompídos ou são invalidos.', conversion_error, date_str) from conversion_error
            
def batch_quantity_conversor(quantity_input: str) -> int:
    'receives an object string and make conversion to integer object'

    try:
        if not isinstance(quantity_input, str):
            raise TypeError
        if not quantity_input.isdigit():
            raise ValueError
        quantity = int(quantity_input)   
        return quantity
    
    except (TypeError, ValueError) as conversion_error:
        raise ConversionError(f'[ERRO] Os dados são inválidos ou estão corrompidos.', conversion_error, quantity_input) from conversion_error

def user_name_conversor(user_name: str) -> str:

    try:
        user_name_formated = user_name.replace(' ', '').upper()
        return user_name_formated

    except (ValueError, TypeError) as conversion_error:
        raise ConversionError(f'[ERRO] Os dados fornecediso estão corrompidos ou são incompátiveis.', conversion_error, user_name) from conversion_error
    