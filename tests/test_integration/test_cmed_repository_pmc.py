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
    cursor: Cursor = db_connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cmed_table (
            "EAN 1" TEXT,
            "PMC 18 %" TEXT,
            "TIPO DE PRODUTO (STATUS DO PRODUTO)"
        )
    ''')
    prod_type: str = 'DEFAULT TEST'
    list_tuple_eanANDprice: list[tuple[str, Decimal]] = [(product.ean, product.max_consumer_price, prod_type) for product in rich_products_list]
    cursor.executemany('''
        INSERT INTO cmed_table (
            "EAN 1",
            "PMC 18 %",
            "TIPO DE PRODUTO (STATUS DO PRODUTO)"
        )
        VALUES (?, ?, ?)
    ''',
        (
            list_tuple_eanANDprice
        )
    )
    db_connection.commit()
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
    result: dict[str, tuple[Decimal, str]] = cmed_repo.get_pmc_map_by_eans(list_ean)
    
    ### --- PHASE ASSERT --- ###
    assert len(result) == 3
    assert result[list_ean[0]] == (rich_products_list[0].max_consumer_price, prod_type)
    assert list_ean[0] == rich_products_list[0].ean
    print(f'\nResult of the dict: {result} \nResult of the list: {list_ean}')

    

    