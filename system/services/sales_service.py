### --- IMPORTS --- ###
from system.utils.exceptions import ProductNotFoundError, InsufficientStockError
from system.repositories.sales_repository import SalesRepository
from system.services.dispatcher_service import DispatcherService
from system.services.product_service import ProductService
from system.models.item import Item
from system.models.product import Product
from system.models.batch import Batch
from decimal import Decimal

####################

class SalesService:
    def __init__(self, prod_service: ProductService, sale_repo: SalesRepository, dispatcher: DispatcherService):
        self.prod_service = prod_service
        self.sale_repo = sale_repo
        self.dispatcher = dispatcher
        self.cart: list[Item] = []

    def _create_item(self, product: Product, batch: Batch, quantity: int) -> Item:

        item = Item (
            product = product,
            batch = batch,
            quantity_sold = quantity
        )

        return item


    def start_new_sale(self):
        self.cart.clear()

    def add_item(self, ean: str, quantity: int) -> Item:
        'add item in the cart'

        product: Product = self.prod_service.find_product_by_ean(ean)
        if product is not None:
            batch: Batch = product.batch[0]
            if batch.quantity >= quantity:
                sale_item: Item = self._create_item(product, batch, quantity)
                self.cart.append(sale_item)
                return sale_item
            else: raise InsufficientStockError(f'[ERRO] Insufficient Stock. Available: {batch.quantity}')
        else: raise ProductNotFoundError(f'[ERRO] Product not Found. Verify the EAN Code. Input: {ean}')


    def get_total(self) -> Decimal:
        pass

    def finish_sale(self, payment_method: str) -> dict:
        pass