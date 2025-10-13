### --- IMPORTS --- ###
from sqlite3 import Connection
from decimal import Decimal
from system.models.product import Product
from system.models.batch import Batch
from system.models.fiscal import FiscalProfile, PurchaseTaxDetails
import logging
################################

class ProductRepository:
    def __init__(self, connection_db: Connection):
        self.connection_db = connection_db
###########################################################    
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
###########################################################    
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
                max_consumer_price                    
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
###########################################################    
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
###########################################################   
    def _insert_table_batchs(self, batch: Batch, taxation_tax_details_id: int, product_id: int, status: str, reason: str):
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
                receive_date,
                status,
                quarantine_reason                                  
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                status,
                reason,
            )
        )
###########################################################
    def _update_table_batchs(self, new_quantity: Decimal, batch_id: int):
        'update the status that determine the batch as active or in quarantine'

        ###########################################################
        cursor = self.connection_db.cursor()
        cursor.execute('''
            UPDATE batchs
            SET quantity = quantity + ?
            WHERE id = ?
        ''',
            (
                new_quantity,
                batch_id,
            )
        )
###########################################################
    def _determine_batch_status(self, product: Product) -> tuple[str, str | None]:
        'determinate if a product has a attribute mandatory as none'

        result: list = []
        ##################################
        # PRODUCT VERIFY
        if not product.supplier_code:
            result.append('supplier_code')
        if not product.name:
            result.append('name')
        ##################################
        batch: Batch = product.batch[0]
        ##################################
        # BATCH VERIFY
        if not batch.physical_id:
            result.append('physical_id')
        if not batch.quantity:
            result.append('quantity')
        if not batch.unit_cost_amount:
            result.append('unit_cost_amount')
        if not batch.use_by_date:
            result.append('use_by_date')
        ##################################
        fiscal_profile: FiscalProfile = product.fiscal_profile
        ##################################
        # FISCAL PROFILE VERIFY
        if not fiscal_profile.ncm:
            result.append('ncm')
        ##################################
        taxation_details: PurchaseTaxDetails = batch.taxation_details
        ##################################
        # PURCHASE TAX DETAILS VERIFY
        if not taxation_details.cfop:
            result.append('cfop')
        ##################################

        if result:
            reason = f'[ALERT] Missing Mandatory Fields: {", ".join(result)}'
            return ('QUARANTINE', reason)
        else:
            return ('ACTIVE', None)          
###########################################################
    def _search_supplier_code(self, product: Product) -> tuple[int | None]:
        'search in db by the supplier_code from product that has receives as argument and return the product_id'

        supplier_code: str = product.supplier_code
        cursor = self.connection_db.cursor()
        cursor.execute('''
            SELECT id
            FROM products
            WHERE supplier_code = ?
        ''',
            (
                supplier_code,
            )
        )
        product_id: tuple = cursor.fetchone()
        return product_id
###########################################################
    def _search_batch_id(self, product_id: int, product: Product) -> tuple[int | None]:
        'search in db by the prod and physical id to verify your existance'

        physical_id: str = product.batch[0].physical_id
        
        cursor = self.connection_db.cursor()
        cursor.execute('''
            SELECT id
            FROM batchs
            WHERE product_id = ? AND physical_id = ? 
        ''',
            (
                product_id,
                physical_id,
            )
        )
        verification: tuple = cursor.fetchone()
        return verification
###########################################################    
    def _save_single_product(self, product: Product) -> str:
        'estructure procedural that insert just one product at a time in database, calling the private responsible methods. Returns your status to use foward'

        try:
            ###########################################################
            product_id_tuple: tuple | None = self._search_supplier_code(product)
            if product_id_tuple is None: # -> NEW PRODUCT
                ######
                fiscal_profile: FiscalProfile = product.fiscal_profile
                ######
                fiscal_profile_id: int = self._insert_table_fiscal_profile(fiscal_profile)
                product_id: int = self._insert_table_products(product, fiscal_profile_id)
            else:           # -> EXISTING
                product_id = product_id_tuple[0]
            ###########################################################
            batch = product.batch[0]
            tax_details = batch.taxation_details
            ###########################################################
            status, reason = self._determine_batch_status(product)
            batch_id_tuple: tuple = self._search_batch_id(product_id, product)
            ######
            if batch_id_tuple is None: # -> NEW BATCH
                tax_details_id = self._insert_table_purchase_tax_details(tax_details)
                self._insert_table_batchs(batch, tax_details_id, product_id, status, reason)
            else:         # -> EXISTING
                batch_id = batch_id_tuple[0] 
                new_quantity = batch.quantity
                self._update_table_batchs(new_quantity, batch_id)
            ###########################################################
            return status
        except Exception as error:
            raise error
###########################################################
    def save_products(self, list_products: list[Product]) -> dict:
        'save a many quantity of products in the table products in database'
        
        active_count = 0
        quarantined_count = 0
        
        if not list_products:
            return None
        ###########################################################
        else:
            for product in list_products:
                try:
                    status = self._save_single_product(product)
                    if status == 'ACTIVE':
                        active_count += 1
                    else:
                        quarantined_count += 1
                except Exception as error:
                    logging.error(f'[ERRO] Unexpected erro is ocurred. Verify the log: {error}')
                    continue
            return {'ACTIVE': active_count, 'QUARANTINE': quarantined_count}
        ###########################################################
