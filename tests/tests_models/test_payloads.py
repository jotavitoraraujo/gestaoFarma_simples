### --- IMPORTS --- ###
from system.models.payloads import ImportationFinishedPayload as IFP
#######################

def test_importationPayload():

    ## -- PHASE ARRANGE -- ##
    status: str = 'SUCESS'
    file_name: str = 'test_file.xlsx'
    total_records: int = 1

    ## -- PHASE ACT -- ##
    payload = IFP (
        status = status,
        file_name = file_name,
        total_records = total_records
    )

    ## -- PHASE ASSERT -- ##
    assert payload.status == status
    assert hasattr(payload, 'status')
    assert hasattr(payload, 'file_name')
    assert hasattr(payload, 'total_records')
    assert isinstance(payload.total_records, int)
    assert isinstance(payload.status, str)