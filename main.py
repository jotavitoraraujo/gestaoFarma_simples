import os
import sistema.database as database
import sistema.modulos.leitorXML as leitorXML
from datetime import datetime



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
                    resposta_db = database.buscar_produto(produto['codigo'])
                    if resposta_db == None:
                        print(f'\n A resposta do database retornou vazia...')
                    else:                    
                        #print('\n [DEBUG]', resposta_db)
                        produto['preco_venda'] = resposta_db[2]
                        produto['data_validade'] = resposta_db[3]                    
                else:
                    print(f'\n [NOVO PRODUTO ENCONTRADO]: {produto['nome']}')                    
                    
                    while True:                        
                        # conversão de ponto para virgula visando o input do usuario | conversão float                        
                        preco_pergunta = f'\n Qual preço de venda deste novo item?: '
                        preco_input = input(f'{preco_pergunta}')
                        try:
                            preco_digitado = float(preco_input.replace(',', '.'))
                            if preco_digitado > 0:
                                break
                            else:
                                print('\n [ERRO] O preço de venda deve ser maior que zero.') 
                        except ValueError:
                            print('\n [ERRO] Entrada inválida. Por favor, digite apenas números.')                   
                        
                    while True:                        
                        # conversão de d/m/aa para aa/m/d para aceitação no sql
                        validade_pergunta = f'\n Qual a validade deste novo item (DIA/MÊS/ANO)?: '
                        validade_input = input(f'{validade_pergunta}')                        
                        try:
                            validade_lista = validade_input.split('/')
                            validade_formatada = f'{validade_lista[2]}-{validade_lista[1]}-{validade_lista[0]}'
                            validade_digitada = datetime.strptime(validade_formatada, '%Y-%m-%d').date()
                            if validade_digitada > datetime.now().date():
                                break
                            else:
                                print(f'\n [ERRO] Data de validade inferior ou igual a data de hoje.')

                        except:
                            print(f'\n [ERRO] Data inválida, por favor tente novamente.')                    
                    produto['preco_venda'] = preco_digitado
                    produto['data_validade'] = validade_digitada
        
        print('\n--- Produtos a serem salvos/atualizados ---')   
        for produto in produtos_nota:
            # imprime os dados de forma mais legivel
            print(f'\n Código: {produto.get('codigo')}')
            print(f'\n Nome: {produto.get('nome')}')
            print(f'\n Qtde: {produto.get('quantidade')}')
            print(f'\n Custo Unitário: R${produto.get('preco_custo'):.2f}')
            if produto.get('preco_venda'):
                print(f'\n Preço de Venda: R$ {produto.get('preco_venda', 0):.2f}')
            if produto.get('data_validade'):
                print(f'\n Validade: {produto.get('data_validade')}')
            print('-' * 30)
        database.salvar_produtos(produtos_nota)        
    else:
        print('\n [INFO] Nenhum produto encontrado ou erro na leitura do arquivo.')

def main():
    'Garantir que a tabela no bd exista.'
    database.criar_tabelas()

    while True:
        escolha = exibir_menu()
        if escolha == '1':
            importar_nfe()
            # print('\n[INFO] Função de importação de XML ainda não implementada.')
        elif escolha == '2':
            print('\n [INFO] Função de registro de venda ainda não implementada.')
        elif escolha == '3':
            print('\n [INFO] Função de relátorios ainda não implementada.')
        elif escolha == '0':
            print('\n Saindo do sistema...')
            break
        else:
            print('\n [ERRO] Opção inválida. Tente novamente')

if __name__ == '__main__':
    main()
