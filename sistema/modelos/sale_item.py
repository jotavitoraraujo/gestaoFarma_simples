from sistema.modelos.product import Product
from sistema.modelos.batch import Batch
from datetime import timedelta, date



class SaleItem:
    def __init__(self, product: Product, batch: Batch, quantity_sold):
        'cria o tipo Item a partir de outras classes com algumas caracteristicas unicas'
        self.product = product
        self.batch = batch
        self.quantity_sold = quantity_sold

    def __str__(self):
        'descreve o item'
        description = f'''
        1. Nome: {self.product.name}
        2. Lote DB: {self.batch.batch_id}
        3. Lote Fisico: {self.batch.physical_batch_id}
        4. Qtd: {self.quantity_sold}
        5. Data de Validade: {self.batch.expiration_date}
        6. Código de barras: {self.product.ean}
        '''
        return description
    
    def __repr__(self) -> str:
        'SaleItem type technical representation'
        
        return f'''
        1. Name: {self.product.name} 
        2. Batch ID in Database: {self.batch.batch_id} 
        3. Physical Batch: {self.batch.physical_batch_id}
        3. Quantity: {self.quantity_sold} 
        4. Expiration Date: {self.batch.expiration_date} 
        5. Barcode (EAN): {self.product.ean}
        '''

    
    def calculate_subtotal(self):
        'access the sales price of the product and multiply for the quantity sold to return the total of this'
        
        price = self.product.sale_price
        quantity = self.quantity_sold

        subtotal = float(price * quantity)
        return subtotal
        

    def get_discounted_price(self, date_object: date) -> float: 
        'applies different discount levels based on the due date of the item'
        
        expiration_date = self.batch.expiration_date
        days_until_expiration: timedelta = (expiration_date - date_object)       
                
        EIGHT_DAYS = timedelta(days = 8)
        FIFTEEN_DAYS = timedelta(days = 16)
        TWENTY_DAYS = timedelta(days = 21)
        THIRTY_DAYS = timedelta(days = 31)     
                       
        final_price = self.product.sale_price       

        # discount conditional 

        if days_until_expiration < EIGHT_DAYS:            
            eighty_percent = float(self.product.sale_price * 0.8)
            final_price = float(self.product.sale_price - eighty_percent)                                     
                                    
        elif days_until_expiration < FIFTEEN_DAYS:
            fifty_percent = float(self.product.sale_price * 0.5)
            final_price = float(self.product.sale_price - fifty_percent)                
        
        elif days_until_expiration < TWENTY_DAYS:
            thirty_days = float(self.product.sale_price * 0.3)
            final_price = float(self.product.sale_price - thirty_days)                
        
        elif days_until_expiration < THIRTY_DAYS:
            twenty_days = float(self.product.sale_price * 0.2)
            final_price = float(self.product.sale_price - twenty_days)     
        
        
        # adds a conditional that checks if there is no prejudice
            
        if final_price < self.batch.cost_price:
            price_to_return = self.product.sale_price
        else:
            price_to_return = final_price
        
        return price_to_return