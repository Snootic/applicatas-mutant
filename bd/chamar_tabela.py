# Só de teste, apagar este arquivo mais tarde

import os
import sys
caminho_projeto = os.getcwd()
sys.path.insert(0, caminho_projeto)
from tabela_sqlite import *
from data.edit_config import *

nome_bd = input('Digite o nome do banco: ')

tabela_sqlite = tabela()

criar_tabela = tabela_sqlite.criar_bd(nome_bd)
if criar_tabela == 'tabela_existe':
    print('Tabela já existe')
else:
    pass

while True:
    ocorrencia = input('Digite a ocorrencia ("wq" para sair): ')
    if ocorrencia == 'wq':
        break
    else:
        tabela_sqlite.adicionar_valor(nome_bd, ocorrencia)
editar_tabela(nome_bd)