from pandas import *
import numpy as np
import sqlite3, asyncio
from data import edit_config
from bd import sqlite


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
    
    if len(matriz) == 0:
        return matriz, None
    
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

async def imports(dados, tipo='', nome=''):
    if tipo == 'csv':
        tabela = read_csv(dados,sep=',')
    else:
        tabela = read_excel(dados)
    
    nome = nome.split('.')[0]
    temp = 1
    nome = f'{nome}_temp{temp}'
    sql = sqlite.tabela()
    tabelas = sql.getTabelas('medidas')
    while temp != 0:
        if nome not in tabelas:
            sql.tabela = nome
            break
        else:
            temp += 1
                
    sql.CriarBD('medidas')
    dados = tabela.to_numpy().tolist()
    for dado in dados:
        sql.add_valor_medidas(dado[0])
    
    return tabela

async def media(tabela):
    matriz,medidas = tabela()
    medidas_totais = np.array(medidas)
    media = np.average(medidas_totais)

    lista_medidas = [media]
    for i in medidas:
        coluna = medidas[i].to_list()
        coluna = np.array(coluna)
        media_coluna = np.average(coluna)
        lista_medidas.append(media_coluna)
        
    return lista_medidas
    
async def mediana(tabela):
    matriz,medidas = tabela()
    medidas_totais = np.array(medidas)
    mediana = np.median(medidas_totais)
    
    lista_medidas = [mediana]
    for i in medidas:
        coluna = medidas[i].to_list()
        coluna = np.array(coluna)
        mediana_coluna = np.median(coluna)
        lista_medidas.append(mediana_coluna)
        
    return lista_medidas

async def max(tabela):
    matriz,medidas = tabela()
    medidas_totais = np.array(medidas)
    max = np.max(medidas_totais)
    
    lista_medidas = [max]
    for i in medidas:
        coluna = medidas[i].to_list()
        coluna = np.array(coluna)
        max_coluna = np.max(coluna)
        lista_medidas.append(max_coluna)
        
    return lista_medidas

async def min(tabela):
    matriz,medidas = tabela()
    medidas_totais = np.array(medidas)
    min = np.min(medidas_totais)
    
    lista_medidas = [min]
    for i in medidas:
        coluna = medidas[i].to_list()
        coluna = np.array(coluna)
        min_coluna = np.min(coluna)
        lista_medidas.append(min_coluna)
        
    return lista_medidas

async def amplitude(tabela):
    maximo = await max(tabela)
    minimo = await min(tabela)
    
    lista_medidas = []
    for i in range(len(maximo)):
        maximo_conjunto = maximo[i]
        minimo_conjunto= minimo[i]
        amp_conjunto = maximo_conjunto - minimo_conjunto
        lista_medidas.append(amp_conjunto)
        
    return lista_medidas

async def primeiro_quartil(tabela):
    matriz,medidas = tabela()
    medidas_totais = np.array(medidas)
    fst_qrt = np.quantile(medidas_totais, 0.25)
    
    lista_medidas = [fst_qrt]
    for i in medidas:
        coluna = medidas[i].to_list()
        coluna = np.array(coluna)
        fst_qrt_coluna = np.quantile(coluna, 0.25)
        lista_medidas.append(fst_qrt_coluna)
        
    return lista_medidas

async def terceiro_quartil(tabela):
    matriz,medidas = tabela()
    medidas_totais = np.array(medidas)
    trd_qrt = np.quantile(medidas_totais, 0.75)
    
    lista_medidas = [trd_qrt]
    for i in medidas:
        coluna = medidas[i].to_list()
        coluna = np.array(coluna)
        trd_qrt_coluna = np.quantile(coluna, 0.75)
        lista_medidas.append(trd_qrt_coluna)
        
    return lista_medidas

async def iqr(tabela):
    fst_qrt = await primeiro_quartil(tabela)
    trd_qrt = await terceiro_quartil(tabela)
    
    lista_medidas = []
    for i in range(len(trd_qrt)):
        trd_qrt_conjunto = trd_qrt[i]
        fst_qrt_conjunto = fst_qrt[i]
        iqr = trd_qrt_conjunto - fst_qrt_conjunto
        lista_medidas.append(iqr)
        
    return lista_medidas
    
async def corte_superior(tabela):
    trd_qrt = await terceiro_quartil(tabela)
    iqr_valores = await iqr(tabela)
    
    lista_medidas = []
    for i in range(len(trd_qrt)):
        trd_qrt_conjunto = trd_qrt[i]
        iqr_valores_conjunto = iqr_valores[i]
        inf = trd_qrt_conjunto + 1.5 * iqr_valores_conjunto
        lista_medidas.append(inf)

    return lista_medidas
    
async def corte_inferior(tabela):
    fst_qrt = await primeiro_quartil(tabela)
    iqr_valores = await iqr(tabela)

    lista_medidas = []
    for i in range(len(fst_qrt)):
        fst_qrt_conjunto = fst_qrt[i]
        iqr_valores_conjunto = iqr_valores[i]
        inf = fst_qrt_conjunto - 1.5 * iqr_valores_conjunto
        lista_medidas.append(inf)
        
    return lista_medidas

async def dados_discrepantes(tabela):
    #TODO
    pass

async def moda(tabela):
    matriz,medidas = tabela()
    medidas_totais = medidas.values.flatten()
    moda = Series(medidas_totais).mode().values
    
    lista_medidas = [moda]
    for i in medidas:
        coluna = medidas[i]
        moda_coluna = coluna.mode().values
        lista_medidas.append(moda_coluna)
        
    return lista_medidas

async def tdf(tabela):
    matriz, dataframe = tabela()
    amp = await amplitude(tabela)
    
    # calcula quantidade de linhas e colunas do dataframe
    qtd_linhas_dataframe = len(dataframe['1ª'])
    colunas_dataframe = dataframe.to_numpy().tolist()
    qtd_colunas_dataframe = len(colunas_dataframe[0])
    
    if qtd_colunas_dataframe*qtd_linhas_dataframe > 100:
    
        # Calcula o Intervalo de Classe pelo método de Sturges
        linhas_classe =  1+3.33*np.log10(qtd_colunas_dataframe*qtd_linhas_dataframe)
        tamanho_classe = amp[0]/linhas_classe
    else:
        # Calcula o Intervalo de Classe pelo Critério Raiz
        linhas_classe = np.sqrt(qtd_colunas_dataframe*qtd_linhas_dataframe)
        tamanho_classe = amp[0]/linhas_classe
    
    # Arredonda a quantidade de linhas
    linhas_classe = round(linhas_classe)
    
    # Arredonda o tamanho das classes
    try:
        tamanho_classe= round(tamanho_classe)
    except:
        pass
    
    # tabela de distribuição de frequência
    nova_matriz = []
    for i in range(len(colunas_dataframe)):
        for x in range(len(colunas_dataframe[0])):
            nova_matriz.append(colunas_dataframe[i][x])
            
    nova_matriz = sorted(nova_matriz)
    
    dado_inicial = nova_matriz[0]
    dado_limite = dado_inicial
    dados = []
    while dado_limite < nova_matriz[-1]: # Define os dados da TDF
        dado_limite += tamanho_classe
        ponto_medio = (dado_inicial+dado_limite)/2
        
        fi = 0
        for i in nova_matriz:
            if i in range(dado_inicial, dado_limite):
                fi += 1
        
        if dado_limite > nova_matriz[-1]:
            dados.append((f'{dado_inicial}|--|{dado_limite}',ponto_medio, fi))
        else:
            dados.append((f'{dado_inicial}|--{dado_limite}',ponto_medio, fi))
        dado_inicial = dado_limite
    
    tdf = DataFrame(dados, columns=['', 'Ponto Médio', 'Fi'])
    tdf['Freq. Relativa'] = tdf['Fi'] / tdf['Fi'].sum()
    tdf['Freq. Relativa %'] = tdf['Fi'] / tdf['Fi'].sum() * 100
    tdf['Freq. Acumulada'] = tdf['Freq. Relativa'].cumsum()/tdf['Freq. Relativa'].sum() * 100
    
    matplot = tdf[:].copy()
    
    total_fi = tdf['Fi'].sum()
    total_fr = tdf['Freq. Relativa'].sum()
    total_frp = tdf['Freq. Relativa %'].sum()
    
    # matplot.loc[-1] = ['Totais', np.nan, np.nan, np.nan, np.nan, 0]
    
    tdf["Freq. Relativa"] = tdf["Freq. Relativa"].round(2).apply(lambda x: f"{x:.2f}")
    tdf["Freq. Relativa %"] = tdf["Freq. Relativa %"].round(2).apply(lambda x: f"{x:.2f}%")
    tdf["Freq. Acumulada"] = tdf["Freq. Acumulada"].round(2).apply(lambda x: f"{x:.2f}%")
    tdf.loc[-1] = ['Totais', '-',total_fi, total_fr,f'{total_frp:.2f}%', '-']
    
    return tdf, matplot