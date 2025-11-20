### --- IMPORTS --- ###
from system.models.dtos import EventPersistenceDTO
from system.utils import converters
from sqlite3 import Connection
from typing import Any
########################

class EventRepository:
    'an object responsable for record an event in the layer persistence'
    
    def __init__(self, connection_db: Connection):
        self.connection_db = connection_db
    
    def _insert_table_events(self, dto: EventPersistenceDTO):
        cursor = self.connection_db.cursor()
        cursor.execute('''
            INSERT INTO events (
                timestamp,
                event_type,
                user_id,
                product_id,
                batch_id,
                details
            )
            VALUES (?, ?, ?, ?, ?, ?)
        ''',
            (
                dto.timestamp,
                dto.event_type,
                dto.user_id,
                dto.product_id,
                dto.batch_id,
                dto.details_data,
            )
        )
    
    def record_event(self, dto: EventPersistenceDTO):
        
        dto.details_data = converters.to_json(dto.details_data)
        self._insert_table_events(dto)