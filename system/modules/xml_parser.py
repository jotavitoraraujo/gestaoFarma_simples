######## --- IMPORTS --- ########
from system.models.product import Product
from system.models.batch import Batch
from system.models.fiscal import FiscalProfile, PurchaseTaxDetails
from system.utils.exceptions import MissingTagError, ConversionError
from datetime import date
from decimal import Decimal, InvalidOperation
import xml.etree.ElementTree as ET
import logging
#################################

class XMLParser:
    def __init__(self, xml_content: str):
        self.xml_content: str = xml_content
        self.list_complete_products: list = []
        self.list_quarantine_products: list[tuple] = []
        self.list_errors: list = []

    def _extract_xml_data(self) -> ET.Element:
        'extract data of the xml and transform he at a object ET as root for the use'

        if self.xml_content is not None:
            if isinstance(self.xml_content, str):
                root_element: ET.Element = ET.fromstring(self.xml_content)
                return root_element
        else:
            return None
    
    ###########
    def _extract_dets(self, root_element: ET.Element) -> list[ET.Element]:
        '''
        create a list of the ET objects from argument this function and returns an list of the knots for the tratament
        use with a for loop provide the control variable a single knot det to no broken the data flow in next functions
        '''
        
        if isinstance(root_element, ET.Element):
            name_space = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
            list_dets: list[ET.Element] = root_element.findall('.//nfe:det', name_space)
            return list_dets
        else:
            None

    ###########
    def _find_tags(self, det: ET.Element) -> dict:
        'find and pull of this knot det, all tags that will make use to Product instance and returns an dictionary'
        
        if isinstance(det, ET.Element):
            #############################################################################
            # -- EXTRACT TO PRODUCT ATTRIBUTES
            #############################################################################
            name_space: dict = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
            supplier_code_xml: ET.Element = det.find('./nfe:prod/nfe:cProd', name_space)           
            ean_xml: ET.Element = det.find('./nfe:prod/nfe:cEAN', name_space)
            name_xml: ET.Element = det.find('./nfe:prod/nfe:xProd', name_space)
            anvisa_code_xml: ET.Element = det.find('./nfe:prod/nfe:med/nfe:cProdANVISA', name_space)
            max_consumer_price_xml: ET.Element = det.find('./nfe:prod/nfe:med/nfe:vPMC', name_space)
            #############################################################################
            # -- EXTRACT TO BATCH ATTRIBUTES
            #############################################################################
            physical_id_xml: ET.Element = det.find('./nfe:prod/nfe:rastro/nfe:nLote', name_space) 
            quantity_xml: ET.Element = det.find('./nfe:prod/nfe:qCom', name_space)  
            unit_cost_amount_xml: ET.Element = det.find('./nfe:prod/nfe:vUnCom', name_space)
            other_expenses_amount_xml: ET.Element = det.find('./nfe:prod/nfe:vOutro', name_space)
            manufacturing_date_xml: ET.Element = det.find('./nfe:prod/nfe:rastro/nfe:dFab', name_space)
            use_by_date_xml: ET.Element = det.find('./nfe:prod/nfe:rastro/nfe:dVal', name_space)
            #############################################################################
            # -- EXTRACT TO FISCAL PROFILE ATTRIBUTES
            #############################################################################
            ncm_xml: ET.Element = det.find('./nfe:prod/nfe:NCM', name_space)
            cest_xml: ET.Element = det.find('./nfe:prod/nfe:CEST', name_space)
            origin_code_xml: ET.Element = det.find('./nfe:imposto/nfe:ICMS/nfe:ICMS60/nfe:orig', name_space)
            #############################################################################
            # -- EXTRACT TO PURCHASE TAX DETAILS ATTRIBUTES
            #############################################################################
            cfop_xml: ET.Element = det.find('./nfe:prod/nfe:CFOP', name_space)
            icms_cst_xml: ET.Element = det.find('./nfe:imposto/nfe:ICMS/nfe:ICMS60/nfe:CST', name_space)
            icms_st_base_amount_xml: ET.Element = det.find('./nfe:imposto/nfe:ICMS/nfe:ICMS60/nfe:vBCSTRet', name_space)
            icms_st_percentage_xml: ET.Element = det.find('./nfe:imposto/nfe:ICMS/nfe:ICMS60/nfe:pST', name_space)
            icms_st_retained_amount_xml: ET.Element = det.find('./nfe:imposto/nfe:ICMS/nfe:ICMS60/nfe:vICMSSTRet', name_space)
            pis_cst_xml: ET.Element = det.find('./nfe:imposto/nfe:PIS/nfe:PISNT/nfe:CST', name_space)
            cofins_cst_xml: ET.Element = det.find('./nfe:imposto/nfe:COFINS/nfe:COFINSNT/nfe:CST', name_space)
            #############################################################################

            dict_tags: dict = {
                ############################
                # PRODUCT TAGS
                'cProd': supplier_code_xml,
                'cEAN': ean_xml,
                'xProd': name_xml,
                'cProdANVISA': anvisa_code_xml,
                'vPMC': max_consumer_price_xml,
                ############################
                # BATCH TAGS
                'nLote': physical_id_xml,
                'qCom': quantity_xml, 
                'vUnCom': unit_cost_amount_xml,
                'vOutro': other_expenses_amount_xml,
                'dFab': manufacturing_date_xml,
                'dVal': use_by_date_xml,
                ############################
                # FISCAL PROFILE TAGS
                'NCM': ncm_xml,
                'CEST': cest_xml,
                'orig': origin_code_xml,
                ############################
                # PURCHASE TAX DETAILS TAGS
                'CFOP': cfop_xml,
                'CST_ICMS': icms_cst_xml,
                'vBCSTRet': icms_st_base_amount_xml,
                'pST': icms_st_percentage_xml,
                'vICMSSTRet': icms_st_retained_amount_xml,
                'CST_PIS': pis_cst_xml,
                'CST_COFINS': cofins_cst_xml
                ############################
            }
        return dict_tags

    ###########
    def _verify_integrity_tags(self, dict_tags: dict, det: ET.Element) -> None:
        '''
        verify if some tag from dict received of argument is equal a none and capture a nItem of the knot det to use within the except.
        this function or returns None or returns a raising the error MissingTagError.
        '''

        if not isinstance(dict_tags, dict):
            raise ValueError

        tags_mandatory: set = {'cProd', 'xProd', 'qCom', 'vUnCom', 'nLote', 'dVal', 'CFOP', 'NCM'}
        tags_missing: list = []
        for key_tag, element in dict_tags.items():
            if element is None and key_tag in tags_mandatory:
                tags_missing.append(key_tag)

        if tags_missing:
            det_nItem = det.attrib.get('nItem')
            raise MissingTagError('[ERRO] An mandatory tag is absent. Verify the content', tags_missing, det_nItem)

    ######################################################
    # -- METHODS TO CONVERT OBJECTS ELEMENT'S IN YOURS RESPECTIVE TYPES 
    def _to_str(self, element: ET.Element) -> str | None:
        if element is not None:
            return element.text
        else: return None
    ###########
    def _to_decimal(self, element: ET.Element) -> Decimal | None:
        if element is not None:
            try:
                return Decimal(element.text)
            except InvalidOperation:
                raise ConversionError('[ERRO] Conversion Fail')
        else: return None
    ###########
    def _to_date(self, element: ET.Element) -> date | None:
        if element is not None:
            try:
                return date.fromisoformat(element.text)
            except:
                raise (ValueError, TypeError)
        else: return None
    
    ######################################################
    def _convertion_tags(self, tags: dict) -> tuple:
        'convert the tags in objetcs type string/float and manage a lift as error inside of except'
        try:
            clean_data = {
                ################################################
                # -- VALUES TO PURCHASE TAX DETAILS
                ################################################
                'cfop': self._to_str(tags.get('CFOP')),
                'icms_cst': self._to_str(tags.get('CST_ICMS')),
                'icms_st_base_amount': self._to_decimal(tags.get('vBCSTRet')),
                'icms_st_percentage': self._to_decimal(tags.get('pST')),
                'icms_st_retained_amount': self._to_decimal(tags.get('vICMSSTRet')),
                'pis_cst': self._to_str(tags.get('CST_PIS')),
                'cofins_cst': self._to_str(tags.get('CST_COFINS')),
                ################################################                
                # -- VALUES TO FISCAL PROFILE
                ################################################
                'ncm': self._to_str(tags.get('NCM')),
                'cest': self._to_str(tags.get('CEST')),
                'origin_code': self._to_str(tags.get('orig')),
                ################################################
                # -- VALUES TO BATCH
                ################################################
                'physical_id': self._to_str(tags.get('nLote')),
                'quantity': self._to_decimal(tags.get('qCom')),
                'unit_cost_amount': self._to_decimal(tags.get('vUnCom')),
                'other_expenses_amount': self._to_decimal(tags.get('vOutro')),
                'use_by_date': self._to_date(tags.get('dVal')),
                'manufacturing_date': self._to_date(tags.get('dFab')),
                ################################################
                # -- VALUES TO PRODUCT
                ################################################
                'supplier_code': self._to_str(tags.get('cProd')),
                'ean': self._to_str(tags.get('cEAN')),
                'name': self._to_str(tags.get('xProd')),
                'anvisa_code': self._to_str(tags.get('cProdANVISA')),
                'max_consumer_price': self._to_decimal(tags.get('vPMC')),
                ################################################
            }
            return clean_data
        except (ValueError) as conversion_error:
            raise ConversionError('[ERRO] This conversion is fail. Verify of types of the values in your keys within dicionary', tags) from conversion_error

    ###########
    def _manufacture_product(self, clean_data: dict) -> Product | None:
        'a simple function which instanciate a product'
        
        if not isinstance(clean_data, dict):
            return None
        else: 
            purchase_tax_details = PurchaseTaxDetails(
                id = None,
                cfop = clean_data['cfop'],
                icms_cst = clean_data['icms_cst'],
                icms_st_base_amount = clean_data['icms_st_base_amount'],
                icms_st_percentage = clean_data['icms_st_percentage'],
                icms_st_retained_amount = clean_data['icms_st_retained_amount'],
                pis_cst = clean_data['pis_cst'],
                cofins_cst = clean_data['cofins_cst']
            )
            fiscal_profile = FiscalProfile(
                id = None,
                ncm = clean_data['ncm'],
                cest = clean_data['cest'],
                origin_code = clean_data['origin_code']
            )
            new_batch = Batch(
                id = None,
                physical_id = clean_data['physical_id'],
                product_id = None,
                quantity = clean_data['quantity'],
                unit_cost_amount = clean_data['unit_cost_amount'],
                other_expenses_amount = clean_data['other_expenses_amount'],
                use_by_date = clean_data['use_by_date'],
                manufacturing_date = clean_data['manufacturing_date'],
                received_date = date.today(),
                taxation_details = purchase_tax_details
            )
            new_product = Product(
                id = None,
                supplier_code = clean_data['supplier_code'],
                ean = clean_data['ean'],
                name = clean_data['name'],
                anvisa_code = clean_data['anvisa_code'],
                sale_price = None,
                max_consumer_price = clean_data['max_consumer_price'],
                fiscal_profile = fiscal_profile
            )
            new_product.batch.insert(0, new_batch)
            return new_product
    
    ###########
    def process(self):
        'start the process of construction new products'
        try:
            root_element: str = self._extract_xml_data()
            list_dets: list[ET.Element] = self._extract_dets(root_element)
            if list_dets is not None:
                for det in list_dets:
                    nitem = det.attrib.get('nItem')
                    try:
                        dict_tags: dict = self._find_tags(det)
                        self._verify_integrity_tags(dict_tags, det)
                        clean_data: tuple = self._convertion_tags(dict_tags)
                        final_product: Product = self._manufacture_product(clean_data)

                        if final_product.ean is not None:
                            self.list_complete_products.append(final_product)
                        else:
                            self.list_quarantine_products.append(final_product)
                    
                    except (MissingTagError, ConversionError) as error:
                        logging.warning(f'[ALERTA] O Item DET Nº: {nitem} da NF-e foi ignorado. Motivo: {error}')
                        self.list_errors.append(error)
                        continue
            else:
                logging.warning(f'[ERRO] Conteúdo do XML vazio. Verifique o arquivo e tente novamente.')
        except ET.ParseError as error:
            logging.warning(
                f'''
                [ERRO] A Nota Fiscal inserida está sintaximente mal formada e não importará nenhum item. 
                Verifique a integridade das tags dentro do arquivo XML e tente novamente ou insira outra NF-e.
                Dados do Erro: {error}
                '''
                )
            self.list_errors.append(error)
    
    ######### --- METHODS TO RETURNS RESULTS OF THIS OPERATION --- #########
    def get_complete_products(self) -> tuple:
        'returns tuple of products complete'
        return (self.list_complete_products)
    
    def get_quarantine_products(self) -> tuple:
        'returns tuple of products incomplete'
        return (self.list_quarantine_products)

    def get_errors(self) -> tuple:
        'returns a tuple with the erros generated within process'
        return (self.list_errors)