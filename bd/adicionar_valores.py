import sqlite3
from criar_diretorio_tabela import *

def adicionar_valor(*args): #Tabela, ocorrencias e custo (opcional)
    
    
    if len(args) == 3:
        tabela, ocorrencias, custo = args
        tabela = criar_diretorio_tabela(tabela)
        tabela = sqlite3.connect(tabela)
        cursor = tabela.cursor()
        cursor.execute("INSERT INTO tabela VALUES(?,?)", (ocorrencias, custo))
    
    elif len(args) == 2:
        tabela, ocorrencias = args
        tabela = criar_diretorio_tabela(tabela)
        tabela = sqlite3.connect(tabela)
        cursor = tabela.cursor()
        cursor.execute("INSERT INTO tabela (ocorrencias) VALUES(?)", (ocorrencias,))
    else:
        return 'argumentos_invalidos'

    tabela.commit()