import sqlite3
from pandas import *
import os
import sys
caminho_projeto = os.getcwd()
sys.path.insert(0, caminho_projeto)
from data.edit_config import * #ler_configuracao

#TODO: melhorar a semantica do sqlite + estudar uma forma mais otimizada de executar o código
# Importar CSV/TXT e XSLS para análise de pareto


class pareto:

    def sqlite(*args):
        caminho_config, itens, linhas, dir_tabela = ler_configuracao()
        
        tabela = sqlite3.connect(dir_tabela)
        cursor = tabela.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM tabela WHERE custo IS NULL')
        if cursor.fetchall()[0][0] > 0:
            cursor.execute('SELECT COUNT(ocorrencias) FROM tabela GROUP BY ocorrencias')
            numero_ocorrencias = cursor.fetchall()
            
            cursor.execute('SELECT ocorrencias FROM tabela group BY ocorrencias')
            ocorrencias = cursor.fetchall()
            
            cursor.execute('SELECT COUNT(ocorrencias) FROM TABELA')
            total_ocorrencias = cursor.fetchall()[0][0]
            print(total_ocorrencias)
            
            ocorrencias = [item[0] for item in ocorrencias]
            numero_ocorrencias = [item[0] for item in numero_ocorrencias]
            
            ocorrencias_ordenadas = {'Ocorrências': ocorrencias, 'Número Ocorrências': numero_ocorrencias}
            items = list(zip(ocorrencias_ordenadas['Ocorrências'], ocorrencias_ordenadas['Número Ocorrências']))
            
            items_ordenados = sorted(items, key=lambda item_maior: item_maior[1], reverse=True)
            items_ordenados.append(('Total',total_ocorrencias))
            
            for i in range(len(items_ordenados)):
                frequencia_relativa = items_ordenados[i][1] / items_ordenados[-1][1]
                frequencia_relativa *= 100
                if i == 0:
                    frequencia_acumulada = frequencia_relativa
                    items_ordenados[i] += (frequencia_relativa, frequencia_acumulada)
                    
                elif items_ordenados[i] != items_ordenados[-1]:
                    frequencia_acumulada = items_ordenados[i-1][3] + frequencia_relativa
                    items_ordenados[i] += (frequencia_relativa, frequencia_acumulada)
                    
                else:
                    items_ordenados[i] += (frequencia_relativa, '-')
                
            pareto_tabela = DataFrame(items_ordenados, columns=['Ocorrências','No. Ocorrências', 'Freq. Relativa','Freq. Acumulada'])
            print(pareto_tabela)
        else:
            pass
        
    def csv():
        pass

    def xsls():
        pass
    
tabel_sqlite = pareto()

tabel_sqlite.sqlite()