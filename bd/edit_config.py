import os
from tabela_sqlite import *

#mudar caminho para app_config.txt

def ler_configuracao(nome_tabela):
    tabela1 = tabela()
    caminho_config = (os.path.abspath('app_config_debug.txt'))
    caminho_tabela = tabela1.criar_diretorio_tabela(nome_tabela)

    with open(caminho_config, 'r', encoding='utf-8') as configuracoes:
        linhas = configuracoes.readlines()
        itens = []
        for linha in linhas:
            itens.append(linha.replace(' ', '').strip().split('='))
            
    return caminho_config, caminho_tabela, itens, linhas


def editar_tabela(nome_tabela):
    nome_tabela = nome_tabela
    caminho_config, caminho_tabela, itens, linhas = ler_configuracao(nome_tabela)
    with open(caminho_config, 'w', encoding='utf-8') as configuracoes:
        for i in range(len(itens)):
            if itens[i][0] == 'ultima_tabela':
                linhas[i] = 'ultima_tabela = '+nome_tabela+'.db\n'
                
            if itens[i][0] == 'caminho_tabela':
                linhas[i] = 'caminho_tabela = '+caminho_tabela+'\n'
                
        configuracoes.writelines(linhas)