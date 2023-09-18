import os
import sys
CAMINHO_PROJETO = os.getcwd()
sys.path.insert(0, CAMINHO_PROJETO)
from bd.tabela_sqlite import *

#mudar caminho para app_config.txt

def LerConfig():
    caminho_config = (os.path.abspath('data/app_config_debug.txt'))

    with open(caminho_config, 'r', encoding='utf-8') as configuracoes:
        linhas = configuracoes.readlines()
        itens = []
        for linha in linhas:
            itens.append(linha.replace(' ', '').strip().split('='))

        dir_tabela = ''
        for i in range(len(itens)):
            if os.path.exists(itens[i][1]):
                dir_tabela = itens[i][1]
        
    return caminho_config, itens, linhas, dir_tabela


def EditarTabela(nome_tabela):
    tabela1 = tabela()
    CAMINHO_TABELA = tabela1.CriarDirTabela(nome_tabela)
    caminho_config, itens, linhas, dir_tabela = LerConfig()

    with open(caminho_config, 'w', encoding='utf-8') as configuracoes:
        for i in range(len(itens)):
            if itens[i][0] == 'ultima_tabela':
                linhas[i] = 'ultima_tabela = '+nome_tabela+'.db\n'
                
            if itens[i][0] == 'tabela_caminho':
                linhas[i] = 'tabela_caminho = '+CAMINHO_TABELA+'\n'

        configuracoes.writelines(linhas)
        
    def getUser():
        