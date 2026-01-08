### --- IMPORTS --- ###
from system.repositories.cmed_repository import CMEDRepository as CR
from system.services.pricing_service import PricingService as PS
from system.models.product import Product
from system.models.batch import Batch
from unittest.mock import MagicMock
from sqlite3 import Connection
from decimal import Decimal
import pytest
###

def test_pricing_service():

    ## -- PHASE ARRANGE -- ##
    cmed_repo_mock = MagicMock(spec = CR)
    pricing_service = PS(cmed_repo_mock)

    prod = MagicMock(spec = Product)
    prod.ean = '123' # CONFIG EAN
    batch = MagicMock(spec = Batch)
    batch.unit_cost_amount = Decimal('10.00') # CONFIG COST
    prod.batch = [batch]
    pmc = Decimal('100.00') # CONFIG PMC
    prod_type: str = 'X' # COFIG PROD TYPE
    target_price: str = '62.00' # CONFIG TARGET PRICE

    cmed_repo_mock.get_pmc_map_by_eans.return_value = {}

    ## -- PHASE ACT -- ##
    result: list[dict] = pricing_service.price_all_prod([prod])
    
    ## -- PHASE ARRANGE 2 -- ##
    data: dict = result[0]

    ## -- PHASE ASSERT -- ##
    assert len(result) == 1
    assert data['ean'] == '123'
    assert data['rule_applied'] == 'DEFAULT'
    assert data['capped'] is False
    assert data['final_price'] == Decimal(f'17.00')