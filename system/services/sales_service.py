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
        self.cart: dict[str, Item] = {}

    def _create_item(self, product: Product, batch: Batch, quantity: int) -> Item:

        item = Item (
            product = product,
            batch = batch,
            quantity_sold = quantity
        )

        return item
    
    def _validate_stock(self, product: Product | None, quantity: int) -> bool[False | True]:

        if not product.batch: return False
        if not product.batch[0].quantity >= quantity: return False
        return True



    def start_new_sale(self):
        self.cart.clear()

    def add_item(self, ean: str, quantity: int) -> Item:
        'add item in the cart'

        if ean not in self.cart:
            product: Product = self.prod_service.find_product_by_ean(ean)
            if not product: raise ProductNotFoundError(f'[ERRO] Product not Found. Verify the EAN Code. Input: {ean}')
            if not self._validate_stock(product, quantity): raise InsufficientStockError(f'[ERRO] Insufficient Stock. Available: {product.batch[0].quantity}')
            new_item: Item = self._create_item(product, product.batch[0], quantity)
            self.cart[ean] = new_item
            return new_item
        
        else: 
            existing_item: Item = self.cart[ean]
            new_quantity: int = existing_item.quantity_sold + quantity
            if not self._validate_stock(existing_item.product, new_quantity): raise InsufficientStockError(f'[ERRO] Insufficient Stock. Available: {existing_item.product.batch[0].quantity}')
            existing_item.quantity_sold = new_quantity
            return existing_item


    def get_total(self) -> Decimal:
        pass

    def finish_sale(self, payment_method: str) -> dict:
        pass