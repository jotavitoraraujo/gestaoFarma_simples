
class User:
    def __init__(self, user_id, user_name, user_pin):
        self.user_id = user_id
        self.user_name = user_name
        self.user_pin = user_pin

    
    def __eq__(self, other) -> bool:
        'dunder method able the if comparate with yourself'

        if isinstance(other, type(self)):
            return (
                other.user_id == self.user_id
                and other.user_name == self.user_name
                and other.user_pin == self.user_pin
            )
        else:
            return False
        
    def __repr__(self) -> str:
        'User type technical representation'

        return f'''
        --- User Stats ---
        1. ID: {self.user_id}
        2. Name: {self.user_name}
        3. Hash: {self.user_pin}
        '''
    
    def __str__(self) -> str:
        'Description of the User'

        return f'''
        --- User Stats ---
        1. ID: {self.user_id}
        2. Name: {self.user_name}
        3. Hash: {self.user_pin}
        '''