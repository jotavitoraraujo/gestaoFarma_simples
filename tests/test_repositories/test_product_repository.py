### --- IMPORTS --- ###
from sqlite3 import Connection
from datetime import date
from system import database
from decimal import Decimal
from system.models.product import Product
from system.models.batch import Batch
from system.models.fiscal import FiscalProfile, PurchaseTaxDetails
from system.repositories.product_repository import ProductRepository
#######################

def test_prod_repo_complete_products(db_connection: Connection, rich_products_list: list[Product]):

    #### --- PHASE ARRANGE --- ####
    database.create_tables(db_connection)
    repo = ProductRepository(db_connection)
    repo.save_complete_products(rich_products_list)
    cursor = db_connection.cursor()
    
    ### --- PHASE ACT TO PRODUCTS --- ###
    cursor.execute('''
        SELECT *
        FROM products
    ''')
    response_products: tuple = cursor.fetchall()
    response_clinda: Product = response_products[0]
    response_broma: Product = response_products[1]
    response_cele: Product = response_products[2]

    ############ ASSERTION TO DATA OF PRODUCTS IN TABLE PRODUCTS #############
    #### PRODUCT CLINDAMINCINA
    assert response_clinda[0] == 1 # ID Product
    assert response_clinda[1] == 1 # ID Fiscal Profile
    assert response_clinda[2] == '0101465' # Supplier Code
    assert response_clinda[3] == '7896112196846' # EAN
    assert response_clinda[4] == 'Clindamin-c 300mg 16cps (clindamicina) / Teuto Farma / *(1,2)' # Name
    assert response_clinda[5] == '1037006270012' # Anvisa Code
    assert response_clinda[6] == None # Sale Price
    assert response_clinda[7] == Decimal('93.47') # Max Consumer Price
    assert response_clinda[8] == None # Min Stock
    assert response_clinda[9] == None # Curva ABC
    #### PRODUCT BROMAZEPAN
    assert response_broma[0] == 2
    assert response_broma[1] == 2
    assert response_broma[2] == '0102122'
    assert response_broma[3] == '7896112113843'
    assert response_broma[4] == 'Bromazepam 6mg 30cpr Gen / Teuto Gen. / *(1,2)'
    assert response_broma[5] == '1037004950067'
    assert response_broma[6] == None
    assert response_broma[7] == Decimal('30.84')
    assert response_broma[8] == None
    #### PRODUCT CELECOXIBE
    assert response_cele[0] == 3
    assert response_cele[1] == 3
    assert response_cele[2] == '0102240'
    assert response_cele[3] == '7896112106470'
    assert response_cele[4] == 'Celecoxibe 200mg 10cps Gen / Teuto Gen. / *(1,2)'
    assert response_cele[5] == '1037005980091'
    assert response_cele[6] == None
    assert response_cele[7] == Decimal('43.13')
    assert response_cele[8] == None
    #######################################################################
    #### --- PHASE ACT TO FISCAL PROFILES OF PRODUCTS --- ###
    cursor.execute('''
        SELECT *
        FROM fiscal_profile
    ''')
    response_fiscal: tuple = cursor.fetchall()
    fiscal_clinda: FiscalProfile = response_fiscal[0]
    fiscal_broma: FiscalProfile = response_fiscal[1]
    fiscal_cele: FiscalProfile = response_fiscal[2]
    
    #### --- PHASE ASSERTION TO DATA OF FISCAL PROFILES FROM PRODUCTS --- ####
    #### FISCAL PROFILE FROM CLINDAMIDA
    assert fiscal_clinda[0] == 1 # ID Fiscal Profile
    assert fiscal_clinda[1] == '30049099' # NCM Code
    assert fiscal_clinda[2] == '1300300' # CEST Code
    assert fiscal_clinda[3] == '0' # Origin Code
    #### FISCAL PROFILE FROM BROMAZEPAN
    assert fiscal_broma[0] == 2
    assert fiscal_broma[1] == '30049064'
    assert fiscal_broma[2] == '1300200'
    assert fiscal_broma[3] == '0'
    #### FISCAL PROFILE FROM CELECOXIBE
    assert fiscal_cele[0] == 3
    assert fiscal_cele[1] == '30049079'
    assert fiscal_cele[2] == '1300200'
    assert fiscal_cele[3] == '0'
    #######################################################################
    #### --- PHASE ACT TO BATCH OF PRODUCTS --- ####
    cursor.execute('''
        SELECT *
        FROM batchs
    ''')
    response_batchs: tuple = cursor.fetchall()
    batch_clinda: Batch = response_batchs[0]
    batch_broma: Batch = response_batchs[1]
    batch_cele: Batch = response_batchs[2]

    #### --- PHASE ASSERTION TO DATA OF BATCHS FROM PRODUCTS --- ####
    #### BATCH FROM CLINDAMICINA PRODUCT
    assert batch_clinda[0] == 1 # ID Batch
    assert batch_clinda[1] == 1 # ID Taxation Tax Details
    assert batch_clinda[2] == 1 # ID Product
    assert batch_clinda[3] == '9684081' # ID Physical
    assert batch_clinda[4] == Decimal('2.0') # Quantity
    assert batch_clinda[5] == Decimal('14.59') # Unit Cost
    assert batch_clinda[6] == Decimal('2.95') # Other Expenses
    assert batch_clinda[7] == date(2045, 8, 31)
    assert batch_clinda[8] == date(2035, 8, 31)
    assert batch_clinda[9] == date.today()
    #assert batch_clinda[10] == None
    #### BATCH FROM BROMAZEPAN PRODUCT
    assert batch_broma[0] == 2
    assert batch_broma[1] == 2
    assert batch_broma[2] == 2
    assert batch_broma[3] == '1384218'
    assert batch_broma[4] == Decimal('4.0')
    assert batch_broma[5] == Decimal('3.99')
    assert batch_broma[6] == Decimal('0.96')
    assert batch_broma[7] == date(2045, 8, 31)
    assert batch_broma[8] == date(2035, 8, 31)
    assert batch_broma[9] == date.today()
    #### BATCH FROM CELECOXIBE PRODUCT
    assert batch_cele[0] == 3
    assert batch_cele[1] == 3
    assert batch_cele[2] == 3
    assert batch_cele[3] == '46470014'
    assert batch_cele[4] == Decimal('3.0')
    assert batch_cele[5] == Decimal('5.59')
    assert batch_cele[6] == Decimal('1.00')
    assert batch_cele[7] == date(2045, 8, 31)
    assert batch_cele[8] == date(2035, 8, 31)
    assert batch_cele[9] == date.today()
    #######################################################################
    #### --- PHASE ACT TO TAXATION TAX DETAILS --- ####
    cursor.execute('''
        SELECT *
        FROM purchase_tax_details
    ''')
    response_purchase: tuple = cursor.fetchall()
    purchase_clinda: PurchaseTaxDetails = response_purchase[0]
    purchase_broma: PurchaseTaxDetails = response_purchase[1]
    purchase_cele: PurchaseTaxDetails = response_purchase[2]
    #### --- PHASE ASSERTION TO DATA OF PURCHASE TAX DETAILS FROM BATCH OF PRODUCTS --- ####
    #### TAXATION TAX DETAILS CLINDAMIDA ####
    assert purchase_clinda[0] == 1
    assert purchase_clinda[1] == '5405'
    assert purchase_clinda[2] == '60'
    assert purchase_clinda[3] == Decimal('43.86')
    assert purchase_clinda[4] == Decimal('18.00')
    assert purchase_clinda[5] == Decimal('2.57')
    assert purchase_clinda[6] == '04'
    assert purchase_clinda[7] == '04'
    #### TAXATION TAX DETAILS BROMAZEPAN ####
    assert purchase_broma[0] == 2
    assert purchase_broma[1] == '5405'
    assert purchase_broma[2] == '60'
    assert purchase_broma[3] == Decimal('22.35')
    assert purchase_broma[4] == Decimal('12.00')
    assert purchase_broma[5] == Decimal('0.75')
    assert purchase_broma[6] == '04'
    assert purchase_broma[7] == '04'
    #### TAXATION TAX DETAILS CELECOXIBE ####
    assert purchase_cele[0] == 3
    assert purchase_cele[1] == '5405'
    assert purchase_cele[2] == '60'
    assert purchase_cele[3] == Decimal('23.49')
    assert purchase_cele[4] == Decimal('12.00')
    assert purchase_cele[5] == Decimal('0.78')
    assert purchase_cele[6] == '04'
    assert purchase_cele[7] == '04'
    #######################################################################
    #### --- PHASE ARRANGE FOR SELECT AND PUT IT ALL TOGETHER --- ####
    cursor.execute('''
        SELECT *
        FROM products
        JOIN fiscal_profile ON products.id_fiscal_profile = fiscal_profile.id
        JOIN batchs ON products.id = batchs.product_id
        JOIN purchase_tax_details ON batchs.id_taxation_details = purchase_tax_details.id
        WHERE products.id = 1
    ''')
    response_complete: tuple = cursor.fetchone()
    #######################################################################
    product = Product (
        id = response_complete[0],
        supplier_code = response_complete[2],
        ean = response_complete[3],
        name = response_complete[4],
        anvisa_code = response_complete[5],
        sale_price = response_complete[6],
        max_consumer_price = response_complete[7],
        fiscal_profile = None
    )
    #######################################################################
    fiscal_profile = FiscalProfile (
        id = response_complete[10],
        ncm = response_complete[11],
        cest = response_complete[12],
        origin_code = response_complete[13]
    )
    #######################################################################
    batch = Batch (
        id = response_complete[14],
        product_id = response_complete[16],
        physical_id = response_complete[17],
        quantity = response_complete[18],
        unit_cost_amount = response_complete[19],
        other_expenses_amount = response_complete[20],
        use_by_date = response_complete[21],
        manufacturing_date = response_complete[22],
        received_date = response_complete[23],
        taxation_details = None
    )
    #######################################################################
    taxation_details = PurchaseTaxDetails (
        id = response_complete[24],
        cfop = response_complete[25],
        icms_cst = response_complete[26],
        icms_st_base_amount = response_complete[27],
        icms_st_percentage = response_complete[28],
        icms_st_retained_amount = response_complete[29],
        pis_cst = response_complete[30],
        cofins_cst = response_complete[31]
    )
    #######################################################################
    product.fiscal_profile = fiscal_profile
    batch.taxation_details = taxation_details
    product.batch.append(batch)
    #######################################################################
    #### --- PHASE ARRANGE TO ASSERTION --- ####
    clindamicina_db: Product = product
    clindamicina_list: Product = rich_products_list[0]
    clindamicina_list.id = 1
    clindamicina_list.fiscal_profile.id = 1
    clindamicina_list.batch[0].id = 1
    clindamicina_list.batch[0].product_id = 1
    clindamicina_list.batch[0].taxation_details.id = 1
    #### --- ASSERTION TO SEE IF THE DATABASE RETURN WILL BUILD THE SAME PRODUCT AS THE ARGUMENT LIST --- ####
    assert clindamicina_db == clindamicina_list
    assert clindamicina_db.batch == clindamicina_list.batch
