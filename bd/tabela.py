import sqlite3

#TODO: funções para criar tabelas análise de PARETO
#Integrar funções na tela inicial

def criar_bd(nome_tabela):
    global tabela 
    tabela = sqlite3.connect(nome_tabela)
    
criar_bd("teste")

cursor = tabela.cursor()

cursor.execute("CREATE TABLE")