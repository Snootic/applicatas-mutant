import sqlite3

#TODO: funções para criar tabelas análise de PARETO
#Integrar funções na tela inicial

def criar_bd(nome_tabela):
    global tabela, cursor
    adicionar = 0
    nome_tabela_original = nome_tabela
    while True:
        try:
            tabela = sqlite3.connect(nome_tabela+'.db')
            cursor = tabela.cursor()
            cursor.execute('''CREATE TABLE if not exists tabela(
                ocorrencias VARCHAR,
                custo REAL DEFAULT 0.00)''')
            break
        except sqlite3.OperationalError:
            adicionar += 1
            nome_tabela=(f'{nome_tabela_original}{adicionar}')
    
criar_bd("teste")


cursor.execute('''INSERT INTO tabela VALUES("Teorias, DEFAULT")''')

tabela.commit()
