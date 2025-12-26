### --- IMPORTS --- ###
from system.services.dispatcher_service import DispatcherService as DS
from system.models.event_types import EventType as ET
from unittest.mock import MagicMock
from typing import Callable
#######################

def test_dispatcher_service():

    ### -- PHASE ARRANGE -- ##
    fake_func: Callable = MagicMock()
    fake_payload: Callable = MagicMock()
    dispatcher = DS()

    ## -- PHASE ACT -- ##
    dispatcher.subscribe(ET.IMPORTATION_FINISHED, fake_func)
    dispatcher.publish(ET.IMPORTATION_FINISHED, fake_payload)

    ## -- PHASE ARRANGE -- ##
    fake_func.assert_called_once()
    fake_func.assert_called_once_with(fake_payload)