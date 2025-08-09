from sistema import database
import logging
from sistema.modulos import config_log
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
    config_log.sistema_logs()

    while True:
        
        escolha = exibir_menu()
        
        if escolha == '1':
            produtos_nota = importador_nfe.importar_nfe()
            
            if produtos_nota is not None:
                database.salvar_produtos(produtos_nota)
                logging.info('[INFO] A lista de produtos foi salva/atualizada, com sucesso.') 
            else:
                logging.error('[ERRO] A lista de produtos está vazia. Verifique a NF-e e tente novamente.')                           
        
        elif escolha == '2':
            item = vendas.adicionar_item()
            if item is not None:
                pass
            else:
                logging.error('[ERRO] Nenhum item encontrado. Tente novamente.' )            
        
        elif escolha == '3':
            print('\n [INFO] Função de relátorios ainda não implementada.')
       
        elif escolha == '4':
            users.cadastro_usuario()            
       
        elif escolha == '0':
            logging.info('\n[INFO] Sistema finalizado.')
            break
       
        else:
            logging.error('\n [ERRO] Opção inválida. Tente novamente')

if __name__ == '__main__':
    main()