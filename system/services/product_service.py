### --- IMPORTS --- ###
from system.repositories.event_repository import EventRepository
from system.models.payloads import QuarantinePayLoad
from system.models.dtos import EventPersistenceDTO
from system.models.event_types import EventType
from datetime import datetime
from typing import Any
#######################

class ProductService:
    def __init__(self, repo: EventRepository):
        self.repo = repo

    def handle_quarantine_event(self, payload: QuarantinePayLoad):

        quarantine_dto = EventPersistenceDTO (
            timestamp = datetime.now(),
            event_type = EventType.QUARANTINE,
            user_id = None,
            product_id = payload.product_id,
            batch_id = payload.batch_id,
            details_data = payload.to_dict()
        )
        self.repo.record_event(quarantine_dto)

