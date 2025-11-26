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
            logging.warning(f'[AVISO] No subscribers found for event: {event}')
            return
        else:
            for handler in self.subscribers[event]:
                try:
                    handler(payload)
                except Exception as error:
                    handler_name: str = getattr(handler, '__name__', str(handler))
                    logging.error(f'=' * 30)
                    logging.error(f'[ERRO] Fail send the event: {event}.')
                    logging.error(f'Subscriber: {handler_name}')
                    logging.error(f'Reason: {error}')
                    logging.error(f'=' * 30)