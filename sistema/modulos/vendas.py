import logging
from sistema import database
from sistema.modelos.item import Item
from sistema.modelos.produto import Produto
from sistema.modelos.lote import Lote
from sistema.modulos import validadores_input

def adicionar_item() -> Item:
    'cria um item após uma busca por nome do produto'

    print('\n')
    print('=' * 30)
    print('[---CARRINHO---]')
    print('=' * 30)    

    while True:

        print('\n')
        input_busca = input('Digite o nome do produto: ')
        print('\n')
        lista_busca = database.buscar_produto_nome(input_busca)
    
        if not lista_busca:            
            logging.warning(f'[ALERTA] A busca por {input_busca} não corresponde a nenhum item.')
            print('Deseja tentar novamente ou vender como Item Avulso?')
            print('0. Digitar novamente')
            print('1. Vender como Item Avulso')
            escolha = input('Opção: ')

            if escolha == '0':
                continue
            elif escolha == '1':
                
                # dados produto avulso                
                print('=' * 30)
                logging.info(f'[INFO] ---CADASTRO DE PRODUTO AVULSO---')
                print('=' * 30)
                
                nome = input(f'Nome do Produto: ')
                preco_venda = validadores_input.validador_pv()
                data_validade = validadores_input.validador_dv()
                quantidade = validadores_input.validador_qtd()
                lote_fisico = validadores_input.validador_lotef()

                # instancias temporarias
                produto_avulso = Produto (
                    id = 'AVULSO',
                    ean = 'AVULSO',
                    nome = nome,
                    preco_venda = preco_venda
                )

                lote_avulso = Lote (
                    id_lote = None,
                    id_lote_fisico = lote_fisico,
                    produto_id = 'AVULSO',
                    quantidade = 0,
                    preco_custo = 0,
                    data_validade = data_validade,
                    data_entrada = 'AVULSO'
                )

                item_avulso = Item (
                    produto = produto_avulso,
                    lote = lote_avulso,
                    quantidade_vendida = quantidade
                )
                return item_avulso            
            else:
                logging.warning(f'[ALERTA] Opção inválida. Tente novamente.')
        else:
            print('=' * 30)            
            print(f'[RESULTADO] Foram encontrados {len(lista_busca)} itens na busca por "{input_busca}". Selecione o desejado.')
            print('=' * 30)      

            ################################################################################################################################
            
            def _menu_lista(lista_busca: list) -> tuple:
                'exibe o menu de opções para selecionar o item desejado (funcao aninhada)'

                if lista_busca is not None:                    
                    recomendacao = f'[RECOMENDADO] O item {lista_busca[0][1]} está com maior próximidade do vencimento, recomenda-se vende-lo.'
                    print(recomendacao)
                    print('=' * 30)
                    print('\n')
                else:
                    pass

                # esse loop for é o menu de opções
                for indice, item in enumerate(lista_busca):
                    print(f'{indice + 1}. {item[1]} - Preço: R${item[3]} - Validade: {item[8]} - Lote: {item[5]} - Quantidade: {item[6]} - Código de barras: {item[2]}')
                
                while True:
                    print('\n')
                    print('=' * 30)
                    print('       ---[SELEÇÃO]---')
                    print('=' * 30)
                    input_opcao = input(f'\nDigite o número da opção desejada: ')             
                    
                    try:
                        input_escolha = int(input_opcao)
                        if 1 <= input_escolha <= len(lista_busca):
                            indice_escolha = input_escolha - 1
                            item_selecionado = lista_busca[indice_escolha]    
                            break                            
                        else:                            
                            logging.warning('[ALERTA] Opção inválida. Tente novamente')                                 
                    
                    except ValueError:                        
                        logging.warning('[ALERTA] Utilize apenas números para selecionar o item. Tente novamente')
                        continue                    
                    
                return item_selecionado
                
            ################################################################################################################################

            item_selecionado = _menu_lista(lista_busca)
            
            def _construir_item_selecionado(item_selecionado: tuple) -> Item:
                
                                
                # desemcapsulando a tupla
                id_produto, nome_produto, codigo_barras, preco_venda_produto, id_lote_, id_lote_fisico, produto_id_, quantidade_, preco_custo_, data_validade_, data_entrada_ = item_selecionado        
                
                produto_selecionado = Produto (            
                    id = id_produto,
                    ean = codigo_barras,
                    nome = nome_produto,
                    preco_venda = preco_venda_produto
                )

                lote_selecionado = Lote (
                    id_lote = id_lote_,
                    id_lote_fisico = id_lote_fisico,
                    produto_id = produto_id_,
                    quantidade = quantidade_,
                    preco_custo = preco_custo_,
                    data_validade = data_validade_,
                    data_entrada = data_entrada_
                )

                input_quantidade = validadores_input.validador_qtd()
                        
                item = Item (
                    produto = produto_selecionado,
                    lote = lote_selecionado,
                    quantidade_vendida = input_quantidade
                )
                
                ###### teste de introdução de log no algoritmo ######                
                logging.info('\n[INFO] Item adicionado ao carrinho: %s', item)
                #####################################################
                
                return item
            
            ################################################################################################################################

            item_processado = _construir_item_selecionado(item_selecionado)
            item_processado_lotef = item_processado.lote.id_lote_fisico

            def _validar_lote_fisico(item_processado_lotef: str) -> bool:

                print('=' * 30)
                print('       ---[VALIDAÇÃO DE LOTE]---')
                print('=' * 30)

                while True: 
                    logging.info(f'[INFO] Insira os 2 primeiros e os 2 ultimos digitos do lote do produto em mãos.')
                    input_digitos = input('Digitos: ')
                    
                    if len(input_digitos) != 4:
                        logging.warning(f'[ALERTA] Entrada inválida. Digite exatamente os 2 primeiros e os 2 ultimos digitos do lote.')
                        continue
                    else:
                        # 2 primeiros e 2 ultimos digitos do produto selecionado (id_lote_fisico armazenado no db)
                        lote_primeiros = item_processado_lotef[:2]
                        lote_ultimos = item_processado_lotef[-2:]
                        lote_formatado = lote_primeiros + lote_ultimos

                        if input_digitos == lote_formatado:
                            lote_correto = True
                        else:
                            lote_correto = False
                                        
                    return lote_correto
            
            ################################################################################################################################

            # logica de registro de desvio de lote
            verificacao_fisica = _validar_lote_fisico(item_processado_lotef)           
            desvio_lote_lista = lista_busca[0][5] != item_processado.lote.id_lote_fisico
            desvio_lote_fisico = not verificacao_fisica
                
            if desvio_lote_lista or desvio_lote_fisico:
                
                logging.warning(f'[ALERTA] Desvio de lote detectado, um registro de alerta foi gerado.')
                logging.warning(f'[ALERTA] ')
                
                id_pedido = None
                id_produto = item_processado.produto.id
                id_usuario = None
                lote_vendido = item_processado_lotef                
                lote_correto = Lote (
                    id_lote = lista_busca[0][4],
                    id_lote_fisico = lista_busca[0][5],
                    produto_id = lista_busca[0][6],
                    quantidade = lista_busca[0][7],
                    preco_custo = lista_busca[0][8],
                    data_validade = lista_busca[0][9],
                    data_entrada = lista_busca[0][10]
                )                    
                
                database.registrar_alerta_lote(id_pedido, id_produto, id_usuario, lote_vendido, lote_correto)
                
            else:
                logging.info(f'[INFO] O item {item_processado.produto.nome} foi adicionado com sucesso.')
            
            return item_processado
                
                    
                    
                
                    




                
        