#### --- IMPORTS --- ####
from system.models.fiscal import FiscalProfile, PurchaseTaxDetails
from decimal import Decimal

### --- SUITE TEST TO FISCAL PROFILE --- ###
### --- INSTANCE --- ###
### --- ARRANGE/ACT PHASE --- ###
fiscal_profile_A = FiscalProfile (
    id = 1,
    ncm = '1234',
    cest = '1234',
    origin_code = '1234' 
)

fiscal_profile_B = FiscalProfile (
    id = 1,
    ncm = '1234',
    cest = '1234',
    origin_code = '1234' 
)

fiscal_profile_C = FiscalProfile (
    id = 1,
    ncm = '12345',
    cest = '12345',
    origin_code = '12345' 
)

repr_string = f'''
        --- Profile Fiscal ---
        1. ID Fiscal Profile: {fiscal_profile_A.id}
        2. NCM Code: {fiscal_profile_A.ncm}
        3. CEST Code: {fiscal_profile_A.cest}
        4. ORIGIN Code: {fiscal_profile_A.origin_code}
        '''

repr_real = repr(fiscal_profile_A)

### --- ASSERT __INIT__ PHASE --- ###
def test_fiscaL_profile_construction():
    assert fiscal_profile_A.id == 1
    assert fiscal_profile_A.ncm == '1234'
    assert fiscal_profile_A.cest == '1234'
    assert fiscal_profile_A.origin_code == '1234'

### --- ASSERT __EQ__ PHASE --- ###
def test_fiscal_profile_equality():
    assert fiscal_profile_A == fiscal_profile_A
    assert fiscal_profile_A == fiscal_profile_B
    assert fiscal_profile_A != fiscal_profile_C

### --- ASSERT __REPR__ PHASE --- ###
def test_fiscal_profile_representation():
    assert repr_string == repr_real

###########################
### --- SUITE TEST TO PURCHASE_TAX_DETAILS --- ###
### --- INSTANCE --- ###
### --- ARRANGE/ACT --- ###

purchase_tax_details_A = PurchaseTaxDetails (
    id = 1,
    cfop = '1234',
    icms_cst = '1234',
    icms_st_base_amount = Decimal('0.1'),
    icms_st_percentage = Decimal('0.2'),
    icms_st_retained_amount = Decimal('0.3'),
    pis_cst = '1234',
    cofins_cst = '1234'
)

purchase_tax_details_B = PurchaseTaxDetails (
    id = 1,
    cfop = '1234',
    icms_cst = '1234',
    icms_st_base_amount = Decimal('0.1'),
    icms_st_percentage = Decimal('0.2'),
    icms_st_retained_amount = Decimal('0.3'),
    pis_cst = '1234',
    cofins_cst = '1234'
)

purchase_tax_details_C = PurchaseTaxDetails (
    id = 1,
    cfop = '1234',
    icms_cst = '1234',
    icms_st_base_amount = Decimal('0.2'),
    icms_st_percentage = Decimal('0.3'),
    icms_st_retained_amount = Decimal('0.4'),
    pis_cst = '1234',
    cofins_cst = '1234'
)

repr_string_2 = f'''
        --- Purchase Tax Details ---
        1. ID Purchase: {purchase_tax_details_A.id}
        2. CFOP: {purchase_tax_details_A.cfop}
        3. ICMS CST: {purchase_tax_details_A.icms_cst}
        4. ICMS Base Value: {purchase_tax_details_A.icms_st_base_amount}
        5. ICMS Percentage: {purchase_tax_details_A.icms_st_percentage}%
        6. ICMS Value: {purchase_tax_details_A.icms_st_retained_amount}
        7. PIS CST: {purchase_tax_details_A.pis_cst}
        8. COFINS CST: {purchase_tax_details_A.cofins_cst}
        '''

repr_real_2 = repr(purchase_tax_details_A)

### --- ASSERT __INIT__ PHASE --- ###
def test_purchase_tax_details_constrution():
    assert purchase_tax_details_A.id == 1
    assert purchase_tax_details_A.cfop == '1234'
    assert purchase_tax_details_A.icms_cst == '1234'
    assert purchase_tax_details_A.icms_st_base_amount == Decimal('0.1')
    assert purchase_tax_details_A.icms_st_percentage == Decimal('0.2')
    assert purchase_tax_details_A.icms_st_retained_amount == Decimal('0.3')
    assert purchase_tax_details_A.pis_cst == '1234'
    assert purchase_tax_details_A.cofins_cst =='1234'

### --- ASSERT __EQ__ PHASE --- ###
def test_purchase_tax_details_equality():
    assert purchase_tax_details_A == purchase_tax_details_A
    assert purchase_tax_details_A == purchase_tax_details_B
    assert purchase_tax_details_A != purchase_tax_details_C

### --- ASSERT __REPR__ PHASE --- ###
def test_purchase_tax_details_representation():
    assert repr_string_2 == repr_real_2