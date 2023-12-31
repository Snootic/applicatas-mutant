import os
import sqlite3
# from sqlite_dump import iterdump
from data import edit_config
from time import sleep

class tabela:
    def __init__(self, table=''):
        self.tabela = table
    def CriarDirSchema(self, dados):
        
        usuario = edit_config.getUser()
        CAMINHO_DBS = os.path.join(os.getcwd(),f'data/users/sqlite_databases/')
        CAMINHO_PASTA_DB = os.path.join(os.getcwd(),f'data/users/sqlite_databases/{usuario}')
        
        if not os.path.exists(CAMINHO_DBS):
            os.mkdir(CAMINHO_DBS)
            
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
    
    def DropTable(self, tabela, dados, dump=True):
        CAMINHO_SCHEMA = self.CriarDirSchema(dados)
        with sqlite3.connect(CAMINHO_SCHEMA) as conn:
            schema = edit_config.getSchema('tab')
            schema = schema.split('.')[0]
            cursor = conn.cursor()
            if dump == True:
                self.dump(dados)
            cursor.execute(f"DROP TABLE {tabela}")
    
    def CriarBD(self, dados):
        CAMINHO_SCHEMA = self.CriarDirSchema(dados)
        with sqlite3.connect(CAMINHO_SCHEMA) as tabela:
            cursor = tabela.cursor()
            cursor.execute(f"SELECT COUNT(name) FROM sqlite_master WHERE type='table' AND name='{self.tabela}';")
            resultado = cursor.fetchone()

            if resultado[0] == 1:
                self.att_config_table(self.tabela,dados)
                return 'Tabela já existe'
            else:
                self.dump(dados)
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
                return 'Tabela criada'
        
    def addValor_pareto(self, ocorrencias, custo='', quantidade=1): #Tabela, ocorrencias e custo (opcional)
        schema = self.CriarDirSchema('pareto')
        with sqlite3.connect(schema) as schema:
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
        
    def atualizar_ocorrencia(self,ocorrenciaatual,novaocorrencia,custo=0,quantidade=0):
        schema = self.CriarDirSchema('pareto')
        with sqlite3.connect(schema) as schema:
            cursor = schema.cursor()
            
            tabela = edit_config.getTabela()
            
            cursor.execute(f"SELECT * FROM {tabela} WHERE ocorrencias='{ocorrenciaatual}'")
            result = cursor.fetchone()
            if result == None:
                return False
            if novaocorrencia == '' or novaocorrencia == ' ':
                return False
            
            self.dump(dados='pareto')
            if custo == 0:
                if quantidade == 0:
                    cursor.execute(f"UPDATE {tabela} SET ocorrencias='{novaocorrencia}' WHERE ocorrencias='{ocorrenciaatual}'")
                else:
                    cursor.execute(f"UPDATE {tabela} SET ocorrencias='{novaocorrencia}' WHERE ocorrencias='{ocorrenciaatual}' LIMIT {quantidade}")
            else:
                if quantidade == 0:
                    cursor.execute(f"UPDATE {tabela} SET custo='{custo}' WHERE ocorrencias='{ocorrenciaatual}'")
                    cursor.execute(f"UPDATE {tabela} SET ocorrencias='{novaocorrencia}' WHERE ocorrencias='{ocorrenciaatual}'")
                else:
                    cursor.execute(f"UPDATE {tabela} SET custo='{custo}' WHERE ocorrencias='{ocorrenciaatual}' LIMIT {quantidade}")
                    cursor.execute(f"UPDATE {tabela} SET ocorrencias='{novaocorrencia}' WHERE ocorrencias='{ocorrenciaatual}' LIMIT {quantidade}")
            self.att_config_table(tabela,'pareto')
            schema.commit()
            
            self.att_config_table(tabela,'pareto')
            schema.commit()
            return True
            
    def getTabelas(self,dados):
        schema = self.CriarDirSchema(dados)
        with sqlite3.connect(schema) as schema:
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
            try:
                cursor.execute(f"SELECT * FROM {tabela} WHERE {coluna}='{medida_atual}'")
            except:
                return False
            result = cursor.fetchone()
            if result == None:
                return False
            
            self.dump(dados='medidas')
            
            cursor.execute(f"UPDATE {tabela} SET {coluna}='{nova_medida}' WHERE {coluna}='{medida_atual}' LIMIT 1")
            schema.commit()
            self.att_config_table(tabela,'medidas')
            return True
            
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
            
            cursor.execute(f"SELECT * FROM {tabela} WHERE ocorrencias='{ocorrencia}'")
            result = cursor.fetchone()
            if result == None:
                return False
            
            self.dump(dados='pareto')
            if quantidade == 0:
                cursor.execute(f"DELETE FROM {tabela} WHERE ocorrencias='{ocorrencia}'")
            else:
                cursor.execute(f"DELETE FROM {tabela} WHERE ocorrencias='{ocorrencia}' LIMIT {quantidade}")
            self.att_config_table(tabela,'pareto')
            schema.commit()
            return True
                
    def delete_valor_medidas(self, dado, conj_dados):
        schema = self.CriarDirSchema('medidas')
        with sqlite3.connect(schema) as schema:
            cursor = schema.cursor()
            coluna = "medidas"+f'{conj_dados}'
            tabela = edit_config.getTabela()
            
            try:
                cursor.execute(f"SELECT * FROM {tabela} WHERE {coluna}='{dado}'")
            except:
                return False
            result = cursor.fetchone()
            if result == None:
                return False
            
            self.dump(dados='medidas')
            cursor.execute(f"DELETE FROM {tabela} WHERE {coluna}='{dado}' LIMIT 1")
            self.att_config_table(tabela,'medidas')
            schema.commit()
            return True

    def dump(self, dados='', manual=False, path=None, tabela=None):
        schema = self.CriarDirSchema(dados)
        dump_path = os.path.join(os.getcwd(),'data/users/sqlite_databases/backup/')
        banco_de_dados = schema.replace('\\','/').split('/')[-1].split('.')[0]
        
        if not os.path.exists(dump_path):
            os.makedirs(os.path.dirname(dump_path))

        if manual == False:
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
                bd = f'{banco_de_dados}_bkp{undo}.sql'
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
        else:
            with sqlite3.connect(schema) as conn:
                with open(path, 'w', encoding='utf-8') as dump:
                    for line in conn.iterdump():
                        if line.startswith(('BEGIN',
                                            f'CREATE TABLE {tabela}',
                                            f'INSERT INTO {tabela}',
                                            f'DELETE FROM',
                                            f'INSERT INTO "{tabela}"',
                                            f'''INSERT INTO "sqlite_sequence" VALUES('{tabela}''')):
                            dump.writelines(line+'\n')
                    
    def restore(self,
                dados,
                manual = False,
                redo = False,
                file=None):
        schema = self.CriarDirSchema(dados)
        
        if manual == False:
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
                    try:
                        dump_path = os.path.join(dump_path,undoing[-1])
                    except IndexError:
                        pass
                    else:
                        redoing.append(undoing[-1])
                        undoing.remove(undoing[-1])
                else:
                    return
                
            else:
                if redoing:
                        try:
                            if len(redoing) > 1:
                                undoing.append(redoing[-1])
                                redoing.remove(redoing[-1])
                                dump_path = os.path.join(dump_path,redoing[-1])
                            else:
                                dump_path = os.path.join(dump_path,redoing[0])
                                undoing.append(redoing[-1])
                                redoing.remove(redoing[-1])
                                
                        except IndexError:
                            pass
                        
                else:
                    return
                
            try:   
                with open(dump_path, 'r', encoding='utf-8') as dump:
                    edit_config.editarUndo(undoing)
                    edit_config.editarRedo(redoing)
                    lines = dump.read()
            except Exception as e:
                print(e,': Erro')
            else:
                for i in self.getTabelas(dados):
                    try:
                        self.DropTable(dados=dados,tabela=i, dump=False)
                    except:
                        self.DropTable(dados=dados,tabela=i[0], dump=False)
                    
                with sqlite3.connect(schema) as conn:
                    cursor = conn.cursor()
                    try:
                        cursor.executescript(lines)
                    except Exception as e:
                        print(e)
                    else:
                        conn.commit()
    
        else:
            try:
                with open(file, 'r', encoding='utf-8') as dump:
                    lines = dump.read()
                    separated_lines = lines.split('\n')
            except Exception as e:
                print(e)
            else:
                table = separated_lines[1].split(' ')
                table = table[-1].split('(')[0]
                try:
                    self.DropTable(dados=dados, tabela=table)
                except Exception as e: 
                    print(e)
                with sqlite3.connect(schema) as conn:
                    cursor = conn.cursor()
                    try:
                        cursor.executescript(lines)
                    except Exception as e:
                        print(e)
                    else:
                        conn.commit()

