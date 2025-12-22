### --- IMPORTS --- ###
from system.repositories.product_repository import ProductRepository
from system.repositories.event_repository import EventRepository
from system.models.payloads import QuarantinePayload
from system.models.dtos import EventPersistenceDTO
from system.models.event_types import EventType
from system.models.product import Product
from datetime import datetime
from typing import Any
#######################

class ProductService:
    def __init__(self, prod_repo: ProductRepository, event_repo: EventRepository):
        self.prod_repo = prod_repo
        self.repo = event_repo

    def handle_quarantine_event(self, payload: QuarantinePayload):

        quarantine_dto = EventPersistenceDTO (
            timestamp = datetime.now(),
            event_type = EventType.QUARANTINE,
            user_id = None,
            product_id = payload.product_id,
            batch_id = payload.batch_id,
            details_data = payload.to_dict()
        )
        self.repo.record_event(quarantine_dto)

    def find_product_by_ean(self, ean: str) -> Product | None:
        
        product: Product = self.prod_repo.find_ean(ean)
        if product is not None:
            return product
        else:
            return None
