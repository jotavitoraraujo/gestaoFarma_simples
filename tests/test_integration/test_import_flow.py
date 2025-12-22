### --- IMPORTS --- ###
from system.services.dispatcher_service import DispatcherService
from system.models.payloads import QuarantinePayload
from system.models.event_types import EventType
from unittest.mock import MagicMock, ANY
from typing import Callable
########################


def test_dispacher_flow():

    ### --- PHASE ARRANGE --- ###
    service = DispatcherService()
    event = EventType.QUARANTINE
    payload = MagicMock(spec = QuarantinePayload)
    
    mock_handler_subscriber_correct: Callable = MagicMock()
    mock_handler_subscriber_error: Callable = MagicMock()
    mock_handler_subscriber_error.side_effect = Exception('RAISE_EXCEPTION')
    
    ### --- PHASE ACT --- ###
    service.subscribe(event, mock_handler_subscriber_error)
    service.subscribe(event, mock_handler_subscriber_correct)
    service.publish(event, payload)
    
    ### --- PHASE ASSERT --- ###
    mock_handler_subscriber_error.assert_called_once_with(payload)
    mock_handler_subscriber_correct.assert_called_once_with(payload)
    

