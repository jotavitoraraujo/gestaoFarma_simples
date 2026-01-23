### --- IMPORTS --- ###
from system.repositories.reporting_repository import ReportingRepository
from decimal import Decimal
from datetime import date

class ReportingService:
    __slots__ = ('report_repo')
    
    def __init__(self, report_repo: ReportingRepository):
        self.report_repo = report_repo

    def _verify_dates(self, start_date: date, end_date: date) -> tuple[date, date]:
        'verify if the dates they are inverted'

        if start_date <= end_date:
            return start_date, end_date
        else: 
            swap_start_date = end_date
            swap_end_date = start_date
            return  swap_start_date, swap_end_date
        
    def _receive_info(self, start_date: date, end_date: date) -> dict[str, Decimal]:

        info: dict[str, Decimal] = self.report_repo.dto_from_db(start_date, end_date)
        return info
    
    def _calculate_mid_ticket(self, info: dict[str, Decimal]) -> dict[str, Decimal]:

        if info['count_orders'] > 0:
            mid_ticket: Decimal = info['sum_revenue'] / info['count_orders']
            info['mid_ticket'] = mid_ticket
            return info
        else: 
            info['mid_ticket'] = Decimal('0.00')
            return info

    def daily_report(self, start_date: date, end_date: date) -> dict[str, Decimal]:

        dates: tuple[date, date] = self._verify_dates(start_date, end_date)
        info: dict[str, Decimal] = self._receive_info(dates[0], dates[1])
        info: dict[str, Decimal] = self._calculate_mid_ticket(info)
        to_UI: dict[str, Decimal] = {
            'orders': Decimal(f'{info['count_orders']}'),
            'revenue': Decimal(f'{info['sum_revenue']}'),
            'total_items_sold': Decimal(f'{info['sum_itens_sold']}'),
            'mid_ticket': Decimal(f'{info['mid_ticket']}')
        }
        return to_UI



        
            
        

