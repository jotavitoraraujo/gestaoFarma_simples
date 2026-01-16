### --- IMPORTS --- ###
from system.utils.exceptions import InsufficientStockError
from sqlite3 import Connection, Cursor
from system.models.item import Item
from decimal import Decimal
from datetime import date

class SalesRepository:
    __slots__ = (
        'connection_db',
    )
    
    def __init__(self, connection_db: Connection):
        self.connection_db = connection_db

    def _insert_orders_table(self, user_id: int, date: date, total_value: Decimal) -> int:
        
        cursor: Cursor = self.connection_db.cursor()
        cursor.execute('''
            INSERT INTO orders (
                user_id,
                order_date,
                total_value
            )
            VALUES (?, ?, ?)
        ''',
            (
                user_id,
                date,
                total_value,
            )
        )
        order_id: int = cursor.lastrowid
        return order_id
    
    def _insert_order_items_table(self, order_id: int, batch_id: int, sale_price: Decimal, quantity_sold: Decimal) -> None:
        
        cursor: Cursor = self.connection_db.cursor()
        cursor.execute('''
            INSERT INTO order_items (
                order_id,
                batch_id,
                sale_price_register,
                quantity_sold
            )
            VALUES (?, ?, ?, ?)
        ''',
            (
                order_id,
                batch_id,
                sale_price,
                quantity_sold,
            )
        )

    def _update_batch_table(self, quantity_sold: Decimal, batch_id: int):

        cursor: Cursor = self.connection_db.cursor()
        cursor.execute('''
            UPDATE batchs
            SET quantity = quantity - ?
            WHERE id = ? AND quantity >= ?
        ''',
            (
                quantity_sold,
                batch_id,
                quantity_sold,
            )
        )
        row_batch_count: int = cursor.rowcount
        if row_batch_count == 0: raise InsufficientStockError(f'[ERRO] Insufficient Stock to updated.')
    
    def _process_items(self, order_id: int, items_dict: dict[str, int | Decimal | list]):

        list_fifo: list[dict[str, int | Decimal]] = items_dict['ALLOCATIONS']
        for fifo in list_fifo:
            self._insert_order_items_table(order_id, fifo['BATCH_ID'], items_dict['SALE_PRICE'], fifo['QUANTITY'])
            self._update_batch_table(fifo['QUANTITY'], fifo['BATCH_ID'])
    
    def save_sale(self, to_repository: dict[str, int | date | Decimal]) -> None:
        'record a sale and update the inventory'

        user_id: int = to_repository['USER_ID']
        time: date = to_repository['DATE']
        total_value: Decimal = to_repository['TOTAL_VALUE']        
        order_id: int = self._insert_orders_table(user_id, time, total_value)
        
        for items_dict in to_repository['ITEMS']:
            self._process_items(order_id, items_dict)