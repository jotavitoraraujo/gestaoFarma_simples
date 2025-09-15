### --- IMPORTS --- ###
from datetime import date

### --- VALIDATORS FUNCTIONS --- ###
def batch_quantity_validator(quantity_input: int) -> bool:
    'check if a number is positive integer'
                         
    if isinstance(quantity_input, int) and quantity_input > 0:                                             
        return True    
    else:
        return False

def batch_physical_validator(batch_inputs: tuple) -> bool:
    'valiate the input of the physical batch printed on the product'

    if not isinstance(batch_inputs, tuple) and len(batch_inputs) == 2:
        return False
    if not isinstance(batch_inputs[0], str) and batch_inputs[1] == '1':
        return False      
    if not batch_inputs[0].isalnum():
        return False
    else:
        return True

def user_pass_validator(pin_digit: str) -> bool:
    'this function verify if length of the a password is equal 4 digits'
    
    if isinstance(pin_digit, str) and len(pin_digit) == 4 and pin_digit.isdigit():
        return True

    else:
        return False

def batch_expiration_date_validator(date_object: date) -> bool:
    'verify if conversion of the object is fact object date truly'
    if date_object > date.today():
        return True
    else:
        return False
    
def price_validator(price: float) -> bool:
    'receives an float number and verify if is valid'

    if isinstance(price, float) and price > 0:
        return True
    else:
        return False
    
def user_name_validator(user_name: str) -> bool:
    'receives an user_name and verify if is alphabetic and type str'

    if isinstance(user_name, str) is not None and user_name.isalpha():
        return True
    else:
        return False














