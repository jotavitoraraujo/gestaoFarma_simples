### --- IMPORTS --- ###
from sqlite3 import Connection
from system.models.product import Product
from system.models.batch import Batch
from system.models.fiscal import FiscalProfile, PurchaseTaxDetails
import logging
################################

class ProductRepository:
    def __init__(self, connection_db: Connection):
        self.connection_db = connection_db
    
    def _insert_table_fiscal_profile(self, fiscal_profile: FiscalProfile) -> int:
        cursor = self.connection_db.cursor()
        cursor.execute('''
            INSERT INTO fiscal_profile (
                ncm_code,
                cest_code,
                origin_code                        
            )
            VALUES (?, ?, ?)
            ''',
            (
                fiscal_profile.ncm,
                fiscal_profile.cest,
                fiscal_profile.origin_code,
            ))
        fiscal_profile_id: int = cursor.lastrowid
        return fiscal_profile_id
    
    def _insert_table_products(self, product: Product, fiscal_profile_id: FiscalProfile) -> int:
        cursor = self.connection_db.cursor()
        cursor.execute('''
                INSERT INTO products (
                    id_fiscal_profile,
                    supplier_code,
                    ean,
                    name_product,
                    anvisa_code,
                    sale_price,
                    max_consumer_price,
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''',
                (
                    fiscal_profile_id,
                    product.supplier_code,
                    product.ean,
                    product.name,
                    product.anvisa_code,
                    product.sale_price,
                    product.max_consumer_price,
                )
            )
        product_id: int = cursor.lastrowid
        return product_id
    
    def _insert_table_purchase_tax_details(self, taxation_tax_details: PurchaseTaxDetails) -> int:
        cursor = self.connection_db.cursor()
        cursor.execute('''
            INSERT INTO purchase_tax_details (
                cfop,
                icms_cst,
                icms_st_base_amount,
                icms_st_percentage,
                icms_st_retained_amount,
                pis_cst,
                cofins_cst
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''',
            (
                taxation_tax_details.cfop,
                taxation_tax_details.icms_cst,
                taxation_tax_details.icms_st_base_amount,
                taxation_tax_details.icms_st_percentage,
                taxation_tax_details.icms_st_retained_amount,
                taxation_tax_details.pis_cst,
                taxation_tax_details.cofins_cst,
            )
        )
        taxation_tax_details_id: int = cursor.lastrowid
        return taxation_tax_details_id
    
    def _insert_table_batchs(self, batch: Batch, taxation_tax_details_id: int, product_id: int):
        cursor = self.connection_db.cursor()
        cursor.execute('''
            INSERT INTO batchs (
                id_taxation_details,
                product_id,
                physical_id,
                quantity,
                unit_cost_amount,
                other_expenses_amount,
                use_by_date,
                manufacturing_date,
                receive_date                                    
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''',
            (
                taxation_tax_details_id,
                product_id,
                batch.physical_id,
                batch.quantity,
                batch.unit_cost_amount,
                batch.other_expenses_amount,
                batch.use_by_date,
                batch.manufacturing_date,
                batch.received_date,
            )
        )

    def save_complete_products(self, list_products: list[Product]):
        'save a many quantity of products in the table products in database'
        try:
            if not list_products:
                return None
            ###########################################################
            cursor = self.connection_db.cursor()
            for product in list_products:
                cursor.execute('''
                    SELECT id
                    FROM products
                    WHERE supplier_code = ?
                ''',
                    (
                        product.supplier_code,
                    )
                )
                response: tuple = cursor.fetchone()
            ###########################################################
                if response is not None:
                    product_id: int = response[0]
                else:
                    fiscal_profile: FiscalProfile = product.fiscal_profile
                    fiscal_profile_id: int = self._insert_table_fiscal_profile(fiscal_profile)
                    product_id: int = self._insert_table_products(product, fiscal_profile_id)
            ###########################################################
                batch: Batch = product.batch[0]
                taxation_tax_details: PurchaseTaxDetails = batch.taxation_details
                taxation_tax_details_id = self._insert_table_purchase_tax_details(taxation_tax_details)
                self._insert_table_batchs(batch, taxation_tax_details_id, product_id)
            ###########################################################
        except Exception as error:
            logging.error(f'[ERRO] Unexpected erro is ocurred. Verify the log: {error}')
            raise error