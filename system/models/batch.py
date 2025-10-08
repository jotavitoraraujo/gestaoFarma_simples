### --- IMPORTS --- ###
from system.models.fiscal import PurchaseTaxDetails
from decimal import Decimal
from datetime import date

##########
# --- CLASS BATCH SETUP --- #
class Batch:
    def __init__(self, 
        id: int, 
        product_id: int,
        physical_id: str,
        quantity: Decimal, 
        unit_cost_amount: Decimal, 
        other_expenses_amount: Decimal,
        use_by_date: date,
        manufacturing_date: date, 
        received_date: date,
        taxation_details: PurchaseTaxDetails
        ):
        
        self.id = id
        self.product_id = product_id
        self.physical_id = physical_id
        self.quantity = quantity
        self.unit_cost_amount = unit_cost_amount
        self.other_expenses_amount = other_expenses_amount
        self.use_by_date = use_by_date
        self.manufacturing_date = manufacturing_date
        self.received_date = received_date
        self.taxation_details = taxation_details

    def __eq__(self, other: 'Batch') -> bool:
        'dunder method for comparassion the of Batch object'

        if isinstance(other, type(self)):
            return (
            other.id == self.id
            and other.physical_id == self.physical_id
            and other.product_id == self.product_id
            and other.quantity == self.quantity
            and other.unit_cost_amount == self.unit_cost_amount
            and other.other_expenses_amount == self.other_expenses_amount
            and other.use_by_date == self.use_by_date
            and other.manufacturing_date == self.manufacturing_date
            and other.received_date == self.received_date
            and other.taxation_details == self.taxation_details
            )
    
    def __repr__(self):
        'Batch type technical representation'

        return f'''
        --- Batch Atributes ---
        1. Batch ID: {self.id}
        2. Pyshical Batch ID: {self.physical_id}
        3. Product ID: {self.product_id}
        4. Quantity: {self.quantity:.0f}
        5. Cost price: {self.unit_cost_amount:.2f}
        6. Cost extras: {self.other_expenses_amount:.2f}
        7. Expiration date: {self.use_by_date}
        8. Manufacturing: {self.manufacturing_date}
        9. Entry date: {self.received_date}
        {self.taxation_details}
    '''