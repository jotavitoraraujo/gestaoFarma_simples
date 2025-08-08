import os
from sistema.modulos import leitorXML
from sistema import database
from sistema.modulos import validadores_input


def importar_nfe():
    'pede o nome do arquivo xml e processa os dados.'
    produtos_nota = None
    
    nome_arquivo = input('Digite o nome do arquivo XML (ex: exemplo_nfe.xml): ')
    caminho_completo = os.path.join('dados', nome_arquivo)    
    try:
        produtos_nota = leitorXML.extrair_dados_nfe(caminho_completo)
    except Exception as e:
        print(f'\n [ERRO] Ocorreu um problema inesperado ao processar o arquivo - Verifique o nome do arquivo.')

    if produtos_nota:
        print(f'\n---{len(produtos_nota)} Produtos Encontrados na Nota Fiscal ---')
        
        for produto in produtos_nota:
                if database.produtos_existentes(produto):
                    resposta_db = database.buscar_produto(produto)
                    if resposta_db == None:
                        print(f'\n [ERRO] A resposta do database retornou vazia...')
                    else:                  
                        produto.preco_venda = resposta_db[2]
                        produto.lotes[0].data_validade = resposta_db[3]                   
                else:
                    print(f'\n [NOVO PRODUTO ENCONTRADO]: {produto.nome}')                    
                    pv_validado = validadores_input.validador_pv()
                    dv_validada = validadores_input.validador_dv()
                    lotef_validado = validadores_input.validador_lotef()                
                    produto.preco_venda = pv_validado
                    produto.lotes[0].data_validade = dv_validada
                    produto.lotes[0].id_lote_fisico = lotef_validado                    
        
        return produtos_nota
    else:
        print('\n [INFO] Nenhum produto encontrado ou erro na leitura do arquivo.')
