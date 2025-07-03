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
    # pede o nome do arquivo xml e processa os dados.
    #print('\nDEBUG: Passo 1 - Entrando na função importar_nfe')
    caminho_arquivo = input('Digite o nome do arquivo XML (ex: exemplo_nfe.xml): ')
    #print(f'DEBUG: Passo 2 - Arquivo digitado pelo usuário: "{caminho_arquivo}"')
    #print('DEBUG: Passo 3 - Chamando a função para ler o XML em leitorXML.py')
    produtos_nota = leitorXML.extrair_dados_nfe(caminho_arquivo)
    #print(f'DEBUG: Passo 4 - Retorno da função do leitorXML: {produtos_nota}')

    if produtos_nota:
        #print('DEBUG: Passo 5 - A lista de produtos não está vazia. Imprimindos produtos.')
        print('\n--- Produtos Encontrados na Nota Fiscal ---')
        for produto in produtos_nota:
            # imprime os dados de forma mais legivel
            print(f' Código: {produto['codigo']}')
            print(f' Nome: {produto['nome']}')
            print(f' Qtde: {produto['quantidade']}')
            print(f' Custo Unitário: R${produto['preco_custo']:.2f}')
            print('-' * 30)
        # LOCAL DA IMPLEMENTAÇÃO DO BANCO DE DADOS
        print('\n [INFO] O próximo passo é adicionar esses produtos ao estoque.')
    else:
        print('DEBUG: Passo 5 - A lista de produtos está vazia ou é None. Nada a imprimir.')

def main():
    # Garantir que a tabela no bd exista.
    database.criar_tabela_produtos()

    while True:
        escolha = exibir_menu()
        if escolha == '1':
            importar_nfe()
            #print('\n[INFO] Função de importação de XML ainda não implementada.')
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
