from sistema.modelos.produto import Produto
from sistema.modelos.lote import Lote
from datetime import timedelta, date



class Item:
    def __init__(self, produto: Produto, lote: Lote, quantidade_vendida):
        'cria o tipo Item a partir de outras classes com algumas caracteristicas unicas'
        self.produto = produto
        self.lote = lote
        self.quantidade_vendida = quantidade_vendida

    def __str__(self):
        'descreve o item'
        descricao = f'''
        1. Nome: {self.produto.nome}
        2. Lote: {self.lote.id_lote}
        3. Qtd: {self.quantidade_vendida}
        4. Data de Validade: {self.lote.data_validade}
        5. Código de barras: {self.produto.ean}
        '''
        return descricao
    
    def __repr__(self) -> str:
        'representacao tecnica do tipo Item'
        return f'1. Nome: {self.produto.nome} 2. Lote: {self.lote.id_lote} 3. Qtd: {self.quantidade_vendida} 4. Data de Validade: {self.lote.data_validade} 5. Código de barras: {self.produto.ean}'

    
    def calcular_subtotal(self):
        'acessa o preço de venda do produto e multiplica pela quantidade vendida para retornar o total dessa compra'

        preco = self.produto.preco_venda
        quantidade = self.quantidade_vendida

        subtotal = float(preco * quantidade)
        return subtotal
        

    def desconto(self):
        'aplica diferentes niveis de desconto baseado em proximidade da data de vencimento do item'

        hoje = date.today()
        validade = self.lote.data_validade
        intervalo: timedelta = (validade - hoje)
        diferenca = intervalo.days
        #print(diferenca)
        
        oito_dias = timedelta(days = 8)
        quinze_dias = timedelta(days = 16)
        vinte_dias = timedelta(days = 21)
        trinta_dias = timedelta(days = 31)     
                       
        preco_final = self.produto.preco_venda       

        # condicional de descontos 

        if diferenca < oito_dias:            
            oitenta_porcento = float(self.produto.preco_venda * 0.8)
            preco_final = float(self.produto.preco_venda - oitenta_porcento)                                     
                                    
        elif diferenca < quinze_dias:
            cinquenta_porcento = float(self.produto.preco_venda * 0.5)
            preco_final = float(self.produto.preco_venda - cinquenta_porcento)                
        
        elif diferenca < vinte_dias:
            trinta_porcento = float(self.produto.preco_venda * 0.3)
            preco_final = float(self.produto.preco_venda - trinta_porcento)                
        
        elif diferenca < trinta_dias:
            vinte_porcento = float(self.produto.preco_venda * 0.2)
            preco_final = float(self.produto.preco_venda - vinte_porcento)     
        
        
        # adiciona uma condicional que verifica se não há prejuizo
            
        if preco_final < self.lote.preco_custo:
            preco_retornar = self.produto.preco_venda
        else:
            preco_retornar = preco_final
        
        return preco_retornar        

        
            
            