### --- IMPORTS --- ###
from datetime import datetime
from dataclasses import dataclass
import json
###############

@dataclass
class EventPersistenceDTO:
    timestamp: datetime
    event_type: str
    user_id: int | None
    product_id: int | None
    batch_id: int | None
    details_json: str