import sqlite3
from criar_diretorio_tabela import *

#TODO: funções para criar tabelas análise de PARETO
#Integrar funções na tela inicial

def criar_bd(nome_tabela):
    caminho_bd = criar_diretorio_tabela(nome_tabela)
    
    tabela_existente = os.path.exists(caminho_bd)

    tabela = sqlite3.connect(caminho_bd)
    cursor = tabela.cursor()
    
    if tabela_existente:
        return "tabela_existe"
    else:
        cursor.execute('''CREATE TABLE if not exists tabela(
        ocorrencias VARCHAR,
        custo REAL DEFAULT NULL)''')
        return f'{nome_tabela}'+".db"