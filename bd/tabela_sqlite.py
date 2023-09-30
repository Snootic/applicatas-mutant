import os
import sqlite3
from data import edit_config

class tabela:
    def __init__(self, table=''):
        self.tabela = table
    def CriarDirSchema(self):
        
        usuario = edit_config.getUser()
        CAMINHO_PASTA_DB = os.path.join(os.getcwd(),f'data/users/sqlite_databases')
        
        if not os.path.exists(CAMINHO_PASTA_DB):
            os.mkdir(CAMINHO_PASTA_DB)
            
        banco_de_dados = f'{usuario}'+'.db'
        CAMINHO_SCHEMA = os.path.join(CAMINHO_PASTA_DB,banco_de_dados)
        return CAMINHO_SCHEMA
    
    def CriarBD(self):
        CAMINHO_SCHEMA = self.CriarDirSchema()
        
        tabela = sqlite3.connect(CAMINHO_SCHEMA)
        cursor = tabela.cursor()
        cursor.execute(f"SELECT COUNT(name) FROM sqlite_master WHERE type='table' AND name='{self.tabela}';")
        resultado = cursor.fetchone()
        if resultado[0] == 1:
            return 'Tabela já existe'
        else:
            cursor.execute(f'''CREATE TABLE if not exists {self.tabela}(
                            ocorrencias VARCHAR,
                            custo REAL DEFAULT NULL)''')
            edit_config.EditarTabela(self.tabela)
            return 'Tabela Criada'
        
    def addValor(self, ocorrencias, custo='', quantidade=1): #Tabela, ocorrencias e custo (opcional)
        schema = self.CriarDirSchema()
        schema = sqlite3.connect(schema)
        cursor = schema.cursor()
        
        tabela = edit_config.getTabela()
        
        for i in range(quantidade):
            if custo != '':
                cursor.execute(f"INSERT INTO {tabela} VALUES(?,?)", (ocorrencias, custo))
            else:
                cursor.execute(f"INSERT INTO {tabela} (ocorrencias) VALUES(?)", (ocorrencias,))
            schema.commit()
        
    def atualizar_ocorrencia(self,ocorrenciaatual,novaocorrencia,quantidade=''):
        schema = self.CriarDirSchema()
        schema = sqlite3.connect(schema)
        cursor = schema.cursor()
        
        tabela = edit_config.getTabela()
        
        cursor.execute(f'SELECT ocorrencias from {tabela} WHERE ocorrencias="{ocorrenciaatual}"')
        sim = cursor.fetchall()
        
        cursor.execute(f"UPDATE {tabela} SET ocorrencias='{novaocorrencia}' WHERE ocorrencias='{ocorrenciaatual}'")
        schema.commit()
        
        cursor.execute(f'SELECT ocorrencias from {tabela} WHERE ocorrencias="{novaocorrencia}"')
        nao = cursor.fetchall()
        
        # return sim, nao
        
    def atualizar_custo(self,):
        pass
    
    def getTabelas(self):
        schema = self.CriarDirSchema()
        schema = sqlite3.connect(schema)
        cursor = schema.cursor()
        
        cursor.execute(f"SELECT name FROM sqlite_master")
        resultado = cursor.fetchall()
        
        return resultado
    
    def SelectTabela(self, tabela):
        edit_config.EditarTabela(tabela)