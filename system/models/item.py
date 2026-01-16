### --- IMPORTS --- ###
from system.models.product import Product
from decimal import Decimal
from typing import Any
################

class Item:
    def __init__(self, product: Product, fifo: list[Any], quantity_sold: Decimal):
        'create an Item using Products, Batches of that Product, and Quantities entered by the users'
        
        self.product = product
        self.fifo = fifo
        self.quantity_sold = quantity_sold
    
    def calculate_subtotal(self):
        'access the sales price of the product and multiply for the quantity sold to return the total of this'
        
        price: Decimal = self.product.sale_price
        quantity: Decimal = self.quantity_sold

        subtotal: Decimal = price * quantity
        return subtotal