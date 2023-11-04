from pandas import *
import numpy as np
import sqlite3
from data import edit_config

def sqlite_table():
    dir_schema = edit_config.getSchema('dir')
    tabela = edit_config.getTabela()
    with sqlite3.connect(dir_schema) as schema:
        cursor = schema.cursor()
        coluna_id = 'id'
        cursor.execute(f"PRAGMA table_info({tabela})")
        colunas_da_tabela = cursor.fetchall()
        nomes_de_colunas = [coluna[1] for coluna in colunas_da_tabela if coluna[1] != coluna_id]
        cursor.execute(f"SELECT {', '.join(nomes_de_colunas)} FROM {tabela}")
        matriz = cursor.fetchall()
    
    lista_medidas = []
    for i in range(len(matriz[0])):
        medidas_coluna = [dados[i] for dados in matriz if dados[i] is not None]
        lista_medidas.append(medidas_coluna)
    
    tupla_medidas = []
    for i in range(len(lista_medidas[0])):
        tupla = tuple([coluna[i] if i < len(coluna) else None for coluna in lista_medidas])
        tupla_medidas.append(tupla)

    colunas = []
    for coluna in range(len(matriz[0])):
        colunas.append(f'{coluna+1}ª')
        
    tabela_formatada = DataFrame(tupla_medidas, columns=colunas)
    
    return matriz, tabela_formatada

def imports():
    #TODO
    pass

def media(tabela):
    medidas = tabela()
    medidas = np.array(medidas)
    media = np.average(medidas)
    
    return media
    
def mediana(tabela):
    medidas = tabela()
    medidas.sort()
    medidas = np.array(medidas)
    mediana = np.median(medidas)
    
    return mediana

def max(tabela):
    medidas = tabela()
    medidas = np.array(medidas)
    max = np.max(medidas)
    
    return max

def min(tabela):
    medidas = tabela()
    medidas = np.array(medidas)
    min = np.min(medidas)
    
    return min

def amplitude(tabela):
    max = max(tabela)
    min = min(tabela)
    
    amp = max-min
    
    return amp

def primeiro_quartil(tabela):
    medidas = tabela()
    medidas.sort()
    medidas = np.array(medidas)
    fst_qrt = np.quantile(medidas, 0.25)
    
    return fst_qrt

def terceiro_quartil(tabela):
    medidas = tabela()
    medidas.sort()
    medidas = np.array(medidas)
    trd_qrt = np.quantile(medidas, 0.75)
    
    return trd_qrt

def iqr(tabela):
    fst_qrt = primeiro_quartil(tabela)
    trd_qrt = terceiro_quartil(tabela)
    
    iqr = trd_qrt - fst_qrt
    
    return iqr
    
def corte_superior(tabela):
    trd_qrt = terceiro_quartil(tabela)
    iqr = iqr(tabela)
    
    sup = trd_qrt + 1,5 * iqr
    
    return sup

def corte_inferior(tabela):
    fst_qrt = primeiro_quartil(tabela)
    iqr = iqr(tabela)
    
    inf = fst_qrt - 1,5 * iqr
    
    return inf

def dados_discrepantes(tabela):
    #TODO
    pass

def moda(tabela):
    medidas = tabela()
    medidas.sort()
    medidas = DataFrame(medidas)
    moda = medidas.mode()
    moda = moda.values
    
    return moda
