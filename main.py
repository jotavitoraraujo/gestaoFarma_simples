import os
import sistema.database as database
import sistema.modulos.leitorXML as leitorXML


def exibir_menu():
    'Exibe o menu principal e retorna a escolha do usuário.'
    print('\n--- Sistema de Gestão da Farmácia ---')
    print('1. Importar Nota Fiscal (XML)')
    print('2. Registrar Venda')
    print('3. Ver Relátorios')
    print('0. Sair')
    return input('Escolha uma opção: ')

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
        print('\n--- Produtos Encontrados na Nota Fiscal ---')
        for produto in produtos_nota:
                if database.produtos_existentes(produto['codigo']):
                    pass
                else:
                    print(f'\n [NOVO PRODUTO ENCONTRADO]: {produto['nome']}')
                    preco_digitado = float(input(f'\n Qual preço de venda deste novo item?: '))
                    validade_digitada = str(input(f'\n Qual a validade deste novo item (ANO/MÊS/DIA)?: '))
                    produto['preco_venda'] = preco_digitado
                    produto['data_validade'] = validade_digitada
        
        print('\n--- Produtos a serem salvos/atualizados ---')   
        for produto in produtos_nota:
            # imprime os dados de forma mais legivel
            print(f' Código: {produto.get('codigo')}')
            print(f' Nome: {produto.get('nome')}')
            print(f' Qtde: {produto.get('quantidade')}')
            print(f' Custo Unitário: R${produto.get('preco_custo'):.2f}')
            if produto.get('preco_venda'):
                print(f'Preço de Venda: R$ {produto.get('preco_venda', 0):.2f}')
            if produto.get('data_validade'):
                print(f' Validade: {produto.get('data_validade')}')
            print('-' * 30)
        database.salvar_produtos(produtos_nota)
        # print('\n [INFO] O próximo passo é adicionar esses produtos ao estoque.')
    else:
        print('\n [INFO] Nenhum produto encontrado ou erro na leitura do arquivo.')

def main():
    'Garantir que a tabela no bd exista.'
    database.criar_tabela_produtos()

    while True:
        escolha = exibir_menu()
        if escolha == '1':
            importar_nfe()
            # print('\n[INFO] Função de importação de XML ainda não implementada.')
        elif escolha == '2':
            print('\n[INFO] Função de registro de venda ainda não implementada.')
        elif escolha == '3':
            print('\n[INFO] Função de relátorios ainda não implementada.')
        elif escolha == '0':
            print('\nSaindo do sistema...')
            break
        else:
            print('\n[ERRO] Opção inválida. Tente novamente')

if __name__ == '__main__':
    main()
