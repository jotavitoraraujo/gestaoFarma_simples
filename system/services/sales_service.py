### --- IMPORTS --- ###
from system.utils.exceptions import ProductNotFoundError, InsufficientStockError, CartEmptyError
from system.repositories.sales_repository import SalesRepository
from system.services.dispatcher_service import DispatcherService
from system.services.product_service import ProductService
from system.models.product import Product
from system.models.batch import Batch
from system.models.item import Item
from decimal import Decimal
from datetime import date

####################

class SalesService:
    __slots__ = (
        'prod_service',
        'sale_repo',
        'dispatcher',
        'cart'
    )
    
    def __init__(self, prod_service: ProductService, sale_repo: SalesRepository, dispatcher: DispatcherService):
        self.prod_service = prod_service
        self.sale_repo = sale_repo
        self.dispatcher = dispatcher
        self.cart: dict[str, Item] = {}

    def _create_item(self, product: Product, fifo: list, quantity: Decimal) -> Item:

        item = Item (
            product = product,
            fifo = fifo,
            quantity_sold = quantity
        )

        return item
    
    def _validate_stock(self, product: Product, quantity: Decimal) -> bool:

        batchs: list[Batch] = product.batch
        total_batch_qty: Decimal = sum((b.quantity for b in batchs))

        if not product.batch: return False
        if not total_batch_qty >= quantity: return False
        return True

    def _fifo_algorithm(self, product: Product, qty_desired: Decimal) -> list[dict[str, int | Decimal]]:

        to_repository: list[dict[str, int | Decimal]] = []
        batchs: list[Batch] = product.batch
        total_batch_qty = Decimal(f'{sum((b.quantity for b in batchs))}')
        
        if not total_batch_qty >= qty_desired: raise InsufficientStockError(f'[ERRO] Insufficient Stock. Available: {product.batch[0].quantity}')

        for batch in batchs:
            if batch.quantity > 0:
                amount_taken: Decimal = min(batch.quantity, qty_desired)
                to_repository.append({'BATCH_ID': batch.id, 'QUANTITY': amount_taken})
                batch.quantity -= amount_taken
                qty_desired -= amount_taken
                if qty_desired == 0: break
        
        return to_repository


    def start_new_sale(self):
        self.cart.clear()

    def add_item(self, ean: str, quantity: Decimal) -> Item:
        'add item in the cart'

        if ean not in self.cart:
            product: Product = self.prod_service.find_product_by_ean(ean)
            if not product: raise ProductNotFoundError(f'[ERRO] Product not Found. Verify the EAN Code. Input: {ean}')
            if not self._validate_stock(product, quantity): raise InsufficientStockError(f'[ERRO] Insufficient Stock. Available: {product.batch[0].quantity}')
            fifo: list[dict[str, int | Decimal]] = self._fifo_algorithm(product, quantity)
            new_item: Item = self._create_item(product, fifo, quantity)
            self.cart[ean] = new_item
            return new_item
        
        else: 
            existing_item: Item = self.cart[ean]
            new_quantity: Decimal = existing_item.quantity_sold + quantity
            if not self._validate_stock(existing_item.product, new_quantity): raise InsufficientStockError(f'[ERRO] Insufficient Stock. Available: {existing_item.product.batch[0].quantity}')
            fifo: list[dict[str, int | Decimal]] = self._fifo_algorithm(existing_item.product, quantity)
            existing_item.fifo.extend(fifo)
            existing_item.quantity_sold = new_quantity
            return existing_item

    def get_total(self) -> Decimal:
        
        total = Decimal('0.00')
        for item in self.cart.values():
            total += item.calculate_subtotal()
        return total

    def finish_sale(self, user_id: int | None)  -> None:
        
        if not self.cart: raise CartEmptyError(f'[ERROR] Cart is empty.', self.cart)

        to_repository: dict[str, int | None | date | Decimal | list[Item]] = {
            'USER_ID': user_id,
            'DATE': date.today(),
            'TOTAL_VALUE': self.get_total(),
            'ITEMS': [{'PRODUCT_ID': item.product.id, 'SALE_PRICE': item.product.sale_price, 'ALLOCATIONS': item.fifo} for item in self.cart.values()]
        }
        self.sale_repo.save_sale(to_repository)
        self.start_new_sale()