import os
import sqlite3

class tabela:
    def criar_diretorio_tabela(self,nome_tabela): 
        diretorio_script = os.path.dirname(os.path.abspath(__file__))
        caminho_pasta_bd = os.path.join(diretorio_script,'tabelas')
        
        if not os.path.exists(caminho_pasta_bd):
            os.mkdir(caminho_pasta_bd)
            
        banco_de_dados = nome_tabela+'.db'
        caminho_bd = os.path.join(caminho_pasta_bd,banco_de_dados)
        return caminho_bd
    
    def criar_bd(self,nome_tabela):
        caminho_bd = self.criar_diretorio_tabela(nome_tabela)
        
        tabela_existente = os.path.exists(caminho_bd)

        tabela = sqlite3.connect(caminho_bd)
        cursor = tabela.cursor()
        
        if tabela_existente:
            return "tabela_existe"
        else:
            cursor.execute('''CREATE TABLE if not exists tabela(
            ocorrencias VARCHAR,
            custo REAL DEFAULT NULL)''')
            return f'{nome_tabela}'+".db"
        
    def adicionar_valor(self,*args): #Tabela, ocorrencias e custo (opcional)
        
        if len(args) == 3:
            tabela, ocorrencias, custo = args
            tabela = self.criar_diretorio_tabela(tabela)
            tabela = sqlite3.connect(tabela)
            cursor = tabela.cursor()
            cursor.execute("INSERT INTO tabela VALUES(?,?)", (ocorrencias, custo))
        
        elif len(args) == 2:
            tabela, ocorrencias = args
            tabela = self.criar_diretorio_tabela(tabela)
            tabela = sqlite3.connect(tabela)
            cursor = tabela.cursor()
            cursor.execute("INSERT INTO tabela (ocorrencias) VALUES(?)", (ocorrencias,))
        else:
            return 'argumentos_invalidos'

        tabela.commit()