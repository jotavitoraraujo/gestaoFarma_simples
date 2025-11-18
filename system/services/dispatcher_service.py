### --- IMPORTS --- ###
from system.models.event_types import EventType
from typing import Callable, Any
import logging
###############

class DispatcherService:
    def __init__(self):
        self.subscribers: dict = {}

    def subscribe(self, event: EventType, handler: Callable) -> None:
        
        if event not in self.subscribers: 
            self.subscribers[event] = set()
        
        self.subscribers[event].add(handler)

    def publish(self, event: EventType, payload: Any) -> None:

        if not self.subscribers.get(event):
            logging.error('[ERRO] This subscribe does not exists or not found.')
        
        else:
            for handler in self.subscribers[event]:
                handler(payload)