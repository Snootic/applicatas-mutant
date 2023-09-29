# import os
# import sys
# CAMINHO_PROJETO = os.getcwd()
# sys.path.insert(0, CAMINHO_PROJETO)
from bd.tabela_sqlite import *

#mudar caminho para app_config.txt

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
            itens.append(linha.replace(' ', '').strip().split('='))

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


def EditarTabela(table):
    tabela1 = tabela()
    user = getUser()
    CAMINHO_SCHEMA = tabela1.CriarDirSchema()
    CAMINHO_CONFIG = LerConfig('config')
    itens = LerConfig('itens')
    linhas = LerConfig('linhas')

    with open(CAMINHO_CONFIG, 'w', encoding='utf-8') as configuracoes:
        for i in range(len(itens)):
            if itens[i][0] == 'ultimo_schema':
                linhas[i] = 'ultimo_schema = '+f'{user}'+'.db\n'
                
            if itens[i][0] == 'schema_caminho':
                linhas[i] = 'schema_caminho = '+f'{CAMINHO_SCHEMA}'+'\n'
                
            if itens[i][0] == 'ultima_tabela':
                linhas[i] = 'ultima_tabela = '+f'{table}'+'\n'

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
                linhas[i] = 'user = '+usuario+'\n'
                configuracoes.writelines(linhas)
                
def editSenha(senha):
    CAMINHO_CONFIG = LerConfig('config')
    itens = LerConfig('itens')
    linhas = LerConfig('linhas')
    
    with open(CAMINHO_CONFIG, 'w', encoding='utf-8') as configuracoes:
        for i in range(len(itens)):
            if itens[i][0] == 'senha':
                linhas[i] = 'senha = '+senha+'\n'
                configuracoes.writelines(linhas)

def editSchema(schema):
    CAMINHO_CONFIG = LerConfig('config')
    itens = LerConfig('itens')
    linhas = LerConfig('linhas')
    
    with open(CAMINHO_CONFIG, 'w', encoding='utf-8') as configuracoes:
        for i in range(len(itens)):
            if itens[i][0] == 'schema_caminho':
                linhas[i] = 'schema_caminho = '+schema+'\n'
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
    