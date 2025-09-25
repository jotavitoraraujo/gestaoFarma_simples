from system.models.batch import Batch

class Product:
    def __init__(self, id, supplier_code, ean, name, sale_price):
        'create class Product'
        
        self.id = id
        self.supplier_code = supplier_code
        self.ean = ean
        self.name = name
        self.sale_price = sale_price
        self.batch: list[Batch] = []

    def __eq__(self, other: 'Product') -> bool:
        'dunder method for comparassion the of Product object'

        if isinstance(other, type(self)):
            return (
            other.id == self.id
            and other.supplier_code == self.supplier_code 
            and other.ean == self.ean 
            and other.name == self.name 
            and other.sale_price == self.sale_price
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
        5. Sale price: {self.sale_price}
        '''