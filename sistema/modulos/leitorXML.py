import xml.etree.ElementTree as ET
from sistema.modelos.produto import Produto
from sistema.modelos.lote import Lote
from datetime import datetime

def extrair_dados_nfe(caminho_do_xml) -> list[Produto]:
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
                
                novo_produto = Produto(
                    id = item.find('.//nfe:cProd', ns).text,
                    ean = ean_valor,
                    nome = item.find('.//nfe:xProd', ns).text,                    
                    preco_venda = None
                )

                data_hoje = datetime.now().strftime('%Y-%m-%d')
                
                novo_lote = Lote(
                    id_lote = None,
                    produto_id = novo_produto.id,
                    quantidade = float(item.find('.//nfe:qCom', ns).text),
                    preco_custo = float(item.find('.//nfe:vUnCom', ns).text),
                    data_validade = None,
                    data_entrada = data_hoje
                    
                )

                novo_produto.lotes.append(novo_lote)
                lista_produtos.append(novo_produto)
            
            except AttributeError:                
                print(f'[AVISO] Item com dados incompletos no XML foi ignorado.')
                continue
        
        return lista_produtos
   
    except ET.ParseError as e:
        print(f'[ERRO] PARSE NO XML. O arquivo está corrompido? Detalhes: {e}')
        return None
    except FileNotFoundError:
        print(f'[ERRO] ARQUIVO NÃO ENCONTRADO. Verifique o nome e o local. Detalhes: {e}')
        return None