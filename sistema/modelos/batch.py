class Batch:
    def __init__(self, batch_id, physical_batch_id, product_id, quantity, cost_price, expiration_date, entry_date):
        self.batch_id = batch_id
        self.physical_batch_id = physical_batch_id
        self.product_id = product_id
        self.quantity = quantity
        self.cost_price = cost_price
        self.expiration_date = expiration_date
        self.entry_date = entry_date

    def __eq__(self, other: 'Batch') -> bool:
        
        if isinstance(other, type(self)):
            return (
            other.batch_id == self.batch_id
            and other.physical_batch_id == self.physical_batch_id
            and other.product_id == self.product_id
            and other.quantity == self.quantity
            and other.cost_price == self.cost_price
            and other.expiration_date == self.expiration_date
            and other.entry_date == self.entry_date
            )