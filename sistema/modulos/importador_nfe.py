import os
from sistema.modulos import xml_parser
from sistema import database
from sistema.modulos import validators
import logging


def importar_nfe():
    'pede o nome do arquivo xml e processa os dados.'
    produtos_nota = None
    
    nome_arquivo = input('Digite o nome do arquivo XML (ex: exemplo_nfe.xml): ')
    caminho_completo = os.path.join('dados', nome_arquivo)    
    try:
        produtos_nota = xml_parser.extrair_dados_nfe(caminho_completo)
    except Exception as e:
        logging.error(f'\n [ERRO] Ocorreu um problema inesperado ao processar o arquivo - Verifique o nome do arquivo.')

    if produtos_nota:
        print(f'\n---{len(produtos_nota)} Produtos Encontrados na Nota Fiscal ---')
        
        for produto in produtos_nota:
                if database.produtos_existentes(produto):
                    resposta_db = database.buscar_produto(produto)
                    if resposta_db == None:
                        logging.error(f'\n [ERRO] A resposta do database retornou vazia...')
                    else:                  
                        produto.sale_price = resposta_db[2]
                        produto.batch[0].expiration_date = resposta_db[3]                   
                else:
                    print(f'\n [NOVO PRODUTO ENCONTRADO]: {produto.name}')                    
                    pv_validado = validators.collect_price_input()
                    dv_validada = validators.collect_date_input()
                    lotef_validado = validators.batch_physical_validator()                
                    produto.sale_price = pv_validado
                    produto.batch[0].expiration_date = dv_validada
                    produto.batch[0].physical_batch_id = lotef_validado                    
        
        return produtos_nota
    else:
        logging.info('\n [INFO] Nenhum produto encontrado ou erro na leitura do arquivo.')
