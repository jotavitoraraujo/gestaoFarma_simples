### --- IMPORTS --- ###
from sqlite3 import Connection
from decimal import Decimal
from datetime import datetime
from system.models.product import Product
from system.models.batch import Batch
from system.models.payloads import QuarantinePayLoad
from system.models.audit_event import AuditEvent
from system.models.fiscal import FiscalProfile, PurchaseTaxDetails
from system.models.dtos import EventPersistenceDTO
from system.repositories.event_repository import EventRepository
import json
import logging
################################

class ProductRepository:
    'an object construction to perform the repository pattern'
    def __init__(self, connection_db: Connection, event_repository: EventRepository):
        self.connection_db = connection_db
        self.event_repository = event_repository
    
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
   
    def _insert_table_batchs(self, batch: Batch, taxation_tax_details_id: int, product_id: int) -> int:
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
        batch_id: int = cursor.lastrowid
        return batch_id

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

    def _determine_batch_status(self, product: Product) -> tuple[str, str | None]:
        'determinate if a product has a attribute mandatory as none'

        if not product.batch:
            reason = f'[ALERT] The batch for this product is False.'
            return ('QUARANTINE', reason)  
        
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
    
    def _create_audit_event(self, product_id: int, batch_id: int, reason: str | None) -> AuditEvent:
        'create an audit_event from the status receives as argument'

        payload = QuarantinePayLoad (
            product_id = product_id, 
            batch_id = batch_id,
            reason = reason,
            emitter_cnpj = None,
            emitter_name = None
        )
        event = AuditEvent (
            id = None,
            timestamp = datetime.now(),
            event_type = 'QUARANTINE_ADDED',
            payload = payload
        )
        return event

    def _create_DTO(self, event: AuditEvent) -> EventPersistenceDTO:
        'register an event within database as a json string'
        
        payload: QuarantinePayLoad = event.payload
        payload_dict: dict = payload.to_dict()
        details_json: str = json.dumps(payload_dict)

        event_dto = EventPersistenceDTO (
            timestamp = event.timestamp,
            event_type = event.event_type,
            user_id = None,
            product_id = payload.product_id,
            batch_id = payload.batch_id,
            details_json = details_json
        )

        return event_dto

    def _get_product_id(self, product: Product) -> int:
        'get product id using private methods using the object product as argument'

        response: tuple | None = self._search_supplier_code(product)
        
        if response is None: # -> Is a new product
            fiscal_profile: FiscalProfile = product.fiscal_profile
            fiscal_profile_id: int = self._insert_table_fiscal_profile(fiscal_profile)
            product_id: int = self._insert_table_products(product, fiscal_profile_id)
        
        else: # -> is existing product
            product_id: int = response[0]
        
        return product_id

    def _get_batch_id(self, batch: Batch, tax_id: int, product_id: int) -> int:
        'get batch_id with private method using the arguments'

        batch_id: int = self._insert_table_batchs(batch, tax_id, product_id)
        return batch_id

    def _save_single_batch(self, product_id: int, product: Product) -> int | None:
        'process to saving in database a single new batch or update an existing -> returns batch_id'

        if not product.batch:
            return None
        
        batch: Batch = product.batch[0]
        taxation_tax_details: PurchaseTaxDetails = batch.taxation_details
        response: tuple | None = self._search_batch_id(product_id, product)

        if response is None: # -> is a new batch
            tax_id = self._insert_table_purchase_tax_details(taxation_tax_details)
            batch_id: int = self._get_batch_id(batch, tax_id, product_id)
        
        else: # -> is existing batch
            batch_id: int = response[0]
            new_quantity: int = batch.quantity
            self._update_table_batchs(new_quantity, batch_id)
        
        return batch_id
    
    def _save_single_product(self, product: Product) -> str:
        'process to saving a single product in database, defined the status of the same and record the result in events table'
        try:
            product_id: int = self._get_product_id(product)
            batch_id: int = self._save_single_batch(product_id, product)
            status, reason = self._determine_batch_status(product)
            
            if status == 'QUARANTINE':
                event: AuditEvent = self._create_audit_event(product_id, batch_id, reason)
                event_dto: EventPersistenceDTO = self._create_DTO(event)
                self.event_repository.record_event(event_dto)
                return status
            else:
                return status
        except Exception as error:
            raise error

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
                    if status == 'QUARANTINE':
                        quarantined_count += 1
                    else:
                        active_count += 1
                except Exception as error:
                    logging.error(f'[ERRO] Unexpected erro is ocurred. Verify the log: {error}')
                    continue
            return {'ACTIVE': active_count, 'QUARANTINE': quarantined_count}
        ###########################################################
