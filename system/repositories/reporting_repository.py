### --- IMPORTS --- ###
from sqlite3 import Connection, Cursor, Row
from datetime import date
from decimal import Decimal

class ReportingRepository:
    __slots__ = ('connection_db')
    
    def __init__(self, connection_db: Connection):
        self.connection_db = connection_db


    def dto_from_db(self, start_date: date, end_date: date) -> dict[str, Decimal] | None:

        cursor: Cursor = self.connection_db.cursor()
        cursor.execute('''
            SELECT
                COUNT(o.id) AS count_orders,
                COALESCE(SUM(o.total_value), 0) AS sum_revenue,
                COALESCE(SUM(subquery.total_items_per_order), 0) AS sum_itens_sold
            FROM orders AS o
            LEFT JOIN
                (SELECT order_id, SUM(quantity_sold) AS total_items_per_order
                FROM order_items
                GROUP BY order_id) AS subquery
            ON o.id = subquery.order_id
            WHERE o.order_date BETWEEN ? AND ?
        ''',
            (
                start_date,
                end_date,
            )
        )
        result: Row = cursor.fetchone()
        return dict(result) if result else None
