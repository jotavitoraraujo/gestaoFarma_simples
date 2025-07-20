from sistema import database
from sistema.modulos import users
from sistema.modulos import importador_nfe




def exibir_menu():
    'Exibe o menu principal e retorna a escolha do usuário.'
    print('\n--- Sistema de Gestão da Farmácia ---')
    print('1. Importar Nota Fiscal (XML)')
    print('2. Registrar Venda')
    print('3. Ver Relátorios')
    print('4. Cadastrar Novo Usuário')
    print('0. Sair')
    return input('Escolha uma opção: ')
    

def main():
    'acesso as funções do menu principal'
    database.criar_tabelas()

    while True:
        escolha = exibir_menu()
        if escolha == '1':
            importador_nfe.importar_nfe()
            # print('\n[INFO] Função de importação de XML ainda não implementada.')
        elif escolha == '2':
            print('\n [INFO] Função de registro de venda ainda não implementada.')
        elif escolha == '3':
            print('\n [INFO] Função de relátorios ainda não implementada.')
        elif escolha == '4':
            users.cadastro_usuario()
            #print('\n [INFO] Função de cadastro ainda não implementada.')
        elif escolha == '0':
            print('\n Saindo do sistema...')
            break
        else:
            print('\n [ERRO] Opção inválida. Tente novamente')

if __name__ == '__main__':
    main()
