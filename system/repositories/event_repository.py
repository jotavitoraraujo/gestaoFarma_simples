### --- IMPORTS --- ###
from sqlite3 import Connection
from system.models.dtos import EventPersistenceDTO
########################

class EventRepository:
    'an object responsable for record an event in the layer persistence'
    
    def __init__(self, connection_db: Connection):
        self.connection_db = connection_db
    
    def _insert_table_events(self, event_dto: EventPersistenceDTO):
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
                event_dto.timestamp,
                event_dto.event_type,
                event_dto.user_id,
                event_dto.product_id,
                event_dto.batch_id,
                event_dto.details_json,
            )
        )
    
    def record_event(self, event_dto):
        self._insert_table_events(event_dto)