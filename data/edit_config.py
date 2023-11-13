import glob
from bd.sqlite import *
import platform

def LerConfig(argumento):
    """
    'config': retorna caminho absoluto das configurações ->
    'itens': retorna lista das variaveis das configurações ->
    'linhas': retorna as configurações brutas ->
    'dirtab': retorna diretorio da schema mais recente ->
    """
    CAMINHO_CONFIG = (os.path.abspath('data/app_config.txt'))
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
        for i in range(len(itens)):
            if itens[i][0] == 'user':
                linhas[i] = 'user='+'\n'
            if itens[i][0] == 'senha':
                linhas[i] = 'senha='+'\n'
            if itens[i][0] == 'ultimo_schema':
                linhas[i] = 'ultimo_schema='+'\n'
            if itens[i][0] == 'ultima_tabela':
                linhas[i] = 'ultima_tabela='+'\n'
            if itens[i][0] == 'schema_caminho':
                linhas[i] = 'schema_caminho='+'\n'
            if itens[i][0] == 'manter_logado':
                linhas[i] = 'manter_logado=False'+'\n'
            if itens[i][0] == 'undo':
                linhas[i] = 'undo=\n'
            if itens[i][0] == 'redo':
                linhas[i] = 'redo=\n'
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
    if platform.system() == 'Windows':
        padrao_txt = os.path.join(os.getcwd(),'data\\users\\sqlite_databases\\backup\\*.sql')
    else:
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