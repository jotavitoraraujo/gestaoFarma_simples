from sistema.modelos.batch import Batch

class Product:
    def __init__(self, id, ean, name, sale_price):
        self.id = id
        self.ean = ean
        self.name = name
        self.sale_price = sale_price
        self.batch: list[Batch] = []