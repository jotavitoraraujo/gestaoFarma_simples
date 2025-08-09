from datetime import datetime
import logging

def validador_pv() -> float:    
    'conversão de ponto para virgula visando o input do usuario | conversão float'
    while True:                                         
        preco_pergunta = f'Qual preço de venda deste novo item?: '
        preco_input = input(f'{preco_pergunta}')
        
        try:
            preco_digitado = float(preco_input.replace(',', '.'))
            if preco_digitado > 0:
                break
            else:
                logging.error('\n [ERRO] O preço de venda deve ser maior que zero.') 
        except ValueError:
            logging.error('\n [ERRO] Entrada inválida. Por favor, digite apenas números.')
    
    return preco_digitado


def validador_dv() -> str:
    'conversão de d/m/aa para aa/m/d para aceitação no sql'
    while True:                        
        validade_pergunta = f'Qual a validade deste novo item? (DIA/MÊS/ANO): '
        validade_input = input(f'{validade_pergunta}')                        
        
        try:            
            validade_lista = validade_input.split('/')
            validade_formatada = f'{validade_lista[2]}-{validade_lista[1]}-{validade_lista[0]}'
            validade_digitada = datetime.strptime(validade_formatada, '%Y-%m-%d').date()
            
            if validade_digitada > datetime.now().date():
                break
            else:
                logging.error(f'\n [ERRO] Data de validade inferior ou igual a data de hoje.')        
        except:
            logging.error(f'\n [ERRO] Data inválida, por favor tente novamente.')
    
    return validade_digitada

def validador_lotef() -> str:
    'valida a entrada do lote fisico impresso no produto'
    while True:
        lote_pergunta = f'Qual o lote impresso fisicamente neste item? (EX: AB123CD): '
        lote_input = input(f'{lote_pergunta}')
        print(f'O lote informado é ***{lote_input}***.')
        print(f'Você confirma que o lote ***{lote_input}*** está correto? ')
        lote_confirmacao = input(f'Digite 1 para confirmar ou 0 para corrigir: ')
        
        if len(lote_confirmacao) > 1:
            logging.error(f'[ERRO] Digite apenas 1 ou 0. Tente novamente')
        elif len(lote_confirmacao) < 1:
            logging.error(f'[ERRO] Digite apenas 1 ou 0. Tente novamente.')
        else:
            if lote_confirmacao == '1':
                lote_fisico = lote_input
            elif lote_confirmacao == '0':
                continue
            else:
                logging.error(f'[ERRO] Opção inválida. Tente novamente.')
        return lote_fisico
        

def validador_qtd() -> int:
    'verifica se um numero é um inteiro positivo'
    
    while True:        
        quantidade_pergunta = f'Quantidade: '
        quantidade_input = input(f'{quantidade_pergunta}')

        try:            
            quantidade_formatada = int(quantidade_input)           
                            
            if quantidade_formatada > 0:
                break                                             
            else:
                logging.error(f'[ERRO] Entrada inválida, insira apenas números. Tente novamente.')
        
        except ValueError:
            logging.error(f'[ERRO] Dados inválidos. Tente novamente.')

    return quantidade_formatada