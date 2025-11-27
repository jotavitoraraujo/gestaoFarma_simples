### --- IMPORTS --- ###
from system.models.product import Product
from system.models.batch import Batch
from decimal import Decimal
################

class Item:
    def __init__(self, product: Product, batch: Batch, quantity_sold: int):
        'create an Item using Products, Batches of that Product, and Quantities entered by the users'
        
        self.product = product
        self.batch = batch
        self.quantity_sold = quantity_sold

    def __str__(self):

        description = f'''
        1. Nome: {self.product.name}
        2. Lote DB: {self.batch.id}
        3. Lote Fisico: {self.batch.physical_id}
        4. Qtd: {self.quantity_sold}
        5. Data de Validade: {self.batch.use_by_date}
        6. Código de barras: {self.product.ean}
        '''
        return description
    
    def __repr__(self) -> str:
        'SaleItem type technical representation'
        
        return f'''
        1. Name: {self.product.name} 
        2. Batch ID in Database: {self.batch.id} 
        3. Physical Batch: {self.batch.physical_id}
        3. Quantity: {self.quantity_sold} 
        4. Expiration Date: {self.batch.use_by_date} 
        5. Barcode (EAN): {self.product.ean}
        '''

    
    def calculate_subtotal(self):
        'access the sales price of the product and multiply for the quantity sold to return the total of this'
        
        price: Decimal = self.product.sale_price
        quantity: Decimal = self.quantity_sold

        subtotal: Decimal = price * quantity
        return subtotal