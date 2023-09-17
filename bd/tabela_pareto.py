import sqlite3

#TODO: funções para criar tabelas análise de PARETO
#Integrar funções na tela inicial

def criar_bd(nome_tabela):
    # global tabela, cursor
    tabela = sqlite3.connect(nome_tabela+'.db')
    cursor = tabela.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (nome_tabela,))
    tabela_existente = cursor.fetchone()
    if tabela_existente:
        return "tabela_existe"
    else:
        cursor.execute('''CREATE TABLE if not exists tabela(
        ocorrencias VARCHAR,
        custo REAL DEFAULT NULL)''')
        return f'{nome_tabela}'+".db"