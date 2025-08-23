import xml.etree.ElementTree as ET
from sistema.modelos.product import Product
from sistema.modelos.batch import Batch
from datetime import datetime
import logging

def extrair_dados_nfe(caminho_do_xml) -> list[Product]:
    'Le um arquivo XML de NF-e e extrai os dados dos produtos. Retorna uma lista de objetos, onde cada objeto é do tipo produto'

    try:
        # define o namespace padrão da NF-e para encontrar as tags corretamente
        ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}

        # carrega o xml
        tree = ET.parse(caminho_do_xml)
        root = tree.getroot()

        lista_produtos = []

        
        for item in root.findall('.//nfe:det', ns):                   
            
            try:
                
                ean_tag = item.find('.//nfe:cEAN', ns)
                ean_valor = ean_tag.text if ean_tag is not None else None                
                
                novo_produto = Product(
                    id = item.find('.//nfe:cProd', ns).text,
                    ean = ean_valor,
                    name = item.find('.//nfe:xProd', ns).text,                    
                    sale_price = None
                )

                data_hoje = datetime.now().strftime('%Y-%m-%d')
                
                novo_lote = Batch(
                    batch_id = None,
                    physical_batch_id = None,
                    product_id = novo_produto.id,
                    quantity = float(item.find('.//nfe:qCom', ns).text),
                    cost_price = float(item.find('.//nfe:vUnCom', ns).text),
                    expiration_date = None,
                    entry_date = data_hoje
                    
                )

                novo_produto.batch.append(novo_lote)
                lista_produtos.append(novo_produto)
            
            except AttributeError:                
                logging.warning(f'[AVISO] Item com dados incompletos no XML foi ignorado.')
                continue
        
        return lista_produtos
   
    except ET.ParseError as e:
        logging.error(f'[ERRO] PARSE NO XML. O arquivo está corrompido? Detalhes: {e}')
        return None
    except FileNotFoundError:
        logging.error(f'[ERRO] ARQUIVO NÃO ENCONTRADO. Verifique o nome e o local. Detalhes: {e}')
        return None
    
#####################################################################################################################

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
        logging.error(f'[ERRO] PARSE NO XML. O arquivo está corrompido? Detalhes: {instance_xml_error}')
        return None