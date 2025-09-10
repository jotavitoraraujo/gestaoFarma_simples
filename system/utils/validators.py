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

    if isinstance(batch_inputs, tuple) and len(batch_inputs) == 2:
        if isinstance(batch_inputs[0], str) and batch_inputs[1] == '1':
            alpha = batch_inputs[0].isalnum()
            if alpha is True:
                return True
            else:
                return False
        else:
            return False
    else:
        return False

def user_pass_validator(pin_digit: str) -> bool:
    'this function verify if length of the a password is equal 4 digits'
    
    if len(pin_digit) != 4:
        return False                
    else:
        return True

def batch_expiration_date_validator(date_object: date) -> bool:
    'verify if conversion of the object is fact object date truly'
    if date_object > date.today():
        return True
    else:
        return False















