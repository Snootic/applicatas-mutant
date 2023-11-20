from time import sleep
from data import edit_config
from bd.sqlite import tabela
import platform, os, sqlite3

class Salvar():
    def __init__(self) -> None:
        self.user = edit_config.getUser()
        
        if platform.system() == 'Windows':
            self.dump_path = os.path.join(os.getcwd(),'data\\users\\sqlite_databases\\backup')
        else:
            self.dump_path = os.path.join(os.getcwd(),'data/users/sqlite_databases/backup')
            
        self.redoing = edit_config.getRedo()
        self.redoing = self.redoing.strip('[]').replace("'", "").replace(' ','').split(',')

        self.undoing = edit_config.getUndo()
        self.undoing = self.undoing.strip('[]').replace("'", "").replace(' ','').split(',')
        
        self.schemas = ['pareto', 'medidas']
        self.save_path = []
        for i in self.schemas:
            self.save_path.append(os.path.join(self.dump_path,f'{self.user}_{i}_save_temp.sql'))
    
    def save(self):
        schema = tabela()
        
        for index, valor in enumerate(self.schemas):
            database = schema.CriarDirSchema(valor)
            
            if os.path.exists(self.save_path[index]):
                os.remove(self.save_path[index])
                
            with sqlite3.connect(database) as conn, open(self.save_path[index], 'w', encoding='utf-8') as save:
                for line in conn.iterdump():
                    save.writelines(line+'\n')
                    
        edit_config.setIsSaved(True)
        
    def dontSave(self):
        schema = tabela()
            
        for index, valor in enumerate(self.schemas):
            database = schema.CriarDirSchema(valor)
            try:
                with open(self.save_path[index], 'r', encoding='utf-8') as sf:
                    last_save = sf.read()
            except Exception as e:
                print(e)
                bkp_list = self.undoing + self.redoing
                
                if f'{self.user}_{valor}_bkp0.sql' in bkp_list:
                    bkp_file = f'{self.user}_{valor}_bkp0.sql'
                try:
                    bkp_file = os.path.join(self.dump_path,bkp_file)
                    
                    with open(bkp_file, 'r', encoding='utf-8') as bkp:
                        last_save = bkp.read()
                except Exception as e:
                    print(e)
                    return
            
            for i in schema.getTabelas(valor):
                schema.DropTable(i[0],valor)
            
            with sqlite3.connect(database) as conn:
                cursor = conn.cursor()
                cursor.executescript(last_save)
        return