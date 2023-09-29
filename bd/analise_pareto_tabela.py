import sqlite3
from pandas import *
from data import edit_config #ler_configuracao

#TODO: melhorar a semantica do sqlite + estudar uma forma mais otimizada de executar o código
# Importar CSV/TXT e XSLS para análise de pareto


class pareto:

    def sqlite(self):
        '''Cria uma tabela de pareto com dados inseridos num Banco de dados
        
        Returns:
            pareto_sql: Pandas DataFrame conténdo a tabela
        '''
        dir_schema = edit_config.getSchema('dir')
        tabela = edit_config.getTabela()

        schema = sqlite3.connect(dir_schema)
        cursor = schema.cursor()

        cursor.execute(f'SELECT COUNT(ocorrencias) FROM {tabela}')
        if cursor.fetchall()[0][0] == 0:
            pareto_sql = DataFrame(columns=['Ocorrências','No. Ocorrências', 'Freq. Relativa','Freq. Acumulada'])
            return pareto_sql
        else:
            cursor.execute(f'SELECT COUNT(*) FROM {tabela} WHERE custo IS NULL')
            if cursor.fetchall()[0][0] > 0:
                cursor.execute(f'SELECT COUNT(ocorrencias) FROM {tabela} GROUP BY ocorrencias')
                numero_ocorrencias = cursor.fetchall()
                
                cursor.execute(f'SELECT ocorrencias FROM {tabela} group BY ocorrencias')
                ocorrencias = cursor.fetchall()
                
                cursor.execute(f'SELECT COUNT(ocorrencias) FROM {tabela}')
                total_ocorrencias = cursor.fetchall()[0][0]
                
                ocorrencias = [item[0] for item in ocorrencias]
                numero_ocorrencias = [item[0] for item in numero_ocorrencias]
                
                items = list(zip(ocorrencias,numero_ocorrencias))
                
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
                    
                pareto_sql = DataFrame(items_ordenados, columns=['Ocorrências','No. Ocorrências', 'Freq. Relativa','Freq. Acumulada'])
                return pareto_sql
            else:
                pass
            
    def csv():
        pass

    def xsls():
        pass
