import os
import sqlite3
from data import edit_config
import platform

class tabela:
    def __init__(self, table=''):
        self.tabela = table
    def CriarDirSchema(self):
        
        usuario = edit_config.getUser()
        if platform.system() == 'Windows':
            CAMINHO_PASTA_DB = os.path.join(os.getcwd(),'data\\users\\sqlite_databases')
        else:
            CAMINHO_PASTA_DB = os.path.join(os.getcwd(),'data/users/sqlite_databases')
        
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
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            ocorrencias VARCHAR,
                            custo REAL DEFAULT NULL)''')
            edit_config.EditarTabela(self.tabela)
            return 'Tabela criada'
        
    def addValor(self, ocorrencias, custo='', quantidade=1): #Tabela, ocorrencias e custo (opcional)
        schema = self.CriarDirSchema()
        schema = sqlite3.connect(schema)
        cursor = schema.cursor()
        
        tabela = edit_config.getTabela()
        
        for i in range(quantidade):
            if custo != '':
                cursor.execute(f"INSERT INTO {tabela} (ocorrencias,custo) VALUES(?,?)", (ocorrencias, custo))
            else:
                cursor.execute(f"INSERT INTO {tabela} (ocorrencias) VALUES(?)", (ocorrencias,))
            schema.commit()
        
    def atualizar_ocorrencia(self,ocorrenciaatual,novaocorrencia,quantidade=0):
        schema = self.CriarDirSchema()
        schema = sqlite3.connect(schema)
        cursor = schema.cursor()
        
        tabela = edit_config.getTabela()
        
        cursor.execute(f'SELECT id, ocorrencias from {tabela} WHERE ocorrencias="{ocorrenciaatual}"')
        lista_com_ids= cursor.fetchall()

        if quantidade == 0:
            cursor.execute(f"UPDATE {tabela} SET ocorrencias='{novaocorrencia}' WHERE ocorrencias='{ocorrenciaatual}'")
            schema.commit()
        else:
            if quantidade > len(lista_com_ids):
                    print('Quantidade listada maior do que ocorrência existente')
                    return 'Quantidade listada maior do que ocorrência existente'
            else:
                for i in range(quantidade):
                        cursor.execute(f"UPDATE {tabela} SET ocorrencias='{novaocorrencia}' WHERE ocorrencias='{ocorrenciaatual}' AND id={lista_com_ids[0][0]}")
                        lista_com_ids.remove(lista_com_ids[0])
                        schema.commit()
            
    def atualizar_custo(self,):
        pass
    
    def getTabelas(self):
        schema = self.CriarDirSchema()
        schema = sqlite3.connect(schema)
        cursor = schema.cursor()
        
        cursor.execute(f"SELECT name FROM sqlite_master")
        resultado = cursor.fetchall()
        
        resultado = [tabela for tabela in resultado if tabela[0] != 'sqlite_sequence']
                
        return resultado
    
    def SelectTabela(self, tabela):
        edit_config.EditarTabela(tabela)