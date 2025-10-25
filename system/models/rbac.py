### --- IMPORTS --- ###
#######################

class Role:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

    def __eq__(self, other: 'Role'):
        'dunder method for comparisson the Role object'

        if isinstance(other, type(self)):
            return (
                other.id == self.id
                and other.name == self.name
            )
        else: return False

    def __repr__(self):
        'Role type technical representation'

        return f'''
        --- Role Attributes ---
        1. ID Internal: {self.id}
        2. Name: {self.name}
        '''

class Permission:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

    def __eq__(self, other: 'Permission'):
        'dunder method for comparission the Permission object'

        if isinstance(other, type(self)):
            return (other.id == self.id
            and other.name == self.name
            )
        else: return False
    
    def __repr__(self):
        'Permission type technical representation'

        return f'''
        --- Permission Attributes ---
        1. ID Internal: {self.id}
        2. Name: {self.name}
        '''