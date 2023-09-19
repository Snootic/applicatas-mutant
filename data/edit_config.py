import os
import sys
CAMINHO_PROJETO = os.getcwd()
sys.path.insert(0, CAMINHO_PROJETO)
from bd.tabela_sqlite import *

#mudar caminho para app_config.txt

def LerConfig(argumento):
    """
    'config': retorna caminho absoluto das configurações ->
    'itens': retorna lista das variaveis das configurações ->
    'linhas': retorna as configurações brutas ->
    'dirtab': retorna diretorio da tabela mais recente ->
    """
    CAMINHO_CONFIG = (os.path.abspath('data/app_config_debug.txt'))

    with open(CAMINHO_CONFIG, 'r', encoding='utf-8') as configuracoes:
        linhas = configuracoes.readlines()
        itens = []
        for linha in linhas:
            itens.append(linha.replace(' ', '').strip().split('='))

        dir_tabela = ''
        for i in range(len(itens)):
            if os.path.exists(itens[i][1]):
                dir_tabela = itens[i][1]
                
    if argumento == 'config':
        return CAMINHO_CONFIG
    elif argumento == 'itens':
        return itens
    elif argumento == 'linhas':
        return linhas
    elif argumento == 'dirtab':
        return dir_tabela


def EditarTabela(nome_tabela):
    tabela1 = tabela()
    CAMINHO_TABELA = tabela1.CriarDirTabela(nome_tabela)
    CAMINHO_CONFIG = LerConfig('config')
    itens = LerConfig('itens')
    linhas = LerConfig('linhas')

    with open(CAMINHO_CONFIG, 'w', encoding='utf-8') as configuracoes:
        for i in range(len(itens)):
            if itens[i][0] == 'ultima_tabela':
                linhas[i] = 'ultima_tabela = '+nome_tabela+'.db\n'
                
            if itens[i][0] == 'tabela_caminho':
                linhas[i] = 'tabela_caminho = '+CAMINHO_TABELA+'\n'

        configuracoes.writelines(linhas)
    
def getTabela(argumento):
    """
    'dir': retorna diretorio da tabela ->
    'tab': retorna tabela
    """
    if argumento == 'tab':
        itens = LerConfig('itens')
        for i in range(len(itens)):
            if itens[i][0] == 'ultima_tabela':
                table = itens[i][1]
                return table
    elif argumento == 'dir':
        dir = LerConfig('dirtab')
        return dir

def editUser(usuario):
    CAMINHO_CONFIG = LerConfig('config')
    itens = LerConfig('itens')
    linhas = LerConfig('linhas')
    
    with open(CAMINHO_CONFIG, 'w', encoding='utf-8') as configuracoes:
        for i in range(len(itens)):
            if itens[i][0] == 'user':
                linhas[i] = 'user = '+usuario+'\n'
                
def getUser():
    itens = LerConfig('itens')
    for i in range(len(itens)):
        if itens[i][0] == 'user':
            usuario = itens[i][1]
            return usuario

def getTema():
    itens = LerConfig('itens')
    for i in range(len(itens)):
        if itens[i][0] == 'tema':
            tema = itens[i][1]
            return tema
    