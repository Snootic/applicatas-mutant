import sqlite3
from pandas import *
from data import edit_config
import numpy as np

#TODO: estudar uma forma mais otimizada de executar o código
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
        self.cursor = schema.cursor()
        
        def mainFunc(tabela):
            self.cursor.execute(f'SELECT COUNT(ocorrencias) FROM {tabela}')
            if self.cursor.fetchall()[0][0] == 0: # se a tabela estiver completamente vazia ele retorna este dataframe
                pareto_sql = DataFrame(columns=['Ocorrências','No. Ocorrências', 'Freq. Relativa','Freq. Acumulada'])
                pareto_tkinter = DataFrame(columns=['Ocorrências','No. Ocorrências', 'Freq. Relativa','Freq. Acumulada'])
                return pareto_sql, pareto_tkinter
            
            else:
                self.cursor.execute(f'SELECT COUNT(*) FROM {tabela} WHERE custo IS NULL')
                if self.cursor.fetchall()[0][0] > 0: # se na tabela houver custo com valor padrao (NULL)
                    self.cursor.execute(f'SELECT COUNT(ocorrencias) FROM {tabela} GROUP BY ocorrencias')
                    numero_ocorrencias = self.cursor.fetchall()
                    
                    self.cursor.execute(f'SELECT ocorrencias FROM {tabela} group BY ocorrencias')
                    ocorrencias = self.cursor.fetchall()
                    
                    self.cursor.execute(f'SELECT COUNT(ocorrencias) FROM {tabela}')
                    total_ocorrencias = self.cursor.fetchall()[0][0]
                    
                    ocorrencias = [item[0] for item in ocorrencias]
                    numero_ocorrencias = [item[0] for item in numero_ocorrencias]
                    
                    items = list(zip(ocorrencias,numero_ocorrencias))
                    
                    items_ordenados = sorted(items, key=lambda item_maior: item_maior[1], reverse=True)
                    items_ordenados.append(('Total',total_ocorrencias))
                    
                    itens_tableview = items_ordenados[:]
                    
                    for i in range(len(items_ordenados)):
                        frequencia_relativa = items_ordenados[i][1] / items_ordenados[-1][1]
                        frequencia_relativa *= 100
                        if i == 0:
                            frequencia_acumulada = frequencia_relativa
                            items_ordenados[i] += (frequencia_relativa, frequencia_acumulada)
                            itens_tableview[i] += (f'{frequencia_relativa:.2f}%', f'{frequencia_acumulada:.2f}%')
                            
                        elif items_ordenados[i] != items_ordenados[-1]:
                            frequencia_acumulada = items_ordenados[i-1][3] + frequencia_relativa
                            if frequencia_acumulada > 99.99:
                                items_ordenados[i] += (frequencia_relativa, frequencia_acumulada)
                                itens_tableview[i] += (f'{frequencia_relativa:.2f}%', f'{frequencia_acumulada:.2f}%')
                            else:
                                items_ordenados[i] += (frequencia_relativa, frequencia_acumulada)
                                itens_tableview[i] += (f'{frequencia_relativa:.2f}%', f'{frequencia_acumulada:.2f}%')
                            
                        else:
                            # items_ordenados[i] += (frequencia_relativa,)
                            itens_tableview[i] += (f'{frequencia_relativa:.2f}%', '-')
                        
                    pareto_sql = DataFrame(items_ordenados, columns=['Ocorrências','No. Ocorrências', 'Freq. Relativa','Freq. Acumulada'])
                    pareto_tkinter = DataFrame(itens_tableview, columns=['Ocorrências','No. Ocorrências', 'Freq. Relativa','Freq. Acumulada'])
                    return pareto_sql, pareto_tkinter
                else:
                # para tabelas com custo definido (NOT-NULL)
                    matplot = ''
                    self.cursor.execute(f'SELECT ocorrencias FROM {tabela}')
                    ocorrencias = self.cursor.fetchall()
                    
                    self.cursor.execute(f'SELECT custo FROM {tabela}')
                    custos = self.cursor.fetchall()
                    
                    ocorrencias = [i[0] for i in ocorrencias]
                    custos = [i[0] for i in custos]
                    
                    items = list(zip(ocorrencias,custos))
                    
                    tabela = DataFrame(items,columns=['Ocorrências','Custo Un.'])
                
                    tabela['No. Ocorrências'] = tabela.groupby('Ocorrências')['Ocorrências'].transform('count')
                    tabela.drop_duplicates(subset='Ocorrências', keep='first', inplace=True)
                    
                    tabela['Custo Total'] = tabela['Custo Un.'] * tabela['No. Ocorrências']
                    
                    tabela = tabela.sort_values(by=['Custo Total'],ascending=False)
                    
                    tabela['Freq. Relativa'] = tabela['Custo Total'] / tabela['Custo Total'].sum() * 100
                    
                    tabela['Freq. Acumulada'] = tabela['Freq. Relativa'].cumsum()/tabela['Freq. Relativa'].sum() * 100
                    
                    matplot = tabela[:].copy()
                    
                    total_ocorrencias = tabela['No. Ocorrências'].sum()
                    total_custos_unitarios = tabela['Custo Un.'].sum()
                    total_custos = tabela['Custo Total'].sum()
                    matplot.loc[-1] = ['Total', total_ocorrencias, total_custos_unitarios, np.nan, np.nan, np.nan]
                    
                    tabela["Freq. Acumulada"] = to_numeric(tabela["Freq. Acumulada"], errors='coerce')
                    tabela["Freq. Relativa"] = tabela["Freq. Relativa"].round(2).apply(lambda x: f"{x:.2f}%")
                    tabela["Freq. Acumulada"] = tabela["Freq. Acumulada"].round(2).apply(lambda x: f"{x:.2f}%")
                    tabela.loc[-1] = ['Total', f'R${total_custos_unitarios}', total_ocorrencias, f'R${total_custos}', '100.00%', '-']
                    return matplot, tabela
        try:
            self.cursor.execute(f'SELECT * FROM {tabela}')
        except sqlite3.OperationalError:
            pass
        else:
            return mainFunc(tabela)
            
    def imports(self, arquivo, tipo):
        if tipo == 'csv':
            tabela = read_csv(arquivo)
        else:
            tabela = read_excel(arquivo)
        matplot = ''
        if len(tabela.columns) > 2:
            matplot = tabela[:]
            matplot = matplot.iloc[:-1]
            matplot = matplot.applymap(lambda x: x.replace('%', '') if isinstance(x, str) else x)
            matplot.iloc[:,-1] = to_numeric(matplot.iloc[:,-1], errors='coerce')
            matplot.iloc[:,-2] = to_numeric(matplot.iloc[:,-2], errors='coerce')
            matplot.iloc[:,-3] = to_numeric(matplot.iloc[:,-3], errors='coerce')
            
        elif len(tabela.columns) == 2:
            pass
        else:
            tabela['No. Ocorrências'] = tabela.groupby('Ocorrências')['Ocorrências'].transform('count')
            tabela.drop_duplicates(subset='Ocorrências', keep='first', inplace=True)
            
            tabela = tabela.sort_values(by=['No. Ocorrências'],ascending=False)
            
            tabela['Freq. Relativa'] = tabela['No. Ocorrências'] / tabela['No. Ocorrências'].sum() * 100
            
            tabela['Freq. Acumulada'] = tabela['Freq. Relativa'].cumsum()/tabela['Freq. Relativa'].sum() * 100
            
            matplot = tabela[:].copy()
            
            total = tabela['No. Ocorrências'].sum()
            matplot.loc[-1] = ['Total', total, np.nan, np.nan]
            
            tabela["Freq. Relativa"] = tabela["Freq. Relativa"].round(2).apply(lambda x: f"{x:.2f}%")
            tabela["Freq. Acumulada"] = tabela["Freq. Acumulada"].round(2).apply(lambda x: f"{x:.2f}%")
            tabela.loc[-1] = ['Total', total, '100.00%', '-']
        
        return matplot, tabela
    