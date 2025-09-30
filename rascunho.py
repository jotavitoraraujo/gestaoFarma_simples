from sqlite3 import Connection
from system import database
from system.models.product import Product
from system.models.batch import Batch


def test_save_products(db_connection: Connection, expected_list_products: list[Product], expected_list_products_dip_diff: list[Product]):

    database.create_tables(db_connection)
    database.save_products(db_connection, expected_list_products)
    cursor = db_connection.cursor()
    cursor.execute('''
        SELECT *
        FROM produtos
        JOIN lotes
        ON produtos.id = lotes.produto_id        
    ''')
    result = cursor.fetchall()
    result_list = []
    for item in result:
        product_instance = Product (
            id = item[0],
            supplier_code = item[1],
            ean = item[3],
            name = item[2],
            sale_price = item[4]           
        )
        ### --- INSTANCE EXPIRATION DATE --- ###
        object_expiration_date = item[12]
        ########################################
        batch_instance = Batch (
            batch_id = item[7],
            physical_batch_id = item[8],
            product_id = item[9],
            quantity = item[10],
            cost_price = item[11],
            expiration_date = object_expiration_date,
            entry_date = item[13]
        )
        product_instance.batch.append(batch_instance)
        result_list.append(product_instance)

    database.save_products(expected_list_products_dip_diff)