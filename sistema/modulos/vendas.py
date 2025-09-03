import logging
from sistema import database
from sistema.modelos.sale_item import SaleItem
from sistema.modelos.product import Product
from sistema.modelos.batch import Batch
from sistema.modelos.user import User
from sistema.modulos import validators


def adicionar_item() -> SaleItem:
    'cria um item após uma busca por nome do produto'

    print('\n')
    print('=' * 30)
    print('[---CARRINHO---]')
    print('=' * 30)    

    while True:

        print('\n')
        input_busca = input('Digite o nome do produto: ')
        print('\n')
        lista_busca = database.search_product_name(input_busca)
    
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
                preco_venda = validators.sell_price_validator()
                data_validade = validators.collect_date_input()
                quantidade = validators.quantity_validator()
                lote_fisico = validators.batch_physical_validator()

                # instancias temporarias
                produto_avulso = Product (
                    id = 'AVULSO',
                    ean = 'AVULSO',
                    name = nome,
                    sale_price = preco_venda
                )

                lote_avulso = Batch (
                    batch_id = None,
                    physical_batch_id = lote_fisico,
                    product_id = 'AVULSO',
                    quantity = 0,
                    cost_price = 0,
                    expiration_date = data_validade,
                    entry_date = 'AVULSO'
                )

                item_avulso = SaleItem (
                    product = produto_avulso,
                    batch = lote_avulso,
                    quantity_sold = quantidade
                )
                logging.warning(f'[ALERTA] Cadastre o produto {item_avulso.product.name} no seu estoque.')
                # criar um tabela para salvar esses produtos no database
                return item_avulso            
            else:
                logging.warning(f'[ALERTA] Opção inválida. Tente novamente.')
        else:
            print('=' * 30)            
            logging.info(f'[INFO] Foram encontrados {len(lista_busca)} itens na busca por "{input_busca}". Selecione o desejado.')
            print('=' * 30)      

            ################################################################################################################################
            
            def _menu_lista(lista_busca: list) -> tuple:
                'exibe o menu de opções para selecionar o item desejado (funcao aninhada)'

                if lista_busca is not None:                    
                    recomendacao = f'[RECOMENDADO] O item {lista_busca[0][1]} está com maior próximidade do vencimento, recomenda-se vende-lo.'
                    print('\n')
                    print('=' * 30)
                    print(recomendacao)
                    print('=' * 30)
                    
                else:
                    pass

                # esse loop for é o menu de opções
                for indice, item in enumerate(lista_busca):
                    print(f'{indice + 1}. {item[1]} - Preço: R${item[3]} - Validade: {item[9]} - Lote: {item[5]} - Quantidade: {item[7]} - Código de barras: {item[2]}')
                
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
            
            def _construir_item_selecionado(item_selecionado: tuple) -> SaleItem:
                
                                
                # desemcapsulando a tupla
                id_produto, nome_produto, codigo_barras, preco_venda_produto, id_lote_, id_lote_fisico, produto_id_, quantidade_, preco_custo_, data_validade_, data_entrada_ = item_selecionado        
                
                produto_selecionado = Product (            
                    id = id_produto,
                    ean = codigo_barras,
                    name = nome_produto,
                    sale_price = preco_venda_produto
                )

                lote_selecionado = Batch (
                    batch_id = id_lote_,
                    physical_batch_id = id_lote_fisico,
                    product_id = produto_id_,
                    quantity = quantidade_,
                    cost_price = preco_custo_,
                    expiration_date = data_validade_,
                    entry_date = data_entrada_
                )

                input_quantidade = validators.quantity_validator()
                        
                item = SaleItem (
                    product = produto_selecionado,
                    batch = lote_selecionado,
                    quantity_sold = input_quantidade
                )
                
                ###### teste de introdução de log no algoritmo ######                
                logging.info(f'\n[INFO] Item adicionado ao carrinho: {item}')
                #####################################################
                
                return item
            
            ################################################################################################################################

            item_processado = _construir_item_selecionado(item_selecionado)
            item_processado_lotef = item_processado.batch.physical_batch_id

            def _validar_lote_fisico(item_processado_lotef: str) -> bool:

                print('=' * 30)
                print('       ---[VALIDAÇÃO]---')
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

                        if input_digitos.lower() == lote_formatado.lower():
                            lote_correto = True
                        else:
                            lote_correto = False
                                        
                    return lote_correto
            
            ################################################################################################################################

            # logica de registro de desvio de lote
            verificacao_fisica = _validar_lote_fisico(item_processado_lotef)           
            desvio_lote_lista = lista_busca[0][5] != item_processado.batch.physical_batch_id
            desvio_lote_fisico = not verificacao_fisica           
            
            if desvio_lote_lista or desvio_lote_fisico:
                
                logging.warning(f'[ALERTA] Desvio de lote detectado, um registro de alerta foi gerado.')

                id_pedido = 'AVULSO'
                id_produto = item_processado.product
                
                id_usuario = User (
                    user_id = 0,
                    user_name = 'AVULSO',
                    user_pin = 'AVULSO'
                )
                
                lote_vendido = item_processado.batch
                
                lote_correto = Batch (
                    batch_id = lista_busca[0][4],
                    physical_batch_id = lista_busca[0][5],
                    product_id = lista_busca[0][6],
                    quantity = lista_busca[0][7],
                    cost_price = lista_busca[0][8],
                    expiration_date = lista_busca[0][9],
                    entry_date = lista_busca[0][10]
                )                    
                
                database.register_batch_alert(id_pedido, id_produto, id_usuario, lote_vendido, lote_correto)
                
            else:
                logging.info(f'[INFO] O item {item_processado.product.name} foi adicionado com sucesso.')
            
            return item_processado
                
                    
                    
                
                    




                
        