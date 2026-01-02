### --- IMPORTS --- ###
from system.repositories.product_repository import ProductRepository
from system.repositories.cmed_repository import CMEDRepository
from unittest.mock import MagicMock, _patch, patch
from system.models.product import Product
from sqlite3 import Connection, Cursor
from system import database as db
from decimal import Decimal
###

@patch('system.repositories.cmed_repository.CMEDRepository._define_chunksize')
def test_chunking_capacity(mockfunc_define_chunksize, db_connection: Connection, rich_products_list: list[Product]):

    ### --- PHASE ARRANGE --- ###
    db.starter_schema(db_connection)
    prod_repo = ProductRepository(db_connection)
    prod_repo.save_products(rich_products_list)
    cmed_repo = CMEDRepository(db_connection)
    mockfunc_define_chunksize.return_value = 1
    cursor: Cursor = db_connection.cursor()
    cursor.execute('''
        SELECT ean
        FROM products
    ''')
    list_ean: list[str] = [row[0] for row in cursor.fetchall()]
    
    ### --- PHASE ACT --- ###
    result: dict[str, Decimal] = cmed_repo.get_pmc_map_by_eans(list_ean)
    assert len(result) == 3


    

    