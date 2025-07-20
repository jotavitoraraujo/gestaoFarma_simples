from sistema.modelos.produto import Produto


def relatorio_importacao(produtos_nota: list[Produto]):
    'imprime produtos salvos ou atualizados no database'

    print('\n--- Produtos a serem salvos/atualizados ---')               
    for produto in produtos_nota:
        # imprime os dados de forma mais legivel
        print(f'Código: {produto.id}')
        print(f'Nome: {produto.nome}')
        print(f'Qtde: {produto.lotes[0].quantidade}')
        print(f'Custo Unitário: R${produto.lotes[0].preco_custo:.2f}')
        
        if produto.preco_venda:
            print(f'Preço de Venda: R$ {produto.preco_venda:.2f}')
        else:
            print(f'[ALERTA] Preço de Venda não definido!')
        
        if produto.lotes[0].data_validade:
            print(f'Validade: {produto.lotes[0].data_validade}')
        else:
            print(f'[ALERTA] Data de validade não definida!')
        
        print('-' * 30)