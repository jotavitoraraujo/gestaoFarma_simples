from sistema import database
from sistema.modelos.item import Item
from sistema.modelos.produto import Produto
from sistema.modelos.lote import Lote
from sistema.modulos import validadores_input

def carrinho() -> Item:
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
            print(f'[AVISO] A busca por {input_busca} não corresponde a nenhum item. Tente novamente.')
            
        else:
            print('=' * 30)            
            print(f'[RESULTADO] Foram encontrados {len(lista_busca)} itens na busca por "{input_busca}". Selecione o desejado.')
            print('=' * 30)           

            ################################################################################################################################
            
            def menu_lista(lista_busca) -> tuple:
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
                    print(f'{indice + 1}. {item[1]} - Preço: R${item[3]} - Validade: {item[8]} - Lote: {item[4]} - Quantidade: {item[6]} - Código de barras: {item[2]}')
                
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
                            print('[ERRO] Opção inválidade. Tente novamente.')                                 
                    
                    except ValueError:
                        print(f'[ERRO] Utilize apenas números para selecionar o item. Tente novamente.')
                        continue                    
                    
                return item_selecionado
                
            ################################################################################################################################

        # construir uma função separada que utilize essa lógica de instancia de Item

        item_selecionado = menu_lista(lista_busca)                
        id_produto, nome_produto, codigo_barras, preco_venda_produto, id_lote_, produto_id_, quantidade_, preco_custo_, data_validade_, data_entrada_ = item_selecionado        
        
        produto_selecionado = Produto (            
            id = id_produto,
            ean = codigo_barras,
            nome = nome_produto,
            preco_venda = preco_venda_produto
        )

        lote_selecionado = Lote (
            id_lote = id_lote_,
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
        return item
       
                





