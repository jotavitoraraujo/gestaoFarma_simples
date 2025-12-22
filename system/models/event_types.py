### --- IMPORTS --- ###
from enum import StrEnum
###############

class EventType(StrEnum):
    QUARANTINE: str = 'QUARANTINE'
    SALE_DEVIATION: str = 'SALE_DEVIATION'
    IMPORTATION_FINISHED: str = 'IMPORTATION_FINISHED'