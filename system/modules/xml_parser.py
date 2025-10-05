######## --- IMPORTS --- ########
from system.models.product import Product
from system.models.batch import Batch
from system.utils.exceptions import MissingTagError, ConversionError
from datetime import date
from decimal import Decimal
import xml.etree.ElementTree as ET
import logging
#################################

class XMLParser:
    def __init__(self, xml_content: str):
        self.xml_content: str = xml_content
        self.list_complete_products: list = []
        self.list_absent_ean_products: list[tuple] = []
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
            
            name_space: dict = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
            supplier_code_xml: ET.Element = det.find('.//nfe:cProd', name_space)           
            ean_xml: ET.Element = det.find('.//nfe:cEAN', name_space)
            name_xml: ET.Element = det.find('.//nfe:xProd', name_space)
            quantity_xml: ET.Element = det.find('.//nfe:qCom', name_space)    
            cost_price_xml: ET.Element = det.find('.//nfe:vUnCom', name_space)
        
            dict_tags: dict = {
                'cProd': supplier_code_xml,
                'cEAN': ean_xml,
                'xProd': name_xml, 
                'qCom': quantity_xml, 
                'vUnCom': cost_price_xml
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

        tags_mandatory: set = {'cProd', 'xProd', 'qCom', 'vUnCom'}
        tags_missing: list = []
        for key_tag, element in dict_tags.items():
            if element is None and key_tag in tags_mandatory:
                tags_missing.append(key_tag)

        if tags_missing:
            det_nItem = det.attrib.get('nItem')
            raise MissingTagError('[ERRO] An mandatory tag is absent. Verify the content', tags_missing, det_nItem)

    ###########
    def _convertion_tags(self, tags: dict) -> tuple:
        'convert the tags in objetcs type string/float and manage a lift as error inside of except'
        
        ean = None
        try:
            supplier_code: str = tags['cProd'].text
            
            if tags['cEAN'] is not None:
                ean = tags['cEAN'].text        
            
            name: str = tags['xProd'].text
            quantity: Decimal = Decimal(tags['qCom'].text)
            cost_price: Decimal = Decimal(tags['vUnCom'].text)
            product_data: tuple = (supplier_code, ean, name, quantity, cost_price,)
            return product_data
        
        except (ValueError) as conversion_error:
            raise ConversionError('[ERRO] This conversion is fail. Verify of types of the values in your keys within dicionary', tags, ean) from conversion_error

    ###########
    def _manufacture_product(self, product_data: tuple) -> Product:
        'an simple function what instance a product'
        
        if len(product_data) == 5:
            new_product = Product (
                id = None,
                supplier_code = product_data[0],
                ean = product_data[1],
                name = product_data[2],
                sale_price = None
            )
            new_batch = Batch (
                id = None,
                physical_id = None,
                product_id = new_product.id,
                quantity = product_data[3],
                unit_cost_amount = product_data[4],
                use_by_date = None,
                received_date = date.today()
            )

            new_product.batch.append(new_batch)
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
                            self.list_absent_ean_products.append(final_product)
                    
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
    
    def get_incomplete_products(self) -> tuple:
        'returns tuple of products incomplete'
        return (self.list_absent_ean_products)

    def get_errors(self) -> tuple:
        'returns a tuple with the erros generated within process'
        return (self.list_errors)