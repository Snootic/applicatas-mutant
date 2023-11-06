import os
import sqlite3
from data import edit_config
import platform

class tabela:
    def __init__(self, table=''):
        self.tabela = table
    def CriarDirSchema(self, dados):
        
        usuario = edit_config.getUser()
        if platform.system() == 'Windows':
            CAMINHO_PASTA_DB = os.path.join(os.getcwd(),'data\\users\\sqlite_databases')
        else:
            CAMINHO_PASTA_DB = os.path.join(os.getcwd(),'data/users/sqlite_databases')
        
        if not os.path.exists(CAMINHO_PASTA_DB):
            os.mkdir(CAMINHO_PASTA_DB)
        
        if dados == 'pareto':
            banco_de_dados = f'{usuario}_pareto'+'.db'
        elif dados == 'medidas':
            banco_de_dados = f'{usuario}_medidas'+'.db'
        CAMINHO_SCHEMA = os.path.join(CAMINHO_PASTA_DB,banco_de_dados)
        return CAMINHO_SCHEMA
    
    def CriarBD(self,dados):
        CAMINHO_SCHEMA = self.CriarDirSchema(dados)
        tabela = sqlite3.connect(CAMINHO_SCHEMA)
        cursor = tabela.cursor()
        cursor.execute(f"SELECT COUNT(name) FROM sqlite_master WHERE type='table' AND name='{self.tabela}';")
        resultado = cursor.fetchone()
        if resultado[0] == 1:
            return 'Tabela já existe'
        else:
            if dados == 'pareto':
                cursor.execute(f'''CREATE TABLE if not exists {self.tabela}(
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                ocorrencias VARCHAR,
                                custo REAL DEFAULT NULL)''')
            elif dados == 'medidas':
                cursor.execute(f'''CREATE TABLE if not exists {self.tabela}(
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                medidas1 INTEGER)''')
                
            edit_config.EditarTabela(self.tabela,dados)
            return 'Tabela criada'
        
    def addValor_pareto(self, ocorrencias, custo='', quantidade=1): #Tabela, ocorrencias e custo (opcional)
        schema = self.CriarDirSchema('pareto')
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
        schema = self.CriarDirSchema('pareto')
        schema = sqlite3.connect(schema)
        cursor = schema.cursor()
        
        tabela = edit_config.getTabela()
        
        if quantidade == 0:
            cursor.execute(f"UPDATE {tabela} SET ocorrencias='{novaocorrencia}' WHERE ocorrencias='{ocorrenciaatual}'")
            schema.commit()
        else:
            cursor.execute(f"UPDATE {tabela} SET ocorrencias='{novaocorrencia}' WHERE ocorrencias='{ocorrenciaatual}' LIMIT {quantidade}")
            schema.commit()
            
    def atualizar_custo(self,ocorrenciaatual,custo):
        schema = self.CriarDirSchema('pareto')
        schema = sqlite3.connect(schema)
        cursor = schema.cursor()
        
        tabela = edit_config.getTabela()
        cursor.execute(f"UPDATE {tabela} SET custo='{custo}' WHERE ocorrencias='{ocorrenciaatual}'")
        schema.commit()
    
    def getTabelas(self,dados):
        schema = self.CriarDirSchema(dados)
        schema = sqlite3.connect(schema)
        cursor = schema.cursor()
        
        cursor.execute(f"SELECT name FROM sqlite_master")
        resultado = cursor.fetchall()
        
        resultado = [tabela for tabela in resultado if tabela[0] != 'sqlite_sequence']
                
        return resultado
    
    def SelectTabela(self, tabela, dados):
        edit_config.EditarTabela(tabela,dados)

    def add_valor_medidas(self, medida, conj_dados = 1):
        schema = self.CriarDirSchema('medidas')
        with sqlite3.connect(schema) as schema:
            cursor = schema.cursor()
            tabela = edit_config.getTabela()
            coluna = "medidas"+f'{conj_dados}'
            cursor.execute(f"""PRAGMA table_info({tabela})""")
            colunas_da_tabela = [linha[1] for linha in cursor.fetchall()]
            
            if coluna not in colunas_da_tabela:
                cursor.execute(f"""
                    ALTER TABLE {tabela}
                    ADD COLUMN {coluna} integer
                    """)
                schema.commit()
            cursor.execute(f"INSERT INTO {tabela} ({coluna}) VALUES(?)", (medida,))
            schema.commit()
     
    def att_valor_medidas(self, medida_atual, nova_medida, conj_dados):
        schema = self.CriarDirSchema('medidas')
        with sqlite3.connect(schema) as schema:
            cursor = schema.cursor()
            tabela = edit_config.getTabela()
            coluna = "medidas"+f'{conj_dados}'
            
            cursor.execute(f"UPDATE {tabela} SET {coluna}='{nova_medida}' WHERE {coluna}='{medida_atual}'")
            schema.commit()
            
    def get_TableColumns(self, medida):
        schema = self.CriarDirSchema('medidas')
        with sqlite3.connect(schema) as schema:
            cursor = schema.cursor()
            tabela = edit_config.getTabela()
            # coluna = "medidas"+f'{conj_dados}'
            cursor.execute(f"""PRAGMA table_info({tabela});""")
            colunas_da_tabela = [linha[1] for linha in cursor.fetchall()]
        
        colunas_da_tabela.remove('id')
        
        lista_colunas = []
        for i in range(len(colunas_da_tabela)):
            lista_colunas.append(f'conjunto {i+1}')
            
        return lista_colunas

    def delete_valor_pareto(self, ocorrencia, quantidade=0):
        schema = self.CriarDirSchema('pareto')
        with sqlite3.connect(schema) as schema:
            cursor = schema.cursor()
            tabela = edit_config.getTabela()
            
            if quantidade == 0:
                cursor.execute(f"DELETE FROM {tabela} WHERE ocorrencias='{ocorrencia}'")
                schema.commit()
            else:
                cursor.execute(f"DELETE FROM {tabela} WHERE ocorrencias='{ocorrencia}' LIMIT {quantidade}")
                schema.commit()