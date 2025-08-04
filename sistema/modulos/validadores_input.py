from datetime import datetime

def validador_pv():    
    'conversão de ponto para virgula visando o input do usuario | conversão float'
    while True:                                         
        preco_pergunta = f'Qual preço de venda deste novo item?: '
        preco_input = input(f'{preco_pergunta}')
        
        try:
            preco_digitado = float(preco_input.replace(',', '.'))
            if preco_digitado > 0:
                break
            else:
                print('\n [ERRO] O preço de venda deve ser maior que zero.') 
        except ValueError:
            print('\n [ERRO] Entrada inválida. Por favor, digite apenas números.')
    
    return preco_digitado


def validador_dv():
    'conversão de d/m/aa para aa/m/d para aceitação no sql'
    while True:                        
        validade_pergunta = f'Qual a validade deste novo item (DIA/MÊS/ANO)?: '
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
    
    return validade_digitada

def validador_qtd():
    'verifica se um numero é um inteiro positivo'
    
    while True:        
        quantidade_pergunta = f'Quantidade: '
        quantidade_input = input(f'{quantidade_pergunta}')

        try:            
            quantidade_formatada = int(quantidade_input)           
                            
            if quantidade_formatada > 0:
                break                                             
            else:
                print(f'[ERRO] Entrada inválida, insira apenas números. Tente novamente.')
        
        except ValueError:
            print(f'[ERRO] Dados inválidos. Tente novamente.')

    return quantidade_formatada