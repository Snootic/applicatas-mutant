import glob
from bd.sqlite import *

def criar_config():
    config = ["tema=cyborg",
              "ultimo_schema=",
              "ultima_tabela=",
              "schema_caminho=",
              "user=",
              "senha=",
              "undo=",
              "redo=",
              "saved=True",
              "autosave=False",
              "manter_logado=False",
              "escala="]
    config_caminho = os.path.abspath('data/app_config.txt')
    with open(config_caminho, 'a', encoding='utf-8') as configuracoes:
        for i in config:
            configuracoes.writelines(i + '\n')

def LerConfig(argumento):
    """
    'config': retorna caminho absoluto das configurações ->
    'itens': retorna lista das variaveis das configurações ->
    'linhas': retorna as configurações brutas ->
    'dirtab': retorna diretorio da schema mais recente ->
    """
    CAMINHO_CONFIG = (os.path.abspath('data/app_config.txt'))
    if not os.path.exists(CAMINHO_CONFIG):
        criar_config()
    dir_schema = None
    
    with open(CAMINHO_CONFIG, 'r', encoding='utf-8') as configuracoes:
        linhas = configuracoes.readlines()
        itens = []
        for linha in linhas:
            itens.append(linha.strip().split('='))
        
        for i in range(len(itens)):
            if itens[i][0] == "schema_caminho":
                dir_schema = itens[i][1]
                
    if argumento == 'config':
        return CAMINHO_CONFIG
    elif argumento == 'itens':
        return itens
    elif argumento == 'linhas':
        return linhas
    elif argumento == 'dirtab':
        return dir_schema


def EditarTabela(table,dados):
    tabela1 = tabela()
    user = getUser()
    CAMINHO_SCHEMA = tabela1.CriarDirSchema(dados)
    CAMINHO_CONFIG = LerConfig('config')
    itens = LerConfig('itens')
    linhas = LerConfig('linhas')

    with open(CAMINHO_CONFIG, 'w', encoding='utf-8') as configuracoes:
        for i in range(len(itens)):
            if itens[i][0] == 'ultimo_schema':
                if dados == 'medidas':
                    linhas[i] = 'ultimo_schema='+f'{user}_medidas.db\n'
                else:
                    linhas[i] = 'ultimo_schema='+f'{user}_pareto.db\n'
                
            if itens[i][0] == 'schema_caminho':
                linhas[i] = 'schema_caminho='+f'{CAMINHO_SCHEMA}'+'\n'
                
            if itens[i][0] == 'ultima_tabela':
                linhas[i] = 'ultima_tabela='+f'{table}'+'\n'

        configuracoes.writelines(linhas)
    
def getSchema(argumento):
    """
    'dir': retorna diretorio da tabela ->
    'tab': retorna tabela
    """
    if argumento == 'tab':
        itens = LerConfig('itens')
        for i in range(len(itens)):
            if itens[i][0] == 'ultimo_schema':
                schema = itens[i][1]
                return schema
    elif argumento == 'dir':
        dir = LerConfig('dirtab')
        return dir

def getTabela():
    itens = LerConfig('itens')
    for i in range(len(itens)):
        if itens[i][0] == 'ultima_tabela':
            tabela = itens[i][1]
            return tabela

def editUser(usuario):
    CAMINHO_CONFIG = LerConfig('config')
    itens = LerConfig('itens')
    linhas = LerConfig('linhas')
    
    with open(CAMINHO_CONFIG, 'w', encoding='utf-8') as configuracoes:
        for i in range(len(itens)):
            if itens[i][0] == 'user':
                linhas[i] = 'user='+usuario+'\n'
                configuracoes.writelines(linhas)
                
def editSenha(senha):
    CAMINHO_CONFIG = LerConfig('config')
    itens = LerConfig('itens')
    linhas = LerConfig('linhas')
    
    with open(CAMINHO_CONFIG, 'w', encoding='utf-8') as configuracoes:
        for i in range(len(itens)):
            if itens[i][0] == 'senha':
                linhas[i] = 'senha='+senha+'\n'
                configuracoes.writelines(linhas)

def editSchema(schema):
    CAMINHO_CONFIG = LerConfig('config')
    itens = LerConfig('itens')
    linhas = LerConfig('linhas')
    
    with open(CAMINHO_CONFIG, 'w', encoding='utf-8') as configuracoes:
        for i in range(len(itens)):
            if itens[i][0] == 'schema_caminho':
                linhas[i] = 'schema_caminho='+schema+'\n'
                configuracoes.writelines(linhas)
                
def editTema(tema):
    CAMINHO_CONFIG = LerConfig('config')
    itens = LerConfig('itens')
    linhas = LerConfig('linhas')
    
    with open(CAMINHO_CONFIG, 'w', encoding='utf-8') as configuracoes:
        for i in range(len(itens)):
            if itens[i][0] == 'tema':
                linhas[i] = 'tema='+tema+'\n'
                configuracoes.writelines(linhas)
                
def editSecao(secao):
    CAMINHO_CONFIG = LerConfig('config')
    itens = LerConfig('itens')
    linhas = LerConfig('linhas')
    
    with open(CAMINHO_CONFIG, 'w', encoding='utf-8') as configuracoes:
        for i in range(len(itens)):
            if itens[i][0] == 'manter_logado':
                linhas[i] = 'manter_logado='+secao+'\n'
                configuracoes.writelines(linhas)
    
def getUser():
    itens = LerConfig('itens')
    for i in range(len(itens)):
        if itens[i][0] == 'user':
            usuario = itens[i][1]
            return usuario
        
def getSenha():
    itens = LerConfig('itens')
    for i in range(len(itens)):
        if itens[i][0] == 'senha':
            senha = itens[i][1]
            return senha

def getTema():
    itens = LerConfig('itens')
    for i in range(len(itens)):
        if itens[i][0] == 'tema':
            tema = itens[i][1]
            return tema

def getSecao():
    itens = LerConfig('itens')
    for i in range(len(itens)):
        if itens[i][0] == 'manter_logado':
            secao = itens[i][1]
            return secao

def apagar_dados():
    CAMINHO_CONFIG = LerConfig('config')
    itens = LerConfig('itens')
    linhas = LerConfig('linhas')
    
    with open(CAMINHO_CONFIG, 'w', encoding='utf-8') as configuracoes:
        for index, item in enumerate(itens):
            if item[0] == 'tema':
                item[1] = 'cyborg'
            elif item[1] == 'True' or item[1] == 'False':
                if item[0] == 'manter_logado':
                    item[1] = 'False'
                elif item[0] == 'autosave':
                    item[1] = 'False'
                elif item[0] == 'saved':
                    item[1] = 'True'
            else:
                item[1] = ''
            linhas[index] = f'{item[0]}={item[1]}\n'
        configuracoes.writelines(linhas)

def limpar_temp():
    CAMINHO_CONFIG = LerConfig('config')
    itens = LerConfig('itens')
    linhas = LerConfig('linhas')
    
    with open(CAMINHO_CONFIG, 'w', encoding='utf-8') as configuracoes:
        for i in range(len(itens)):
            if itens[i][0] == 'undo':
                linhas[i] = 'undo=\n'
            if itens[i][0] == 'redo':
                linhas[i] = 'redo=\n'
        configuracoes.writelines(linhas)
    padrao_txt = os.path.join(os.getcwd(),'data/users/sqlite_databases/backup/*.sql')
    arquivos_txt = glob.glob(padrao_txt)
    for arquivo in arquivos_txt:
        os.remove(arquivo)
   
def editarUndo(undo):
    CAMINHO_CONFIG = LerConfig('config')
    itens = LerConfig('itens')
    linhas = LerConfig('linhas')

    with open(CAMINHO_CONFIG, 'w', encoding='utf-8') as configuracoes:
        for i in range(len(itens)):
            if itens[i][0] == 'undo':
                linhas[i] = f'undo={undo}\n'
                configuracoes.writelines(linhas)

def getUndo():
    itens = LerConfig('itens')
    for i in range(len(itens)):
        if itens[i][0] == 'undo':
            undo = itens[i][1]
            return undo
        
def editarRedo(redo):
    CAMINHO_CONFIG = LerConfig('config')
    itens = LerConfig('itens')
    linhas = LerConfig('linhas')
    
    with open(CAMINHO_CONFIG, 'w', encoding='utf-8') as configuracoes:
        for i in range(len(itens)):
            if itens[i][0] == 'redo':
                linhas[i] = f'redo={redo}\n'
                configuracoes.writelines(linhas)

def getRedo():
    itens = LerConfig('itens')
    for i in range(len(itens)):
        if itens[i][0] == 'redo':
            redo = itens[i][1]
            return redo

def setIsSaved(saved: bool):
    CAMINHO_CONFIG = LerConfig('config')
    itens = LerConfig('itens')
    linhas = LerConfig('linhas')
    
    with open(CAMINHO_CONFIG, 'w', encoding='utf-8') as configuracoes:
        for i in range(len(itens)):
            if itens[i][0] == 'saved':
                linhas[i] = f'saved={saved}\n'
                configuracoes.writelines(linhas)
   
def getIsSaved() -> str:
    itens = LerConfig('itens')
    for i in range(len(itens)):
        if itens[i][0] == 'saved':
            saved = itens[i][1]
            return saved

def setAutoSave(auto_save: bool):
    CAMINHO_CONFIG = LerConfig('config')
    itens = LerConfig('itens')
    linhas = LerConfig('linhas')
    
    with open(CAMINHO_CONFIG, 'w', encoding='utf-8') as configuracoes:
        for i in range(len(itens)):
            if itens[i][0] == 'autosave':
                linhas[i] = f'autosave={auto_save}\n'
                configuracoes.writelines(linhas)

def getAutoSave() -> str: 
    itens = LerConfig('itens')
    for i in range(len(itens)):
        if itens[i][0] == 'autosave':
            auto_save = itens[i][1]
            return auto_save

def set_scale(scale: int) -> int:
    CAMINHO_CONFIG = LerConfig('config')
    itens = LerConfig('itens')
    linhas = LerConfig('linhas')

    with open(CAMINHO_CONFIG, 'w', encoding='utf-8') as configuracoes:
        for i in range(len(itens)):
            if itens[i][0] == 'escala':
                linhas[i] = f'escala={scale}\n'
                configuracoes.writelines(linhas)
                
def get_scale() -> float: 
    itens = LerConfig('itens')
    for i in range(len(itens)):
        if itens[i][0] == 'escala':
            try:
                scale = float(itens[i][1])
            except:
                return None
            else:
                return scale
        