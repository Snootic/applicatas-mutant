import os
import sys
caminho_projeto = os.getcwd()
sys.path.insert(0, caminho_projeto)
from bd.tabela_sqlite import *

#mudar caminho para app_config.txt

def ler_configuracao():
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


def editar_tabela(nome_tabela):
    tabela1 = tabela()
    caminho_tabela = tabela1.criar_diretorio_tabela(nome_tabela)
    caminho_config, itens, linhas, dir_tabela = ler_configuracao()

    with open(caminho_config, 'w', encoding='utf-8') as configuracoes:
        for i in range(len(itens)):
            if itens[i][0] == 'ultima_tabela':
                linhas[i] = 'ultima_tabela = '+nome_tabela+'.db\n'
                
            if itens[i][0] == 'tabela_caminho':
                linhas[i] = 'tabela_caminho = '+caminho_tabela+'\n'

        configuracoes.writelines(linhas)