# Só de teste, apagar este arquivo mais tarde

import os
from tabela_sqlite import *
from edit_config import *

nome_bd = input('Digite o nome do banco: ')

tabela_sqlite = tabela()

criar_tabela = tabela_sqlite.criar_bd(nome_bd)
if criar_tabela == 'tabela_existe':
    print('Tabela já existe')
else:
    pass

ocorrencia = input('Digite a ocorrencia: ')
numero_ocorrencias = int(input('Digite a quantidade da ocorrencia: '))

for i in range(numero_ocorrencias):
    tabela_sqlite.adicionar_valor(nome_bd, ocorrencia)
    
editar_tabela(nome_bd)