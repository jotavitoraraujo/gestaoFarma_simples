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
            if all(self) and all(other) == True:
                return True
            else:
                return False
        else:
            return False
        

