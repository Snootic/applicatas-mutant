import os
import sqlite3

class tabela:
    usuario: str
    def CriarDirTabela(self,nome_tabela):
        
        CAMINHO_PASTA_DB = os.path.join(os.getcwd(),f'data/users/sqlite_databases')
        
        if not os.path.exists(CAMINHO_PASTA_DB):
            os.mkdir(CAMINHO_PASTA_DB)
            
        banco_de_dados = nome_tabela+'.db'
        CAMINHO_SCHEMA = os.path.join(CAMINHO_PASTA_DB,banco_de_dados)
        return CAMINHO_SCHEMA
    
    def CriarBD(self,nome_tabela):
        CAMINHO_SCHEMA = self.CriarDirTabela(self.usuario)
        
        tabela_existente = os.path.exists(CAMINHO_SCHEMA)

        tabela = sqlite3.connect(CAMINHO_SCHEMA)
        cursor = tabela.cursor()
        
        if tabela_existente:
            return "tabela_existe"
        else:
            cursor.execute(f'''CREATE TABLE if not exists {nome_tabela}(
            ocorrencias VARCHAR,
            custo REAL DEFAULT NULL)''')
            return f'{nome_tabela}'+".db"
        
    def addValor(self,*args): #Tabela, ocorrencias e custo (opcional)
        
        if len(args) == 3:
            tabela, ocorrencias, custo = args
            tabela = self.CriarDirTabela(tabela)
            tabela = sqlite3.connect(tabela)
            cursor = tabela.cursor()
            cursor.execute("INSERT INTO tabela VALUES(?,?)", (ocorrencias, custo))
        
        elif len(args) == 2:
            tabela, ocorrencias = args
            tabela = self.CriarDirTabela(tabela)
            tabela = sqlite3.connect(tabela)
            cursor = tabela.cursor()
            cursor.execute("INSERT INTO tabela (ocorrencias) VALUES(?)", (ocorrencias,))
        else:
            return 'argumentos_invalidos'

        tabela.commit()