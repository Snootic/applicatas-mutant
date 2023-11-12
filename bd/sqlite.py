from calendar import c
import os
import sqlite3
from sqlite_dump import iterdump
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
    
    def att_config_table(self,tabela, dados):
            CAMINHO_SCHEMA = self.CriarDirSchema(dados)
            edit_config.EditarTabela(tabela,dados)
            edit_config.editSchema(CAMINHO_SCHEMA)
    
    def DropTable(self, tabela, dados):
        CAMINHO_SCHEMA = self.CriarDirSchema(dados)
        conn = sqlite3.connect(CAMINHO_SCHEMA)
        schema = edit_config.getSchema('tab')
        schema = schema.split('.')[0]
        cursor = conn.cursor()
        self.dump(dados)
        cursor.execute(f"DROP TABLE {tabela}")
    
    def CriarBD(self, dados):
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
            self.att_config_table(self.tabela,dados)
            self.dump(dados)
            return 'Tabela criada'
        
    def addValor_pareto(self, ocorrencias, custo='', quantidade=1): #Tabela, ocorrencias e custo (opcional)
        schema = self.CriarDirSchema('pareto')
        schema = sqlite3.connect(schema)
        cursor = schema.cursor()
        self.dump(dados='pareto')
        
        tabela = edit_config.getTabela()
        
        for i in range(quantidade):
            if custo != '':
                cursor.execute(f"INSERT INTO {tabela} (ocorrencias,custo) VALUES(?,?)", (ocorrencias, custo))
            else:
                cursor.execute(f"INSERT INTO {tabela} (ocorrencias) VALUES(?)", (ocorrencias,))
            self.att_config_table(tabela,'pareto')
            schema.commit()
        
    def atualizar_ocorrencia(self,ocorrenciaatual,novaocorrencia,quantidade=0):
        schema = self.CriarDirSchema('pareto')
        schema = sqlite3.connect(schema)
        cursor = schema.cursor()
        self.dump(dados='pareto')
        
        tabela = edit_config.getTabela()
        
        if quantidade == 0:
            cursor.execute(f"UPDATE {tabela} SET ocorrencias='{novaocorrencia}' WHERE ocorrencias='{ocorrenciaatual}'")
        else:
            cursor.execute(f"UPDATE {tabela} SET ocorrencias='{novaocorrencia}' WHERE ocorrencias='{ocorrenciaatual}' LIMIT {quantidade}")
        self.att_config_table(tabela,'pareto')
        schema.commit()
            
    def atualizar_custo(self,ocorrenciaatual,custo):
        schema = self.CriarDirSchema('pareto')
        schema = sqlite3.connect(schema)
        cursor = schema.cursor()
        self.dump(dados='pareto')
        
        tabela = edit_config.getTabela()
        cursor.execute(f"UPDATE {tabela} SET custo='{custo}' WHERE ocorrencias='{ocorrenciaatual}'")
        self.att_config_table(tabela,'pareto')
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
            
            self.dump(dados='medidas')
            
            if coluna not in colunas_da_tabela:
                cursor.execute(f"""
                    ALTER TABLE {tabela}
                    ADD COLUMN {coluna} integer
                    """)
                schema.commit()
            cursor.execute(f"INSERT INTO {tabela} ({coluna}) VALUES(?)", (medida,))
            self.att_config_table(tabela,'medidas')
            schema.commit()
     
    def att_valor_medidas(self, medida_atual, nova_medida, conj_dados):
        schema = self.CriarDirSchema('medidas')
        with sqlite3.connect(schema) as schema:
            cursor = schema.cursor()
            tabela = edit_config.getTabela()
            coluna = "medidas"+f'{conj_dados}'
            self.dump(dados='medidas')
            
            cursor.execute(f"UPDATE {tabela} SET {coluna}='{nova_medida}' WHERE {coluna}='{medida_atual} LIMIT 1'")
            self.att_config_table(tabela,'medidas')
            schema.commit()
            
    def get_TableColumns(self, medida):
        schema = self.CriarDirSchema('medidas')
        with sqlite3.connect(schema) as schema:
            cursor = schema.cursor()
            tabela = edit_config.getTabela()
            # coluna = "medidas"+f'{conj_dados}'
            cursor.execute(f"""PRAGMA table_info({tabela})""")
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
            self.dump(dados='pareto')
            
            if quantidade == 0:
                cursor.execute(f"DELETE FROM {tabela} WHERE ocorrencias='{ocorrencia}'")
            else:
                cursor.execute(f"DELETE FROM {tabela} WHERE ocorrencias='{ocorrencia}' LIMIT {quantidade}")
            self.att_config_table('pareto')
            schema.commit()
                
    def delete_valor_medidas(self, dado, conj_dados):
        schema = self.CriarDirSchema('medidas')
        with sqlite3.connect(schema) as schema:
            cursor = schema.cursor()
            coluna = "medidas"+f'{conj_dados}'
            tabela = edit_config.getTabela()
            self.dump(dados='medidas')
            
            cursor.execute(f"DELETE FROM {tabela} WHERE {coluna}='{dado}' LIMIT 1")
            self.att_config_table(tabela,'medidas')
            schema.commit()

    def dump(self, dados='', redo=False):
        schema = self.CriarDirSchema(dados)
        if platform.system() == 'Windows':
            dump_path = os.path.join(os.getcwd(),'data\\users\\sqlite_databases\\backup')
            banco_de_dados = schema.split('\\')[-1].split('.')[0]
        else:
            dump_path = os.path.join(os.getcwd(),'data/users/sqlite_databases/backup')
            banco_de_dados = schema.split('/')[-1].split('.')[0]
        
        undo = 0
        undoing = edit_config.getUndo()
        undoing = undoing.strip('[]').replace("'", "").replace(' ','').split(',')
        
        redoing = edit_config.getRedo()
        redoing = redoing.strip('[]').replace("'", "").replace(' ','').split(',')
        
        if undoing[0] == '':
            undoing.remove(undoing[0])
        if redoing[0] == '':
            redoing.remove(redoing[0])
        
        while True:
            bd = f'{banco_de_dados}_bkp{undo}.txt'
            if any(bd in s for s in undoing) or any(bd in s for s in redoing):
                undo +=1
            else:
                undoing.append(bd)
                break
        
        dump_path = os.path.join(dump_path, bd)
            
        with sqlite3.connect(schema) as conn:
            with open(dump_path, 'w', encoding='utf-8') as dump:
                for line in conn.iterdump():
                    dump.writelines(line+'\n')
                edit_config.editarUndo(undoing)
                    
    def restore(self,dados, manual = False, redo=False):
        schema = self.CriarDirSchema(dados)
            
        if manual == False:
            if platform.system() == 'Windows':
                    dump_path = os.path.join(os.getcwd(),'data\\users\\sqlite_databases\\backup')
            else:
                dump_path = os.path.join(os.getcwd(),'data/users/sqlite_databases/backup')

            redoing = edit_config.getRedo()
            redoing = redoing.strip('[]').replace("'", "").replace(' ','').split(',')

            undoing = edit_config.getUndo()
            undoing = undoing.strip('[]').replace("'", "").replace(' ','').split(',')
            
            if undoing[0] == '':
                undoing.remove(undoing[0])
            if redoing[0] == '':
                redoing.remove(redoing[0])
            
            if redo == False:
                if undoing:
                    dump_path = os.path.join(dump_path,undoing[-1])
                    redoing.append(undoing[-1])
                    undoing.remove(undoing[-1])
                else:
                    return
                
            else:
                if redoing:
                    dump_path = os.path.join(dump_path,redoing[-1]) 
                    undoing.append(redoing[-1])
                    redoing.remove(redoing[-1])
                else:
                    return
                    
            try:   
                with open(dump_path, 'r', encoding='utf-8') as dump:
                    edit_config.editarUndo(undoing)
                    edit_config.editarRedo(redoing)
                    lines = dump.readlines()
                    incomplete_line = ''
            except Exception as e:
                print(e,': Erro')
            else:
                if os.path.exists(schema):
                    os.remove(schema)
                with sqlite3.connect(schema) as conn:
                    cursor = conn.cursor()
                    for line in lines:
                        line = line.replace('\n','')
                        if line[-1] != ';' or (len(incomplete_line) >1 and 
                                            incomplete_line[-1] != ';'):
                            incomplete_line += line.lstrip()
                            if incomplete_line[-1] == ';':
                                line = incomplete_line
                        try:
                            cursor.execute(f'{line}')
                            incomplete_line = ''
                        except Exception as e:
                            print(e)
                    conn.commit()