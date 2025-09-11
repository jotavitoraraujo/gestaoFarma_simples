### --- IMPORTS --- ###
from datetime import date

### --- CONVERSORS FUNCTIONS --- ###
def price_str_conversor(price_str: str) -> float:
    'receives an object string and make convert in an float'

    price_converted = float(price_str.replace(',', '.'))
    return price_converted

def expiration_date_str_conversor(date_str: str) -> date:
    'receives an object string and make convert to date_object for acceptance in sql'

    date_data_processing: list = date_str.split('/')
    if len(date_data_processing) == 3:
        date_str_formated = f'{date_data_processing[2]}-{date_data_processing[1]}-{date_data_processing[0]}'
        date_object = date.fromisoformat(date_str_formated)
    else:
        raise ValueError
    return date_object

def quantity_conversor(quantity_input: str) -> int:
    'receives an object string and make conversion to integer object'

    try:
        quantity_input = int(quantity_input)
        if isinstance(quantity_input, int):
            pass
    except ValueError:
        raise ValueError 
    
    return quantity_input
