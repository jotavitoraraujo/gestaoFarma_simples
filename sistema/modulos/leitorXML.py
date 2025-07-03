import xml.etree.ElementTree as ET

def extrair_dados_nfe(caminho_do_xml):
    'Le um arquivo XML de NF-e e extrai os dados dos produtos.'
    'Retorna uma lista de dicts, onde cada dict é um produto'

    try:
        # define o namespace padrão da NF-e para encontrar as tags corretamente
        ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}

        # carrega o xml
        tree = ET.parse(caminho_do_xml)
        root = tree.getroot()

        lista_produtos = []

        # repete sobre cada item ('det') da nota fiscal
        for item in root.findall('.//nfe:det', ns):
            produto = {}

            # tenta extrair cada campo do produto. Usa .text p/ pegar o conteudo da tag
            try:
                # o find() procura por uma tag filha.
                produto['codigo'] = item.find('.//nfe:cProd', ns).text
                produto['nome'] = item.find('.//nfe:xProd', ns).text
                produto['quantidade'] = float(item.find('.//nfe:qCom', ns).text)
                produto['preco_custo'] = float(item.find('.//nfe:vUnCom', ns).text)

                # O EAN (codigo de barra [sigla]) pode não existir, então verificamos antes.
                ean_tag = item.find('.//nfe:cEAN', ns)
                if ean_tag is not None:
                    produto['ean'] = ean_tag.text
                else: 
                    produto['ean'] = None

                lista_produtos.append(produto)
            
            except AttributeError:
                # pula um item se alguma tag essencial não for encontrada
                print(f'Aviso: Item com dados incompletos no XML foi ignorado.')
                continue
        
        return lista_produtos
   
    except ET.ParseError as e:
        print(f'DEBUG: ERRO DE PARSE NO XML. O arquivo está corrompido? Detalhes: {e}')
        return None
    except FileNotFoundError:
        print(f'DEBUG: ERRO DE ARQUIVO NÃO ENCONTRADO. Verifique o nome e o local. Detalhes: {e}')
        return None