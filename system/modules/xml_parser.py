import xml.etree.ElementTree as ET
from system.models.product import Product
from system.models.batch import Batch
from datetime import datetime
import logging

def extract_nfe_data(xml_content: str) -> list[Product]:
    'receives xml string form and return one list of products'

    try:
        name_space = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
        root_element: ET.Element = ET.fromstring(xml_content)
        product_list = []
        
        for item in root_element.findall('.//nfe:det', name_space):                   
            try:
                
                ean_tag = item.find('.//nfe:cEAN', name_space)                 
                ean_value = ean_tag.text if ean_tag is not None else None      
                
                new_product = Product(
                    id = item.find('.//nfe:cProd', name_space).text,
                    ean = ean_value,
                    name = item.find('.//nfe:xProd', name_space).text,                    
                    sale_price = None
                )
                
                today = datetime.now().strftime('%Y-%m-%d')
                
                new_batch = Batch(
                    batch_id = None,
                    physical_batch_id = None,
                    product_id = new_product.id,
                    quantity = float(item.find('.//nfe:qCom', name_space).text),
                    cost_price = float(item.find('.//nfe:vUnCom', name_space).text),
                    expiration_date = None,
                    entry_date = today   
                )
                new_product.batch.append(new_batch)
                product_list.append(new_product)
            except AttributeError:                
                logging.warning(f'[AVISO] Item com dados incompletos no XML foi ignorado.')
                continue
        return product_list
    
    except ET.ParseError as instance_xml_error:
        logging.error(f'[ERRO] A importação da NF-e falhou. Solicite um novo arquivo .xml ao seu fornecedor. Detalhes técnicos: {instance_xml_error}')
        return None
    
#####################################################################################################################