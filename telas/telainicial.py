from telas import app
from tkinter import *
import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import *
from bd.tabela_pareto import *
from bd.sqlite import tabela
import matplotlib.pyplot as plt
from bd.medidas import *
from data.edit_config import EditarTabela
import asyncio
from functools import partial

class inicio:
    def __init__(self, login, estilo):
        self.login = login
        self.home = ttk.Toplevel()
        self.app = app.Tela(self.home, 'Peraeque - Início')
        self.app.centralizarTela(900, 600)
        self.app.menu()
        self.app.instancia_com_tabela = self
        self.app.aba_atual = 0
        self.app.home = self.home
        self.aba = 0
        
        self.width = self.home.winfo_screenwidth()
        self.height = self.home.winfo_screenheight()
        
        #Estilo da tela
        colors = self.login.style.colors
        self.estilo = estilo
        
        #notebook
        self.notebook = ttk.Notebook(self.home, style='custom2.TNotebook')
        self.notebook.pack(expand=True)
        
        self.tela_pareto = ttk.Frame(self.notebook, width=self.width, height=self.height,style='custom2.TFrame')
        self.tela_pareto.pack(fill='both', expand=True)
        self.tela_medidas = ttk.Frame(self.notebook, width=self.width, height=self.height,style='custom2.TFrame')
        self.tela_medidas.pack(fill='both',expand=True)
        self.tela_binomial = ttk.Frame(self.notebook, width=self.width, height=self.height,style='custom2.TFrame')
        self.tela_binomial.pack(fill='both', expand=True)
        
        self.notebook.add(self.tela_pareto, text='Pareto')
        self.notebook.add(self.tela_medidas, text='Medidas')
        self.notebook.add(self.tela_binomial, text='Binomial')
        
        self.notebook.bind('<ButtonRelease-1>', lambda event: self.aba_atual())
        
        self.home.protocol("WM_DELETE_WINDOW", self.fechar_login)
        
        self.pareto = self.telas_pareto(self.tela_pareto)
        self.medida = self.telas_medidas(self.tela_medidas)
        # self.binomial = self.telas_binomiais(self.tela_binomial)
        
        self.data_pareto: DataFrame
        self.data_medidas: DataFrame
        self.tabela_pareto: str
        self.tabela_medidas: str
        
        self.home.mainloop()
   
    def telas_pareto(self, tela):
        ep = Esqueleto(tela, 'pareto', self.app, self)
        tabelas = tabela()
        sqlite = pareto()
        
        ep.abrir_tabela['value'] = tabelas.getTabelas('pareto')
        # Tabela da análise de pareto
        def tabela_analise_pareto(colunas = ''):
            global pareto_tabela
            pareto_tabela = Tableview(
                tela,
                coldata=colunas,
                rowdata=[],
                autofit=True,
                autoalign=False,
            )
            pareto_tabela.place(relx=0.405,rely=0.45,anchor=CENTER, relheight=0.75, relwidth=0.815)
        # Função para inserir os dados da tabela
        def analise_pareto(tabela=None, grafico=None, name=None):
            global matplot
            if sqlite.sqlite() == None and tabela is None:
                return False
            if isinstance(tabela, str):
                matplot, DataFrame= sqlite.sqlite()
            elif tabela is not None and not tabela.empty:
                DataFrame = tabela
                matplot = grafico
            else:
                matplot, DataFrame= sqlite.sqlite()

            colunas=list(DataFrame)
            colunas_novas = []
            for item in colunas:
                if isinstance(item, str):
                    dicionario = {"text": item, "stretch": True, "width": 120}
                elif isinstance(item, dict):
                    dicionario = item
                colunas_novas.append(dicionario)
            dados=DataFrame.to_numpy().tolist()
            dados = list(reversed(dados))
            pareto_tabela.destroy()
            tabela_analise_pareto(colunas=colunas_novas)
            pareto_tabela.insert_rows(index = 'end', rowdata = dados)
            pareto_tabela.load_table_data()
            self.data_pareto = DataFrame
            if grafico is not None and not grafico.empty:
                ep.tabela_atual_var.set(value=name)
            edit_config.setIsSaved(False)
        # Realiza o bloqueio das entries de dados de acordo com a tabela atual
        def bloquear_entrys():
            if len(pareto_tabela.get_rows()) < 1 or len(pareto_tabela.get_columns()) == 6:
                adicionar_custo.configure(state='normal')
                alterar_custo.configure(state='normal')
            else:
                adicionar_custo.configure(state="disabled")
                alterar_custo.configure(state='disabled')
                
            if ep.tabela_atual_var.get() == 'SELECIONE UMA TABELA':
                adicionar.configure(state='disabled')
                adicionar_quantidade.configure(state='disabled')
                alterar_atual.configure(state='disabled')
                alterar_quantidade.configure(state='disabled')
                alterar_novo.configure(state='disabled')
                adicionar_custo.configure(state="disabled")
                alterar_custo.configure(state='disabled')
                delete.configure(state='disabled')
            else:
                adicionar.configure(state='normal')
                adicionar_quantidade.configure(state='normal')
                alterar_atual.configure(state='normal')
                alterar_quantidade.configure(state='normal')
                alterar_novo.configure(state='normal')
                delete.configure(state='normal')
        # Gerar gráfico de pareto
        def grafico():
            try:
                print(matplot.head(0))
                color1 = 'royalblue'
                color2 = 'black'
                fig,ax1 = plt.subplots(figsize=(15,10))
                ax1.set_title('Pareto')
                if len(pareto_tabela.get_columns()) == 6:
                    ax1.set_ylabel('Custo',color=color1)
                    ax1.bar(matplot['Ocorrências'], matplot['Custo Total'], color=color1, edgecolor='orange', linewidth=2)
                    ax1.tick_params(axis = 'y', labelcolor = color1)
                    
                    for i, valor in enumerate(matplot['Custo Total']):
                        ax1.annotate(f'R$ {valor:.2f}', (i, valor))
                    
                    ax2 = ax1.twinx()
                    ax2.set_ylabel('%', color=color2)
                    ax2.plot(matplot['Ocorrências'], matplot['Freq. Acumulada'], color = color2, marker = 's', markersize = 8, linestyle = '-')
                else:
                    ax1.set_ylabel('Frequência (%)',color=color1)
                    ax1.bar(matplot['Ocorrências'], matplot['Freq. Relativa'], color=color1, edgecolor='orange', linewidth=2)
                    ax1.tick_params(axis = 'y', labelcolor = color1)
                
                    for i, valor in enumerate(matplot['Freq. Relativa']):
                        ax1.annotate(f'{valor:.2f} %', (i, valor))
                    
                    ax2 = ax1.twinx()
                    ax2.set_ylabel('%', color=color2)
                    ax2.plot(matplot['Ocorrências'], matplot['Freq. Acumulada'], color = color2, marker = 's', markersize = 8, linestyle = '-')
            except Exception as e:
                self.app.error_screen(text=f'{e}. Não foi possível gerar gráfico, verifique seus dados e tente novamente',y=120)
                ep.gerar_grafico.configure(style="Estilo1.danger.TButton")
                self.home.after(3000, lambda: ep.gerar_grafico.configure(style="Estilo1.TButton"))
            else:
                ax2.tick_params(axis='y',labelcolor=color2)
                ax2.set_ylim([0,120])
                for i in ax1.get_xticklabels():
                    i.set_rotation(45)
                plt.show()
        #Adicionar ocorrencias na tabela aberta
        def adicionar_itens_funcao():
            custo = adicionar_custo_var.get()
            custos = ''
            for caractere in custo:
                if caractere.isdigit() or caractere in ',.':
                    if caractere == ',': caractere.replace(',','.')
                    custos += caractere
            if len(pareto_tabela.get_columns()) == 6:
                try:
                    tabelas.addValor_pareto(adicionar_var.get(), quantidade=adicionar_quantidade_var.get(), custo=custos)
                except:
                    adicionar.configure(bootstyle="Danger")
                    adicionar_custo.configure(bootstyle="Danger")
                    self.home.after(3000, lambda: (adicionar_custo.configure(bootstyle="Default"), 
                                               adicionar.configure(bootstyle="Default")))
                else:
                    analise_pareto()
                    bloquear_entrys()
                    return 
            if len(pareto_tabela.get_rows()) < 1 or len(pareto_tabela.get_columns()) == 4:
                try:
                    if custos != '':
                        tabelas.addValor_pareto(adicionar_var.get(), quantidade=adicionar_quantidade_var.get(), custo=custos)
                    else:
                        tabelas.addValor_pareto(adicionar_var.get(), quantidade=adicionar_quantidade_var.get())
                except:
                    adicionar.configure(bootstyle="Danger")
                    self.home.after(3000, lambda: adicionar.configure(bootstyle="Default"))
                else:
                    analise_pareto()
                    bloquear_entrys()
        # Atualizar ocorrencia
        def atualizar_itens_funcao():
            if len(pareto_tabela.get_columns()) == 6:
                try:
                    custo = float(alterar_custo_var.get())
                except:
                    alterar_custo.config(bootstyle='Danger')
                    self.home.after(3000,lambda: alterar_custo.config(bootstyle='Default'))
                    return
                else:
                    if not tabelas.atualizar_ocorrencia(alterar_atual_var.get(),
                                                alterar_novo_var.get(),
                                                custo,
                                                alterar_quantidade_var.get()):
                        
                        alterar_atual.config(bootstyle='Danger')
                        alterar_novo.config(bootstyle='Danger')
                        self.home.after(3000,lambda: (alterar_atual.config(bootstyle='Default'),
                                                      alterar_novo.config(bootstyle='Default')))
                        return
            else:
                if not tabelas.atualizar_ocorrencia(ocorrenciaatual=alterar_atual_var.get(),
                                                novaocorrencia=alterar_novo_var.get(),
                                                quantidade=alterar_quantidade_var.get()):
                    
                    alterar_atual.config(bootstyle='Danger')
                    alterar_novo.config(bootstyle='Danger')
                    self.home.after(3000,lambda: (alterar_atual.config(bootstyle='Default'),
                                                alterar_novo.config(bootstyle='Default')))
                    return
                    
            analise_pareto()
            att_max_att()
            bloquear_entrys() 
        # Deletar Item da tabela
        def delete_item():
            if not tabelas.delete_valor_pareto(delete_var.get(), delete_quantidade_var.get()):
                delete.configure(bootstyle='Danger')
                delete_quantidade.configure(bootstyle='Danger')
                self.home.after(3000, lambda: (delete.configure(bootstyle='Default'),
                delete_quantidade.configure(bootstyle='Default')))
                return
            analise_pareto()
            att_max_att()
            bloquear_entrys()
        
        def alterar_custos():
            linhas_tabela = pareto_tabela.tablerows
            if len(pareto_tabela.get_columns()) == 6:
                for linha in linhas_tabela:
                    if linha.values[0] == alterar_atual_var.get():
                        alterar_custo_var.set(value=linha.values[1])
                        alterar_quantidade.configure(to=linha.values[2])
        
        def att_max_att():
            linhas_tabela = pareto_tabela.tablerows
            for linha in linhas_tabela:
                if linha.values[0] == alterar_atual_var.get():
                    if len(pareto_tabela.get_columns()) == 6:
                        alterar_quantidade.configure(to=linha.values[2])
                    else:
                        alterar_quantidade.configure(to=linha.values[1])
        # Widgets de Adicionar
        adicionar_var = ttk.StringVar(value='Ocorrência')
        adicionar = ttk.Entry(ep.adicionar_frame,
                                    textvariable=adicionar_var,
                                    font=self.estilo.fonte)
        adicionar.place(relx=0.02,rely=0.1, relheight=0.35, relwidth=0.72)
        adicionar.bind(
            '<FocusIn>',
            lambda event: (adicionar_var.set(value=''),
                           adicionar.unbind('<FocusIn>')))
        
        adicionar_custo_var = ttk.StringVar(value='Custo Unitário')
        adicionar_custo = ttk.Spinbox(ep.adicionar_frame,
                                    textvariable=adicionar_custo_var,
                                    font=self.estilo.fonte)
        adicionar_custo.place(relx=0.02, rely=0.55, relheight=0.35,relwidth=0.72)
        adicionar_custo.bind(
            '<FocusIn>',
            lambda event: (adicionar_custo_var.set(value=''),
                           adicionar_custo.unbind('<FocusIn>')))
                    
        adicionar_quantidade_var = ttk.IntVar(value=1)
        adicionar_quantidade = ttk.Spinbox(ep.adicionar_frame,
                                            textvariable=adicionar_quantidade_var,
                                            from_=1,
                                            to=10000)
        adicionar_quantidade.place(relx=0.78,rely=0.1, relheight=0.35, relwidth=0.2)
        
        adicionar_btn = ttk.Button(ep.adicionar_frame,
                                          text= 'Adicionar',
                                          width=9,
                                          style='Estilo1.TButton',
                                          command=adicionar_itens_funcao)
        adicionar_btn.place(relx=0.78, rely=0.55, relheight=0.35, relwidth=0.2)
        
        # Widgets de Atualizar
        alterar_atual_var = ttk.StringVar(value='Ocorrência atual')
        alterar_atual = ttk.Entry(ep.atualizar_frame,
                                    textvariable=alterar_atual_var,
                                    width=30,
                                    font=self.estilo.fonte)
        alterar_atual.place(relx=0.02,rely=0.1, relheight=0.35,relwidth=0.72)
        alterar_atual.bind(
            '<FocusIn>',
            lambda event: (alterar_atual_var.set(value=''),
                           alterar_atual.unbind('<FocusIn>')))
        
        alterar_quantidade_var = ttk.IntVar()
        alterar_quantidade = ttk.Spinbox(ep.atualizar_frame,
                                            textvariable=alterar_quantidade_var,
                                            width=10,
                                            from_=1,
                                            to=10000)
        alterar_quantidade.place(relx=0.78,rely=0.1, relheight=0.35, relwidth=0.2)
        
        alterar_novo_var = ttk.StringVar(value='Nova ocorrência')
        alterar_novo = ttk.Entry(ep.atualizar_frame,
                                    textvariable=alterar_novo_var,
                                    width=15,
                                    font=self.estilo.fonte)
        alterar_novo.bind(
            '<FocusIn>',
            lambda event: (alterar_novo_var.set(value=''),
                           alterar_novo.unbind('<FocusIn>')))
        alterar_novo.place(relx=0.02, rely=0.55, relheight=0.35, relwidth=0.36)
        
        alterar_custo_var = StringVar(value='Custo Unitário')
        alterar_custo = ttk.Spinbox(ep.atualizar_frame,
                                    textvariable=alterar_custo_var,
                                    width=10,
                                    from_=1,
                                    font=self.estilo.fonte)
        alterar_custo.place(relx=0.385, rely=0.55, relheight=0.35,relwidth=0.36)
        alterar_custo.bind(
            '<FocusIn>',
            lambda event: (alterar_custo_var.set(value=''),
                           alterar_custo.unbind('<FocusIn>')))
        
        alterar_btn = ttk.Button(ep.atualizar_frame,
                                          text= 'Atualizar',
                                          width=9,
                                          style='Estilo1.TButton',
                                          command=atualizar_itens_funcao)
        alterar_btn.place(relx=0.78, rely=0.55, relheight=0.35,relwidth=0.2)

        # Widgets de Deletar
        delete_var = ttk.StringVar(value='Ocorrência')
        delete = ttk.Entry(ep.delete_frame,
                                    textvariable=delete_var,
                                    font=self.estilo.fonte)
        delete.place(relx=0.375,rely=0.29, relheight=0.35, relwidth=0.72, anchor=CENTER)
        delete.bind(
            '<FocusIn>',
            lambda event: (delete_var.set(value=''),
                           delete.unbind('<FocusIn>')))
        
        delete_quantidade_var = ttk.IntVar()
        delete_quantidade = ttk.Spinbox(ep.delete_frame,
                                            textvariable=delete_quantidade_var,
                                            width=10,
                                            from_=0,
                                            to=10000)
        delete_quantidade.place(relx=0.375,rely=0.75, relheight=0.35, relwidth=0.72, anchor=CENTER)
        
        delete_btn = ttk.Button(ep.delete_frame,
                                          text= 'Deletar',
                                          width=9,
                                          style='Estilo1.TButton',
                                          command=delete_item)
        delete_btn.place(relx=0.86, rely=0.5, relheight=0.35, relwidth=0.23, anchor=CENTER)
        
        ep.tabela_atual_var.trace("w", lambda *args: bloquear_entrys())
        alterar_atual_var.trace("w", lambda *args: alterar_custos())
        
        ep.criar_tabela_botao.configure(command= lambda: ep.criar_tabela(analise_pareto, bloquear_entrys))
        ep.gerar_grafico.configure(command=grafico)
        ep.abrir_tabela_btn.configure(command=lambda: ep.abrir_tabela_selecionada(analise_pareto, bloquear_entrys))
        ep.delete_tabela_botao.configure(command= lambda: ep.delete_tabela(pareto_tabela.destroy, 
                                                                           tabela_analise_pareto,
                                                                           att_max_att,
                                                                           bloquear_entrys))
        
        tabela_analise_pareto()
        bloquear_entrys()
        return analise_pareto
        
    def telas_medidas(self, tela):
        em = Esqueleto(tela, 'medidas', self.app, self)
        tabelas = tabela()
        em.abrir_tabela['value'] = tabelas.getTabelas('medidas')
        
        def mudar_conj_dados():
            atualizar_coluna['value'] = tabelas.get_TableColumns('medidas')
        #Tabela de medidas
        def tabela_medidas_matriz(colunas = ''):
            global tabela_medidas_matrix
            tabela_medidas_matrix = Tableview(
                dados_matriz,
                coldata=colunas,
                rowdata=[],
                autofit=True,
                autoalign=False,
            )
            tabela_medidas_matrix.pack(fill=BOTH, expand=True)   
        def tabela_medidas_formatada():
            global tabela_medidas_format
            tabela_medidas_format = Tableview(
                tabela_formatada,
                coldata=[],
                rowdata=[],
                autofit=True,
                autoalign=False,
            )
            tabela_medidas_format.pack(fill=BOTH, expand=True)   
        def tabela_de_medidas(colunas = ''):
            global tabela_medidas
            tabela_medidas = Tableview(
                medidas_dados,
                coldata=colunas,
                rowdata=[],
                autofit=True,
                autoalign=False,
            )
            tabela_medidas.pack(fill=BOTH, expand=True)  
        def tabela_tdf(colunas = ''):
            global tabela_medidas_tdf
            tabela_medidas_tdf = Tableview(
                tdf_frame,
                coldata=colunas,
                rowdata=[],
                autofit=True,
                autoalign=False,
            )
            tabela_medidas_tdf.pack(fill=BOTH, expand=True)
        # Chama um diálogo com 2 opções de gŕaficos
        def grafico():
            popup = ttk.Toplevel(self.home)
            histograma = ttk.Button(popup, text='Histograma', command=lambda: (Histograma(), popup.destroy()))
            histograma.pack()
            boxplot = ttk.Button(popup, text='BoxPlot', command=lambda:(BoxPlot(), popup.destroy()))
            boxplot.pack()
        # Gráfico Histograma
        def Histograma():
            try:
                print(tabela_df[0])
                color1 = 'royalblue'
                fig,ax1 = plt.subplots(figsize=(15,10))
            except Exception as e:
                self.app.error_screen(text=f'{e}. Não foi possível gerar gráfico, verifique seus dados e tente novamente',y=120)
                em.gerar_grafico.configure(style="Estilo1.danger.TButton")
                self.home.after(3000, lambda: em.gerar_grafico.configure(style="Estilo1.TButton"))
            else:
                ax1.set_title('Distribuição de Frequência')
                ax1.set_ylabel('Frequência (%)',color=color1)
                ax1.bar(tabela_df[1][''], tabela_df[1]['Freq. Relativa %'], color=color1, edgecolor='orange', linewidth=2, width=0.99)
                ax1.tick_params(axis = 'y', labelcolor = color1)
                for i in ax1.get_xticklabels():
                    i.set_rotation(45)
                plt.show()
        # Gráfico BoxPlot
        def BoxPlot():
            try:
                print(tabela_df[0])
            except Exception as e:
                self.app.error_screen(text=f'{e}. Não foi possível gerar gráfico, verifique seus dados e tente novamente',y=120)
                em.gerar_grafico.configure(style="Estilo1.danger.TButton")
                self.home.after(3000, lambda: em.gerar_grafico.configure(style="Estilo1.TButton"))
            else:
                color1 = 'royalblue'
                plt.subplots(figsize=(15,10))
                plt.boxplot(tabela_matriz)
                plt.xlabel('Eixo X')
                plt.ylabel('Eixo Y')
                plt.title('Boxplot')
                plt.show() 
        # Função de adicionar Valores
        def add_valor_tabela():
            medida = inserir_var.get()
            conjunto_dado = inserir_coluna_var.get()
            conj_dados = ''
            for caractere in conjunto_dado:
                if caractere.isdigit():
                    conj_dados += caractere
            try:
                medida = int(medida)
            except:
                inserir.configure(bootstyle="Danger")
                self.home.after(3000, lambda: inserir.configure(bootstyle="Default"))
            else:
                if conj_dados == '':
                    tabelas.add_valor_medidas(medida)
                else:
                    tabelas.add_valor_medidas(medida,conj_dados)
                    
                inserir_coluna['value'] = tabelas.get_TableColumns('medidas')    
                tabelas_medidas()
        # Função de atualizar os dados
        def att_valor_tabela():
            dado_atual = atualizar_atual_var.get()
            novo_dado = atualizar_novo_var.get()
            conjunto_dado = atualizar_coluna_var.get()
            conj_dados = ''
            for caractere in conjunto_dado:
                if caractere.isdigit():
                    conj_dados += caractere
            try:
                conjunto_dado = int(conj_dados)
                dado_atual = float(dado_atual)
                novo_dado = float(novo_dado)
            except:
                atualizar_atual.configure(bootstyle="Danger")
                atualizar_coluna.configure(bootstyle="Danger")
                atualizar_novo.configure(bootstyle="Danger")
                self.home.after(3000, lambda: (atualizar_atual.configure(bootstyle="Default"), 
                                                atualizar_coluna.configure(bootstyle="Default"),
                                                atualizar_novo.configure(bootstyle="Default")))
            else:
                if not tabelas.att_valor_medidas(dado_atual, novo_dado, conjunto_dado):
                    
                    atualizar_atual.configure(bootstyle="Danger")
                    atualizar_coluna.configure(bootstyle="Danger")
                    atualizar_novo.configure(bootstyle="Danger")
                    self.home.after(3000, lambda: (atualizar_atual.configure(bootstyle="Default"), 
                                                    atualizar_coluna.configure(bootstyle="Default"),
                                                    atualizar_novo.configure(bootstyle="Default")))
                else:
                    tabelas_medidas()
        # Função de Deletar os dados
        def deleteValor():
            medida = delete_var.get()
            conjunto_dado = delete_coluna_var.get()
            conj_dados = ''
            for caractere in conjunto_dado:
                if caractere.isdigit():
                    conj_dados += caractere
            try:
                medida = int(medida)
                conj_dados = int(conj_dados)
            except:
                delete.configure(bootstyle="Danger")
                delete_coluna.configure(bootstyle="Danger")
                self.home.after(3000, lambda: (delete.configure(bootstyle="Default"),
                                delete_coluna.configure(bootstyle="Default")))
            else:
                if not tabelas.delete_valor_medidas(medida, conj_dados):
                    delete.configure(bootstyle="Danger")
                    delete_coluna.configure(bootstyle="Danger")
                    self.home.after(3000, lambda: (inserir.configure(bootstyle="Default"),
                                    delete_coluna.configure(bootstyle="Default")))
                else:
                    tabelas_medidas()
            
        # Recarrega os dados das tabelas vazias
        def resetTables():
            tabela_medidas_matrix.destroy()
            tabela_medidas_matriz()
            tabela_medidas_format.destroy()
            tabela_medidas_formatada()
            tabela_medidas.destroy()
            tabela_de_medidas()
            tabela_medidas_tdf.destroy()
            tabela_df =([],DataFrame([], columns=['', 'Freq. Relativa %']))
            tabela_tdf()
        # Insere os dados nas tabelas
        def tabelas_medidas(tabela=None, nome=None):
            importado = 1
            sqlite_table
            if tabela is None or isinstance(tabela, str) or tabela.empty:
                global tabela_df
                global tabela_matriz
                if sqlite_table() == False:
                    return False
                importado = 0
                tabela_desorganizada, tabela = sqlite_table()
                tabela_desorganizada = [dado for dados in tabela_desorganizada for dado in dados] # Cria uma lista com os valores das colunas da tabela
                tabela_matriz = [dado for dado in tabela_desorganizada if dado is not None] # Separa os valores da lista, excluindo os valores Nulos, para matriz
                if not isinstance(tabela, DataFrame):
                    resetTables()
                    return
            else:
                tabela_matriz = tabela.to_numpy().tolist()
                tabela_matriz = [dado for dados in tabela_matriz for dado in dados]
                em.tabela_atual_var.set(value=nome)
            
            self.data_medidas = tabela
            
            # Separa os dados em linhas de 5 valores cada
            linhas = []
            for i in range(0, len(tabela_matriz), 5):
                sublista = tabela_matriz[i:i + 5]
                linhas.append(sublista)
            
            # Matriz de dados
            tabela_medidas_matrix.destroy()
            coluna = [{"text": '', "stretch": True, "width": 120}] * 5
            tabela_medidas_matriz(colunas = coluna)
            tabela_medidas_matrix.insert_rows(index = 0, rowdata = linhas)
            tabela_medidas_matrix.load_table_data()
            
            # Tabela formatada, com tarefas e separação de colunas etc.
            colunas=list(tabela)
            dados=tabela.to_numpy().tolist()
            
            tabela_medidas_format.destroy()
            tabela_medidas_formatada()
            # tabela_medidas_format.insert_column("end", text='Tarefas', stretch=True, width=120)
            for item in colunas:
                tabela_medidas_format.insert_column("end",text=f'{item}', stretch=True, width=120)
            tabela_medidas_format.insert_rows(index=0, rowdata=dados)
            tabela_medidas_format.load_table_data()
            
            # Tabela de medidas
            tabela_medidas.destroy()
            tabela_de_medidas()
            
            #chamando funções de todas as medidas
            media_valores = asyncio.run(media(sqlite_table))
            mediana_valores = asyncio.run(mediana(sqlite_table))
            max_valores = asyncio.run(max(sqlite_table))
            min_valores = asyncio.run(min(sqlite_table))
            amplitude_valores = asyncio.run(amplitude(sqlite_table))
            primeiro_quartil_valores = asyncio.run(primeiro_quartil(sqlite_table))
            terceiro_quartil_valores = asyncio.run(terceiro_quartil(sqlite_table))
            iqr_valores = asyncio.run(iqr(sqlite_table))
            corte_inferior_valores = asyncio.run(corte_inferior(sqlite_table))
            corte_superior_valores = asyncio.run(corte_superior(sqlite_table))
            moda_valores = asyncio.run(moda(sqlite_table))
            
            #colunas da tabela
            colunas = ['Média', 'Mediana', 'Max', 'Min', 'Amplitude', '1ºQuartil', '3ºQuartil','IQR','Corte Inferior', 'Corte Superior', 'Moda']
            for i in colunas:
                tabela_medidas.insert_column("end",text=f'{i}', stretch=True, width=30)
            # adicionando os valores as linhas
            for x in range(len(media_valores)):
                dados = [f'{media_valores[x]:.2f}', f'{mediana_valores[x]:.2f}', f'{max_valores[x]:.2f}', f'{min_valores[x]:.2f}',
                         f'{amplitude_valores[x]:.2f}',f'{primeiro_quartil_valores[x]:.2f}',f'{terceiro_quartil_valores[x]:.2f}',
                         f'{iqr_valores[x]:.2f}',f'{corte_inferior_valores[x]:.2f}',f'{corte_superior_valores[x]:.2f}',
                         moda_valores[x]]
                tabela_medidas.insert_row(index=0,values=dados)
                tabela_medidas.load_table_data()
                
            # Tabela de Distribuição de frequência
            tabela_df = tdf(sqlite_table)
            
            colunas=list(tabela_df[0])
            colunas_novas = []
            for item in colunas:
                if isinstance(item, str):
                    dicionario = {"text": item, "stretch": True, "width": 120}
                elif isinstance(item, dict):
                    dicionario = item
                colunas_novas.append(dicionario)
            dados=tabela_df[0].to_numpy().tolist()
            dados = list(reversed(dados))
            tabela_medidas_tdf.destroy()
            tabela_tdf(colunas=colunas_novas)
            tabela_medidas_tdf.insert_rows(index = 'end', rowdata = dados)
            tabela_medidas_tdf.load_table_data()
            edit_config.setIsSaved(False)
        #Notebok tabelas
        notebook = ttk.Notebook(tela, style='custom.TNotebook')
        notebook.place(relx=0.405,rely=0.45, anchor=CENTER, relheight=0.75, relwidth=0.815)
        
        dados_matriz = ttk.Frame(notebook)
        dados_matriz.pack()
        medidas_dados = ttk.Frame(notebook)
        medidas_dados.pack()
        tabela_formatada = ttk.Frame(notebook)
        tabela_formatada.pack()
        tdf_frame = ttk.Frame(notebook)
        tdf_frame.pack()
        
        notebook.add(dados_matriz, text='Matriz de dados')
        notebook.add(tabela_formatada, text='Tabela formatada')
        notebook.add(medidas_dados, text='Medidas')
        notebook.add(tdf_frame, text='Tabela de distribuição de frequência')

        #Adicionar medidas
        inserir_var = ttk.StringVar(value='Insira o dado')
        inserir = ttk.Entry(em.adicionar_frame,
                        textvariable=inserir_var,
                        font=self.estilo.fonte)
        inserir.place(relx=0.02,rely=0.1, relheight=0.35, relwidth=0.65)
        inserir.bind(
            '<FocusIn>',
            lambda event: (inserir_var.set(value=''),
                           inserir.unbind('<FocusIn>')))
        
        inserir_coluna_var = ttk.StringVar(value='Coluna de dados')
        inserir_coluna = ttk.Combobox(em.adicionar_frame,
                                      textvariable=inserir_coluna_var,
                                      width=15,
                                      font=self.estilo.fonte)
        inserir_coluna.place(relx=0.02, rely=0.55, relheight=0.35,relwidth=0.65)
        inserir_coluna.bind('<FocusIn>', lambda event: (inserir_coluna_var.set(value=''), inserir_coluna.unbind('<FocusIn>')))
        
        inserir_btn = ttk.Button(em.adicionar_frame,
                                          text= 'Adicionar',
                                          width=8,
                                          style='Estilo1.TButton',
                                          command= add_valor_tabela)
        inserir_btn.place(relx=0.83, rely=0.5, relheight=0.35, relwidth=0.3, anchor=CENTER)
        
        #Atualizar dados
        atualizar_atual_var = ttk.StringVar(value='Dado atual')
        atualizar_atual = ttk.Entry(em.atualizar_frame,
                                    textvariable=atualizar_atual_var,
                                    width=10,
                                    font=self.estilo.fonte)
        atualizar_atual.place(relx=0.02,rely=0.1, relheight=0.35, relwidth=0.475)
        atualizar_atual.bind(
            '<FocusIn>',
            lambda event: (atualizar_atual_var.set(value=''),
                           atualizar_atual.unbind('<FocusIn>')))
        
        atualizar_novo_var = ttk.StringVar(value='Novo dado')
        atualizar_novo = ttk.Entry(em.atualizar_frame,
                                    textvariable=atualizar_novo_var,
                                    width=10,
                                    font=self.estilo.fonte)
        atualizar_novo.place(relx=0.505, rely=0.1, relheight=0.35, relwidth=0.475)
        atualizar_novo.bind(
            '<FocusIn>',
            lambda event: (atualizar_novo_var.set(value=''),
                           atualizar_novo.unbind('<FocusIn>')))
        
        atualizar_coluna_var = ttk.StringVar(value='Coluna')
        atualizar_coluna = ttk.Combobox(em.atualizar_frame,
                                      textvariable=atualizar_coluna_var,
                                      width=10,
                                      font=self.estilo.fonte)
        atualizar_coluna.place(relx=0.02, rely=0.55, relheight=0.35,relwidth=0.65)
        atualizar_coluna.bind('<FocusIn>', lambda event: (atualizar_coluna_var.set(value=''),
                                                            atualizar_coluna.unbind('<FocusIn>')))
        
        atualizar_btn = ttk.Button(em.atualizar_frame,
                                          text= 'Atualizar',
                                          width=9,
                                          style='Estilo1.TButton',
                                          command= att_valor_tabela)
        atualizar_btn.place(relx=0.68, rely=0.55, relheight=0.35,relwidth=0.3)
        
        atualizar_atual_var.trace('w', lambda *args: mudar_conj_dados())
        
        # Deletar item da tabela
        delete_var = ttk.StringVar(value='Dado')
        delete = ttk.Entry(em.delete_frame,
                                    textvariable=delete_var,
                                    width=10,
                                    font=self.estilo.fonte)
        delete.place(relx=0.02,rely=0.1, relheight=0.35, relwidth=0.65)
        delete.bind(
            '<FocusIn>',
            lambda event: (delete_var.set(value=''),
                           delete.unbind('<FocusIn>')))
        
        delete_coluna_var = ttk.StringVar(value='Coluna de dados')
        delete_coluna = ttk.Combobox(em.delete_frame,
                                      textvariable=delete_coluna_var,
                                      width=15,
                                      font=self.estilo.fonte)
        delete_coluna.place(relx=0.02, rely=0.55, relheight=0.35,relwidth=0.65)
        delete_coluna.bind('<FocusIn>', lambda event: (delete_coluna_var.set(value=''), delete_coluna.unbind('<FocusIn>')))
        
        delete_btn = ttk.Button(em.delete_frame,
                                          text= 'Deletar',
                                          width=8,
                                          style='Estilo1.TButton',
                                          command= deleteValor)
        delete_btn.place(relx=0.83, rely=0.5, relheight=0.35, relwidth=0.3, anchor=CENTER)
        
        em.criar_tabela_botao.configure(command= lambda: em.criar_tabela(tabelas_medidas))
        em.gerar_grafico.configure(command=grafico)
        em.abrir_tabela_btn.configure(command=lambda: em.abrir_tabela_selecionada(tabelas_medidas))
        em.delete_tabela_botao.configure(command= lambda: em.delete_tabela(resetTables))

        tabela_medidas_matriz()
        tabela_medidas_formatada()
        tabela_de_medidas()
        tabela_tdf()
        
        return tabelas_medidas
    
    def analise_pareto(self, *args):
        self.pareto(*args)
            
    def medidas(self, *args):
        self.medida(*args)
        
    def exportar(self, caminho, tipo, dados):
        if tipo == 'csv':
            if dados == 'pareto':
                self.data_pareto.to_csv(caminho, index=False)
            elif dados == 'medidas':
                self.data_medidas.to_csv(caminho, index=False)
        elif tipo == 'xlsx':
            if dados == 'pareto':
                self.data_pareto.to_excel(caminho, index=False)
            elif dados == 'medidas':
                self.data_medidas.to_excel(caminho, index=False)
        
    def aba_atual(self):
        indice_notebook = self.notebook.index("current")
        self.app.aba_atual = indice_notebook
        self.aba = indice_notebook
        return indice_notebook
    
    def fechar_login(self):
        if edit_config.getSecao() == 'False':
            edit_config.apagar_dados()
        edit_config.limpar_temp()
        edit_config.setIsSaved(True)
        self.home.destroy()
        self.login.destroy()
        
class Esqueleto():
    def __init__(self, tela, aba, aplicativo, home):
        self.estilo = app.Estilo()
        self.tabelas = tabela()
        self.aba = aba
        self.tela = tela
        self.aplicativo = aplicativo
        self.home = home.home
        
        self.tabela_func_frame = ttk.Frame(
            tela,
            style='custom3.TFrame')
        
        self.tabela_func_frame.place(relx=0.91, rely=0.45, anchor='center', relheight=0.75, relwidth=0.18)
        
        self.criar_tabela_var = ttk.StringVar(value='Criar nova Tabela')
        self.criar_tabela_entry = ttk.Entry(
            self.tabela_func_frame,
            textvariable=self.criar_tabela_var,
            font=self.estilo.fonte)
        self.criar_tabela_entry.bind(
            '<FocusIn>',
            lambda event: (self.criar_tabela_var.set(value=''),
                           self.criar_tabela_entry.unbind('<FocusIn>')))
        
        self.criar_tabela_botao = ttk.Button(
            self.tabela_func_frame,
            text='Criar',
            style='Estilo1.TButton'
        )
        
        self.criar_tabela_label = ttk.Label(
            self.tabela_func_frame,
            text='Criar uma nova tabela',
            style='Comum2.TLabel',
        )
        
        self.criar_tabela_label.place(relx=0.5, rely=0.04, anchor=CENTER)
        self.criar_tabela_entry.place(relx=0.5, rely=0.12, relheight=0.1, relwidth=0.95,anchor=CENTER)
        self.criar_tabela_botao.place(relx=0.5, rely=0.23, relheight=0.1, relwidth=0.5,anchor=CENTER)
                
        ttk.Separator(self.tabela_func_frame,style='custom.TSeparator').place(anchor=CENTER, relx=0.5, rely=0.3,relwidth=0.97)
        
        self.abrir_tabela_var = ttk.StringVar(value='Abrir uma tabela')
        self.abrir_tabela = ttk.Combobox(self.tabela_func_frame,
                                    textvariable=self.abrir_tabela_var,
                                    font=self.estilo.fonte)
        
        self.abrir_tabela_btn = ttk.Button(self.tabela_func_frame,
                                      text='Abrir',
                                      style='Estilo1.TButton')
        
        self.abrir_tabela_label = ttk.Label(
            self.tabela_func_frame,
            text='Abrir uma tabela existente',
            style='Comum2.TLabel',
        )
        
        self.abrir_tabela_label.place(relx=0.5, rely=0.33,anchor=CENTER)
        self.abrir_tabela_btn.place(relx=0.5, rely=0.49, relheight=0.1, relwidth=0.5,anchor=CENTER)
        self.abrir_tabela.place(relx=0.5, rely=0.395, relwidth=0.95,anchor=CENTER)
        
        ttk.Separator(self.tabela_func_frame,style='custom.TSeparator').place(anchor=CENTER, relx=0.5, rely=0.555,relwidth=0.97)
        
        self.gerar_grafico_label = ttk.Label(
            self.tabela_func_frame,
            text='Gerar gráfico de Pareto',
            style='Comum2.TLabel'
        )
        self.gerar_grafico_label.place(relx=0.5, rely=0.58,anchor=CENTER)
        self.gerar_grafico_label.lower()
        self.gerar_grafico = ttk.Button(self.tabela_func_frame,text='Gerar gráfico',style='Estilo1.TButton')
        self.gerar_grafico.place(relx=0.5, rely=0.66, relheight=0.1, relwidth=0.7,anchor=CENTER)
        
        ttk.Separator(self.tabela_func_frame,style='custom.TSeparator').place(anchor=CENTER, relx=0.5, rely=0.725,relwidth=0.97)
        
        self.delete_tabela_label = ttk.Label(
            self.tabela_func_frame,
            text='Deletar Tabela',
            style='Comum2.TLabel'
        )
        
        self.delete_tabela_var = ttk.StringVar(value='Deletar Tabela')
        self.delete_tabela_entry = ttk.Entry(
            self.tabela_func_frame,
            textvariable=self.delete_tabela_var,
            font=self.estilo.fonte)
        self.delete_tabela_entry.bind(
            '<FocusIn>',
            lambda event: (self.delete_tabela_var.set(value=''),
                           self.delete_tabela_entry.unbind('<FocusIn>')))
        
        self.delete_tabela_botao = ttk.Button(
            self.tabela_func_frame,
            text='Deletar',
            style='Estilo1.TButton',
        )
        
        self.delete_tabela_label.place(relx=0.5, rely=0.75, anchor=CENTER)
        self.delete_tabela_entry.place(relx=0.5, rely=0.82, relheight=0.1, relwidth=0.95,anchor=CENTER)
        self.delete_tabela_botao.place(relx=0.5, rely=0.93, relheight=0.1, relwidth=0.5,anchor=CENTER)
        
        self.adicionar_frame = ttk.Frame(tela, style='custom3.TFrame')
        self.adicionar_frame.place(relx=0.165, rely=0.915, anchor=CENTER, relheight=0.16, relwidth=0.33)
        
        self.atualizar_frame = ttk.Frame(tela, style='custom3.TFrame')
        self.atualizar_frame.place(relx=0.5, rely=0.915, anchor=CENTER, relheight=0.16, relwidth=0.33)
        
        self.delete_frame = ttk.Frame(tela, style='custom3.TFrame')
        self.delete_frame.place(relx=0.835, rely=0.915, anchor=CENTER, relheight=0.16, relwidth=0.33)
        
        self.tabela_atual_var = StringVar(value='SELECIONE UMA TABELA')
        self.tabela_atual = ttk.Label(tela,textvariable=self.tabela_atual_var,style='Titulo2.TLabel')
        self.tabela_atual.place(relx=0.35,rely=0.05,anchor=CENTER)
        
        def set_tabela(dados):
            if dados == 0:
                home.tabela_pareto = self.tabela_atual_var.get()
            elif dados == 1:
                home.tabela_medidas = self.tabela_atual_var.get()
                
        self.tabela_atual_var.trace('w', lambda *args: set_tabela(home.aba))
    
    #Criar uma tabela nova
    def criar_tabela(self,*args, **kwargs):
        criar_tabela = tabela(self.criar_tabela_var.get())
        
        try:
            criar_tabela = criar_tabela.CriarBD(dados=self.aba)
            self.tabela_atual_var.set(value=self.criar_tabela_var.get())
            
        except Exception as e:
            self.aplicativo.error_screen(text=f'{e}: Nome da tabela inválido')
            self.criar_tabela_entry.config(bootstyle="Danger")
            self.home.after(3000,lambda: self.criar_tabela_entry.config(bootstyle="Default"))
            return
        else:
            for i in args:
                i()
            for x in kwargs:
                x
    # Deletar Tabela
    def delete_tabela(self,*args, **kwargs):
        confirmar = self.aplicativo.error_screen(text=f'Deseja realmente deletar a tabela: {self.delete_tabela_var.get()}?\nAs informações podem ser perdidas.',
                                                 buttons=["Sim:danger","Não:primary"], y=120, x=220)
        if confirmar == 'Sim':
            try:
                self.tabelas.DropTable(tabela = self.delete_tabela_var.get(),dados = self.aba)
            except Exception as e:
                print(e)
                self.delete_tabela_entry.configure(bootstyle = 'Danger')
                self.home.after(3000, lambda: self.delete_tabela_entry.configure(bootstyle = 'Default'))
            else:
                for i in args:
                    i()
                for x in kwargs:
                    x
                
    def abrir_tabela_selecionada(self, *args, **kwargs):
        try:
            self.tabelas.SelectTabela(self.abrir_tabela_var.get(), self.aba)
            if args[0]() == False: raise Exception("None")
            self.tabela_atual_var.set(value=self.abrir_tabela_var.get())
        except Exception as e:
            print(e)
            self.aplicativo.error_screen(text='Nenhuma tabela selecionada')
            self.abrir_tabela.config(bootstyle="Danger")
            self.home.after(3000,lambda: self.abrir_tabela.config(bootstyle="Default"))
        else:
            for i in args[1:]:
                i()
            for x in kwargs:
                x
             