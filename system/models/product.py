### --- IMPORTS --- ###
from system.models.fiscal import FiscalProfile
from system.models.batch import Batch
from decimal import Decimal

#########
# --- CLASS PRODUCT SETUP --- #
class Product:
    __slots__ = (
        'id', 
        'supplier_code', 
        'ean', 
        'name', 
        'anvisa_code', 
        'sale_price', 
        'max_consumer_price', 
        'fiscal_profile', 
        'batch'
    )
    
    def __init__(self, 
        id: int, 
        supplier_code: str, 
        ean: str, 
        name: str,
        anvisa_code: str,
        sale_price: Decimal,
        max_consumer_price: Decimal,
        fiscal_profile: FiscalProfile
        ):
        'create class Product'
        
        self.id = id
        self.supplier_code = supplier_code
        self.ean = ean
        self.name = name
        self.anvisa_code = anvisa_code
        self.sale_price = sale_price
        self.max_consumer_price = max_consumer_price
        self.fiscal_profile = fiscal_profile
        self.batch: list[Batch] = []

    def __eq__(self, other: 'Product') -> bool:
        'dunder method for comparassion the of Product object'

        if isinstance(other, type(self)):
            return (
            other.id == self.id
            and other.supplier_code == self.supplier_code
            and other.ean == self.ean
            and other.name == self.name
            and other.anvisa_code == self.anvisa_code  
            and other.sale_price == self.sale_price
            and other.max_consumer_price == self.max_consumer_price
            and other.fiscal_profile == self.fiscal_profile
            and other.batch == self.batch
            )
        else:
            return False

    def __repr__(self):
        'Product type technical representation'

        return f'''
        --- Product Atributes ---
        1. ID Autoincrement: {self.id}
        2. ID Supplier: {self.supplier_code}
        3. EAN: {self.ean}
        4. Name: {self.name}
        5. ANVISA Code: {self.anvisa_code}
        6. Sale price: {self.sale_price}
        7. MAX Price Consumer: {self.max_consumer_price}
        {self.fiscal_profile}
        '''