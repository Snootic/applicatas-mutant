from pandas import *
import numpy as np
import sqlite3
from data import edit_config

def sqlite_table():
    dir_schema = edit_config.getSchema('dir')
    tabela = edit_config.getTabela()
    with sqlite3.connect(dir_schema) as schema:
        cursor = schema.cursor()
        cursor.execute(f"SELECT medidas FROM {tabela}")
        medidas = cursor.fetchall()
        
    return medidas

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
