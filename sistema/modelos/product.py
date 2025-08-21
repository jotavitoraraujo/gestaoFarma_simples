from sistema.modelos.batch import Batch

class Product:
    def __init__(self, id, ean, name, sale_price):
        self.id = id
        self.ean = ean
        self.name = name
        self.sale_price = sale_price
        self.batch: list[Batch] = []

    def __eq__(self, other: 'Product') -> bool:
        
        if isinstance(other, type(self)):
            return (
            other.id == self.id 
            and other.ean == self.ean 
            and other.name == self.name 
            and other.sale_price == self.sale_price
            and other.batch == self.batch
            )
        else:
            return False

