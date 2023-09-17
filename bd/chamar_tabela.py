# Só de teste, apagar este arquivo mais tarde

import os
import sqlite_tabela as tabela
import adicionar_valores
from criar_diretorio_tabela import *

nome_bd = input('Digite o nome do banco: ')

criar_tabela = tabela.criar_bd(nome_bd)
if criar_tabela == 'tabela_existe':
    print('Tabela já existe')
else:
    pass

ocorrencia = input('Digite a ocorrencia: ')
numero_ocorrencias = int(input('Digite a quantidade da ocorrencia: '))

for i in range(numero_ocorrencias):
    adicionar_valores.adicionar_valor(nome_bd, ocorrencia)


#mudar caminho para app_config.txt
caminho_config = (os.path.abspath('app_config_debug.txt'))
caminho_tabela = criar_diretorio_tabela(nome_bd)

with open(caminho_config, 'r', encoding='utf-8') as configuracoes:
    linhas = configuracoes.readlines()
    itens = []
    for linha in linhas:
        itens.append(linha.replace(' ', '').strip().split('='))
        
with open(caminho_config, 'w', encoding='utf-8') as configuracoes:
    for i in range(len(itens)):
        if itens[i][0] == 'ultima_tabela':
            linhas[i] = 'ultima_tabela = '+nome_bd+'.db\n'
            
        if itens[i][0] == 'caminho_tabela':
            linhas[i] = 'caminho_tabela = '+caminho_tabela+'\n'
            
    configuracoes.writelines(linhas)
    