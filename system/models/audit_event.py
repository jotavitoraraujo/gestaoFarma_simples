### --- IMPORTS --- ###
from system.models.event_types import EventType
from datetime import datetime
from typing import Any

#########################

class AuditEvent:
    def __init__(self, id: int, timestamp: datetime, event_type: EventType, payload: Any):
        self.id = id
        self.timestamp = timestamp
        self.event_type = event_type
        self.payload = payload