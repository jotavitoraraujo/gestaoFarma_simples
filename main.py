from sistema import database
from sistema.modulos import users
from sistema.modulos import importador_nfe
from sistema.modulos import vendas




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
            produtos_nota = importador_nfe.importar_nfe()
            
            if produtos_nota is not None:
                database.salvar_produtos(produtos_nota)
                print(f'[SUCESSO] A lista de produtos foi salva/atualizada.') 
            else:
                print(f'[ERRO] A lista de produtos está vazia. Verifique a NF-e e tente novamente.')                           
        
        elif escolha == '2':
            item = vendas.carrinho()
            if item is not None:
                print(item)
            else:
                print('[ERRO]' * 5)
            #print('\n [INFO] Função de registro de venda ainda não implementada.')
        
        elif escolha == '3':
            print('\n [INFO] Função de relátorios ainda não implementada.')
       
        elif escolha == '4':
            users.cadastro_usuario()            
       
        elif escolha == '0':
            print('\n Saindo do sistema...')
            break
       
        else:
            print('\n [ERRO] Opção inválida. Tente novamente')

if __name__ == '__main__':
    main()