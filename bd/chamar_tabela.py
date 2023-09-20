# Só de teste, apagar este arquivo mais tarde

import os
import sys
CAMINHO_PROJETO = os.getcwd()
sys.path.insert(0, CAMINHO_PROJETO)
from tabela_sqlite import *
from data import edit_config

nome_bd = input('Digite o nome do banco: ')

tabela_sqlite = tabela(table=nome_bd)

criar_tabela = tabela_sqlite.CriarBD()
if criar_tabela == 'tabela_existe':
    print('Tabela já existe')
else:
    pass

while True:
    ocorrencia = input('Digite a ocorrencia ("wq" para sair): ')
    if ocorrencia == 'wq':
        break
    else:
        tabela_sqlite.addValor(ocorrencia)
edit_config.EditarTabela(nome_bd)