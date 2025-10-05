from system.models.product import Product


def relatorio_importacao(produtos_nota: list[Product]):
    'imprime produtos salvos ou atualizados no database'

    print('\n--- Produtos a serem salvos/atualizados ---')               
    for produto in produtos_nota:
        # imprime os dados de forma mais legivel
        print(f'Código: {produto.id}')
        print(f'Nome: {produto.name}')
        print(f'Qtde: {produto.batch[0].quantity}')
        print(f'Custo Unitário: R${produto.batch[0].unit_cost_amount:.2f}')
        
        if produto.sale_price:
            print(f'Preço de Venda: R$ {produto.sale_price:.2f}')
        else:
            print(f'[ALERTA] Preço de Venda não definido!')
        
        if produto.batch[0].use_by_date:
            print(f'Validade: {produto.batch[0].use_by_date}')
        else:
            print(f'[ALERTA] Data de validade não definida!')
        
        print('-' * 30)