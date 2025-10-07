### --- IMPORTS --- ###
from system.modules.xml_parser import XMLParser
from typing import Callable
import logging



# def importar_nfe():
#     'pede o nome do arquivo xml e processa os dados.'
#     produtos_nota = None
    
#     nome_arquivo = input('Digite o nome do arquivo XML (ex: exemplo_nfe.xml): ')
#     caminho_completo = os.path.join('dados', nome_arquivo)    
#     try:
#         produtos_nota = xml_parser.extract_nfe_data(caminho_completo)
#     except Exception as instance_exception:
#         logging.error(f'\n [ERRO] Ocorreu um problema inesperado ao processar o arquivo - Verifique o nome do arquivo. Detalhes: {instance_exception}')

#     if produtos_nota:
#         print(f'\n---{len(produtos_nota)} Produtos Encontrados na Nota Fiscal ---')
        
#         for produto in produtos_nota:
#                 if database.products_existing(produto):
#                     resposta_db = database.search_product(produto)
#                     if resposta_db == None:
#                         logging.error(f'\n [ERRO] A resposta do database retornou vazia...')
#                     else:                  
#                         produto.sale_price = resposta_db[2]
#                         produto.batch[0].expiration_date = resposta_db[3]                   
#                 else:
#                     print(f'\n [NOVO PRODUTO ENCONTRADO]: {produto.name}')                    
#                     pv_validado = validators.collect_price_input()
#                     dv_validada = validators.collect_date_input()
#                     lotef_validado = validators.batch_physical_validator()                
#                     produto.sale_price = pv_validado
#                     produto.batch[0].expiration_date = dv_validada
#                     produto.batch[0].physical_batch_id = lotef_validado                    
        
#         return produtos_nota
#     else:
#         logging.info('\n [INFO] Nenhum produto encontrado ou erro na leitura do arquivo.')

class NFEImporter:
    def __init__(self, parser: XMLParser, persistence: Callable):
        self.parser = parser
        self.persistence = persistence

    def run_import(self, xml_file_path: str):
        'starts the process of importation'
        try:
            with open(xml_file_path, encoding = 'UTF-8') as xml_file_open:
                xml_content = xml_file_open.read()
            ###############################################################################
            # -- 
            parser_instance: XMLParser = self.parser(xml_content)
            parser_instance.process()
            complete_products: list = parser_instance.get_complete_products()
            quarantine_products: list = parser_instance.get_quarantine_products()
            errors_raised: list = parser_instance.get_errors()
            ###############################################################################
            if complete_products:
                self.persistence(complete_products)
                logging.info(f'[INFO] Produtos importados com sucesso!')
            else:
                logging.warning(f'[ALERTA] Nenhum produto foi importado. Verifique o log de ocorrências.')
            ###############################################################################
            if quarantine_products:
                # -> AQUI VIRÁ A FUNÇÃO QUE SALVARÁ ESSES PRODUTOS NA TABELA produtos_pendentes
                logging.warning(f'[ALERTA] Foram importados {len(quarantine_products)} para a quarentena. Favor completar o cadastro.')
            else:
                logging.info(f'[INFO] Nenhum produto foi enviado a quarentena.')
            ###############################################################################
            if errors_raised:
                for index, erros in enumerate(errors_raised):
                    logging.error(f'[ERRO] {index}: {erros}')
            else:
                logging.info(f'[INFO] Nenhum erro detectado.')
            ###############################################################################
        except FileNotFoundError:
            logging.error(f'[ERRO] O Arquivo inserido não existe. Tente novamente.')
        except PermissionError:
            logging.error(f'[ERRO] O Arquivo inserido não pode ser processado devido a permissões na importação. Tente novamente.')



