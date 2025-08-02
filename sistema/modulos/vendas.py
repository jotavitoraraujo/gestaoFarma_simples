from sistema import database
from sistema.modelos.item import Item
from sistema.modelos.produto import Produto
from sistema.modelos.usuario import Usuario

def carrinho() -> Item:
    'cria um item após uma busca por nome do produto'

    print('=' * 30)
    print('[---CARRINHO---]')
    print('-' * 30)    

    while True:

        input_busca = input('Digite o nome do produto: ')
        lista_busca = database.buscar_produto_nome(input_busca)

        if not lista_busca:
            print(f'[AVISO] A busca por {input_busca} não corresponde a nenhum item. Tente novamente.')
            
        else:
            print('=' * 30)
            print('[LISTA] ---GESTÃO FARMA ITENS---')
            print('=' * 30)
            print(f'\n[RESULTADO] Foram encontrados {len(lista_busca)} itens na busca por "{input_busca}". Selecione o desejado.')            

            def menu_lista(lista_busca):
                'exibe o menu de opções para selecionar o item desejado'

                # esse loop for é o menu de opções
                for indice, item in enumerate(lista_busca):
                    print(f'{indice + 1}. {item[1]} - Preço: R${item[2]:.2f} - Validade: {item[3]}')
                    if indice == 0:
                        print(f'[RECOMENDADO] O {item[1]}, está com maior próximidade do vencimento, recomenda-se vende-lo.')
                    else:
                        pass
                
                while True:

                    input_opcao = input(f'[SELEÇÃO] Digite o número da opção desejada: ')                
                    
                    try:
                        input_escolha = int(input_opcao)
                        if 1 <= input_escolha <= len(lista_busca):
                            indice_escolha = input_escolha - 1
                            item_selecionado = lista_busca[indice_escolha]    
                            return item_selecionado
                        else:
                            print('[ERRO] Opção inválidade. Tente novamente.')                                 
                    
                    except ValueError:
                        print(f'[ERRO] Utilize apenas números para selecionar o item. Tente novamente.')
                        continue

            item_selecionado = menu_lista(lista_busca)            

                





