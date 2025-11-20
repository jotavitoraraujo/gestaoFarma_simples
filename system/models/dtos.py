### --- IMPORTS --- ###
from system.models.event_types import EventType
from datetime import datetime
from dataclasses import dataclass
from typing import Any
###############

@dataclass
class EventPersistenceDTO:
    timestamp: datetime
    event_type: EventType
    user_id: int | None
    product_id: int | None
    batch_id: int | None
    details_data: Any