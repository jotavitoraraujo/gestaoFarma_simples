from sistema.modelos.produto import Produto
from sistema.modelos.lote import Lote
from datetime import timedelta, date



class SaleItem:
    def __init__(self, product: Produto, batch: Lote, quantity_sold):
        'cria o tipo Item a partir de outras classes com algumas caracteristicas unicas'
        self.product = product
        self.batch = batch
        self.quantity_sold = quantity_sold

    def __str__(self):
        'descreve o item'
        description = f'''
        1. Nome: {self.product.nome}
        2. Lote DB: {self.batch.id_lote}
        3. Lote Fisico: {self.batch.id_lote_fisico}
        4. Qtd: {self.quantity_sold}
        5. Data de Validade: {self.batch.data_validade}
        6. Código de barras: {self.product.ean}
        '''
        return description
    
    def __repr__(self) -> str:
        'SaleItem type technical representation'
        
        return f'''
        1. Name: {self.product.nome} 
        2. Batch ID in Database: {self.batch.id_lote} 
        3. Physical Batch: {self.batch.id_lote_fisico}
        3. Quantity: {self.quantity_sold} 
        4. Expiration Date: {self.batch.data_validade} 
        5. Barcode (EAN): {self.product.ean}
        '''

    
    def calculate_subtotal(self):
        'access the sales price of the product and multiply for the quantity sold to return the total of this'
        
        price = self.product.preco_venda
        quantity = self.quantity_sold

        subtotal = float(price * quantity)
        return subtotal
        

    def get_discounted_price(self, date_object: date) -> float: 
        'applies different discount levels based on the due date of the item'
        
        expiration_date = self.batch.data_validade
        days_until_expiration: timedelta = (expiration_date - date_object)       
                
        EIGHT_DAYS = timedelta(days = 8)
        FIFTEEN_DAYS = timedelta(days = 16)
        TWENTY_DAYS = timedelta(days = 21)
        THIRTY_DAYS = timedelta(days = 31)     
                       
        final_price = self.product.preco_venda       

        # discount conditional 

        if days_until_expiration < EIGHT_DAYS:            
            eighty_percent = float(self.product.preco_venda * 0.8)
            final_price = float(self.product.preco_venda - eighty_percent)                                     
                                    
        elif days_until_expiration < FIFTEEN_DAYS:
            fifty_percent = float(self.product.preco_venda * 0.5)
            final_price = float(self.product.preco_venda - fifty_percent)                
        
        elif days_until_expiration < TWENTY_DAYS:
            thirty_days = float(self.product.preco_venda * 0.3)
            final_price = float(self.product.preco_venda - thirty_days)                
        
        elif days_until_expiration < THIRTY_DAYS:
            twenty_days = float(self.product.preco_venda * 0.2)
            final_price = float(self.product.preco_venda - twenty_days)     
        
        
        # adds a conditional that checks if there is no prejudice
            
        if final_price < self.batch.preco_custo:
            price_to_return = self.product.preco_venda
        else:
            price_to_return = final_price
        
        return price_to_return