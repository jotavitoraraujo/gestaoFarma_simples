### --- IMPORTS --- ###
from decimal import Decimal
##########
# --- PROFILE (THIS IS A FISCAL PROFILE) --- #
class FiscalProfile:
    def __init__(self,
        id: int,
        ncm: str,
        cest: str,
        origin_code: str,
    ):
        'create a Profile class'

        self.id = id
        self.ncm = ncm
        self.cest = cest
        self.origin_code = origin_code

    def __eq__(self, other: 'FiscalProfile') -> bool:
        'dunder method for comparassion the of Profile object'

        if isinstance(other, type(self)):
            return (
            other.id == self.id
            and other.ncm == self.ncm
            and other.cest == self.cest
            and other.origin_code == self.origin_code
            )
        else:
            return False
        
    def __repr__(self) -> str:
        'print in terminal the status for fiscal profile of this object'

        return f'''
        --- Profile Fiscal ---
        1. ID Fiscal Profile: {self.id}
        2. NCM Code: {self.ncm}
        3. CEST Code: {self.cest}
        4. ORIGIN Code: {self.origin_code}
        '''
    
##########
# --- TRANSACTIONAL DATA (INPUT OF A FISCAL DATA IN THE STOCK) --- #
class PurchaseTaxDetails:
    
    def __init__(self,
        id: int,
        cfop: str,
        icms_cst: str,
        icms_st_base_amount: Decimal,
        icms_st_percentage: Decimal,
        icms_st_retained_amount: Decimal,
        pis_cst: str,
        cofins_cst: str
    ):
        'create a class to controling input taxation at a nf-e'
    
        self.id = id
        self.cfop = cfop
        self.icms_cst = icms_cst
        self.icms_st_base_amount = icms_st_base_amount
        self.icms_st_percentage = icms_st_percentage
        self.icms_st_retained_amount = icms_st_retained_amount
        self.pis_cst = pis_cst
        self.cofins_cst = cofins_cst

    def __eq__(self, other: 'PurchaseTaxDetails') -> bool:
        'dunder method for comparassion the of PurchaseTaxDetails object'

        if isinstance(other, type(self)):
            return (
                other.id == self.id
                and other.cfop == self.cfop
                and other.icms_cst == self.icms_cst
                and other.icms_st_base_amount == self.icms_st_base_amount
                and other.icms_st_percentage == self.icms_st_percentage
                and other.icms_st_retained_amount == self.icms_st_retained_amount
                and other.pis_cst == self.pis_cst
                and other.cofins_cst == self.cofins_cst
            )
        else:
            return False
    
    def __repr__(self) -> str:
        'print in terminal the status for fiscal data in input taxtional of this object'

        return f'''
        --- Purchase Tax Details ---
        1. ID Purchase: {self.id}
        2. CFOP: {self.cfop}
        3. ICMS CST: {self.icms_cst}
        4. ICMS Base Value: {self.icms_st_base_amount}
        5. ICMS Percentage: {self.icms_st_percentage}
        6. ICMS Value: {self.icms_st_retained_amount}
        7. PIS CST: {self.pis_cst}
        8. COFINS CST: {self.cofins_cst}
        '''
