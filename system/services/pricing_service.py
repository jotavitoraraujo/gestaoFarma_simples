### --- IMPORTS --- ###
from system.repositories.cmed_repository import CMEDRepository
from system.models.product import Product
from decimal import Decimal
from typing import Any
###

class PricingService:
    def __init__(self, cmed_repo: type[CMEDRepository]):
        self.cmed_repo = cmed_repo
        self.profit: dict[str, Decimal] = {
            'SAFETY': Decimal('0.20'),
            'DEFAULT': Decimal('0.50'),
            'Biológico': Decimal('0.25'),
            'Novo': Decimal('0.25'),
            'Similar': Decimal('3.0'),
            'Genérico': Decimal('5.0')
        }

    def _to_list_dicts(self, prod: Product, final_price: Decimal, prod_type: str, capped: bool = None) -> dict[str, str | Decimal | bool | None]:
        'build a list of dicts as DTOs'

        data: dict[str, str | Decimal | bool] = {
            'ean': prod.ean,
            'cost': prod.batch[0].unit_cost_amount,
            'final_price': final_price,
            'rule_applied': prod_type,
            'capped': capped
        }
        return data

    
    def price_all_prod(self, products: list[Product]):
        'price all injected products as an argument'

        ean_list: list[str] = [prod.ean for prod in products]
        pmc_map: dict[str, tuple[Decimal, str]] = self.cmed_repo.get_pmc_map_by_eans(ean_list)
        list_dicts: list[dict] = []
        
        for prod in products:
            capped: bool = False
            
            if prod.ean in pmc_map.keys():
                pmc, prod_type = pmc_map[prod.ean]
            else:
                pmc: Any = None
                prod_type: str = 'DEFAULT'

            margin_key: str = prod_type if prod_type in self.profit.keys() else 'DEFAULT'
            margin: Decimal = self.profit[margin_key]
            target_price: Decimal = prod.batch[0].unit_cost_amount * (1 + margin + self.profit['SAFETY'])
            if pmc is not None:
                if target_price > pmc:
                    final_price: Decimal = min(target_price, pmc)
                    capped = True
                else: final_price = target_price
            dict_data: dict[str, str | Decimal | bool | None] = self._to_list_dicts(prod, final_price, prod_type, capped)
            list_dicts.append(dict_data)
        return list_dicts