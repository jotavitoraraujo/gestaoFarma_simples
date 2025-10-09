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
    def _find_tags_in_xml(self, det: ET.Element) -> dict:
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
    def _check_presence_mandatory_tags(self, dict_tags: dict, det: ET.Element) -> None:
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
    def _conversion_of_tag_dict_key_values(self, dict_tags: dict) -> dict:
        'convert the tags in objetcs type string/decimal/date and manage a lift as error inside of except'
        try:
            converted_data_for_attrib_product = {
                ################################################
                # -- VALUES TO PURCHASE TAX DETAILS
                ################################################
                'cfop': self._to_str(dict_tags.get('CFOP')),
                'icms_cst': self._to_str(dict_tags.get('CST_ICMS')),
                'icms_st_base_amount': self._to_decimal(dict_tags.get('vBCSTRet')),
                'icms_st_percentage': self._to_decimal(dict_tags.get('pST')),
                'icms_st_retained_amount': self._to_decimal(dict_tags.get('vICMSSTRet')),
                'pis_cst': self._to_str(dict_tags.get('CST_PIS')),
                'cofins_cst': self._to_str(dict_tags.get('CST_COFINS')),
                ################################################                
                # -- VALUES TO FISCAL PROFILE
                ################################################
                'ncm': self._to_str(dict_tags.get('NCM')),
                'cest': self._to_str(dict_tags.get('CEST')),
                'origin_code': self._to_str(dict_tags.get('orig')),
                ################################################
                # -- VALUES TO BATCH
                ################################################
                'physical_id': self._to_str(dict_tags.get('nLote')),
                'quantity': self._to_decimal(dict_tags.get('qCom')),
                'unit_cost_amount': self._to_decimal(dict_tags.get('vUnCom')),
                'other_expenses_amount': self._to_decimal(dict_tags.get('vOutro')),
                'use_by_date': self._to_date(dict_tags.get('dVal')),
                'manufacturing_date': self._to_date(dict_tags.get('dFab')),
                ################################################
                # -- VALUES TO PRODUCT
                ################################################
                'supplier_code': self._to_str(dict_tags.get('cProd')),
                'ean': self._to_str(dict_tags.get('cEAN')),
                'name': self._to_str(dict_tags.get('xProd')),
                'anvisa_code': self._to_str(dict_tags.get('cProdANVISA')),
                'max_consumer_price': self._to_decimal(dict_tags.get('vPMC')),
                ################################################
            }
            return converted_data_for_attrib_product
        except (ValueError) as conversion_error:
            raise ConversionError('[ERRO] This conversion is fail. Verify of types of the values in your keys within dicionary', dict_tags) from conversion_error

    ###########
    def _manufacture_product(self, data_converted: dict) -> Product | None:
        'a simple function which instanciate a product'
        
        if not isinstance(data_converted, dict):
            return None
        else: 
            purchase_tax_details = PurchaseTaxDetails(
                id = None,
                cfop = data_converted['cfop'],
                icms_cst = data_converted['icms_cst'],
                icms_st_base_amount = data_converted['icms_st_base_amount'],
                icms_st_percentage = data_converted['icms_st_percentage'],
                icms_st_retained_amount = data_converted['icms_st_retained_amount'],
                pis_cst = data_converted['pis_cst'],
                cofins_cst = data_converted['cofins_cst']
            )
            fiscal_profile = FiscalProfile(
                id = None,
                ncm = data_converted['ncm'],
                cest = data_converted['cest'],
                origin_code = data_converted['origin_code']
            )
            new_batch = Batch(
                id = None,
                product_id = None,
                physical_id = data_converted['physical_id'],
                quantity = data_converted['quantity'],
                unit_cost_amount = data_converted['unit_cost_amount'],
                other_expenses_amount = data_converted['other_expenses_amount'],
                use_by_date = data_converted['use_by_date'],
                manufacturing_date = data_converted['manufacturing_date'],
                received_date = date.today(),
                taxation_details = purchase_tax_details
            )
            new_product = Product(
                id = None,
                supplier_code = data_converted['supplier_code'],
                ean = data_converted['ean'],
                name = data_converted['name'],
                anvisa_code = data_converted['anvisa_code'],
                sale_price = None,
                max_consumer_price = data_converted['max_consumer_price'],
                fiscal_profile = fiscal_profile
            )
            new_product.batch.insert(0, new_batch)
            return new_product
    
    ###########
    def execute_process(self):
        'start the process of construction new products'
        try:
            root_element: str = self._extract_xml_data()
            list_dets: list[ET.Element] = self._extract_dets(root_element)
            if list_dets is not None:
                for det in list_dets:
                    nitem = det.attrib.get('nItem')
                    try:
                        dict_tags: dict = self._find_tags_in_xml(det)
                        self._check_presence_mandatory_tags(dict_tags, det)
                        clean_data: dict = self._conversion_of_tag_dict_key_values(dict_tags)
                        final_product: Product = self._manufacture_product(clean_data)

                        if final_product.ean is not None:
                            self.list_complete_products.append(final_product)
                        else:
                            self.list_quarantine_products.append(final_product)
                    
                    except (MissingTagError, ConversionError) as error:
                        logging.warning(f'[ALERTA] O Item DET Nº: {nitem} da NF-e foi enviado a quarentena. Motivo: {error}')
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