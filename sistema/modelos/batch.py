class Batch:
    def __init__(self, batch_id, physical_batch_id, product_id, quantity, cost_price, expiration_date, entry_date):
        self.batch_id = batch_id
        self.physical_batch_id = physical_batch_id
        self.product_id = product_id
        self.quantity = quantity
        self.cost_price = cost_price
        self.expiration_date = expiration_date
        self.entry_date = entry_date
