### --- IMPORTS --- ###
from system.services.dispatcher_service import DispatcherService as DS
from system.repositories.cmed_repository import CMEDRepository as CR
from system.modules.cmed_importer import CMEDImporter as CI
from system.modules.cmed_parser import CMEDParser as CP
from unittest.mock import MagicMock
from sqlite3 import Connection
from threading import Thread
from pathlib import Path
import pytest
#######################

def test_cmed_import_file_not_found(db_connection: Connection):

    ## --- PHASE ARRANGE -- ##
    func_save = CR(db_connection).save_cmed
    not_found_path = Path('file_not_found.xlsx')
    dispatcher = MagicMock(DS)
    importer = CI(CP, dispatcher, func_save)

    ## -- PHASE ACT -- ##
    side_thread: Thread = importer.run_import(not_found_path)
    side_thread.join()

    ## -- PHASE ASSERT -- ##
    assert not side_thread.is_alive()
    dispatcher.publish.assert_not_called()