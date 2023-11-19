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

#TODO:
# Salvamento de arquivos em tabelas sqlite

# TRATAMENTO DE ERROS E RETORNO VISUAL PARA O USUARIO COM POPUPS - URGENTE

class inicio:
    def __init__(self, login=''):
        self.login = login
        self.home = ttk.Toplevel()
        self.app = app.Tela(self.home, 'Peraeque - Início')
        self.app.centralizarTela(900, 600)
        self.app.menu()
        self.app.instancia_com_tabela = self
        self.app.aba_atual = 0
        self.app.home = self.home
        
        self.width = self.home.winfo_screenwidth()
        self.height = self.home.winfo_screenheight()
        
        #Estilo da tela
        colors = self.login.style.colors
        self.estilo = app.Estilo()
        
        #notebook
        self.notebook = ttk.Notebook(self.home)
        self.notebook.pack(expand=True)
        
        self.tela_pareto = ttk.Frame(self.notebook, width=self.width,  height=self.height)
        self.tela_pareto.pack(fill='both', expand=True)
        self.tela_medidas = ttk.Frame(self.notebook, width=self.width,  height=self.height)
        self.tela_medidas.pack(fill='both',expand=True)
        self.tela_binomial = ttk.Frame(self.notebook, width=self.width,  height=self.height)
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
        #Pegar dados para criar tabela análise de pareto
        sqlite = pareto()
        
        #Tabela da análise de pareto
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
        
        def analise_pareto(tabela=None, grafico=None, name=None):
            global matplot
            if sqlite.sqlite() == None:
                edit_config.setIsSaved(False)
                return
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
                tabela_atual_var.set(value=name)
            edit_config.setIsSaved(False)
        
        # Gerar gráfico com matplotlib
        def grafico():
            
            color1 = 'royalblue'
            color2 = 'black'

            fig,ax1 = plt.subplots(figsize=(15,10))

            ax1.set_title('Pareto')
            
            try:
                ax1.set_ylabel('Custo',color=color1)
                
                ax1.bar(matplot['Ocorrências'], matplot['Custo Total'], color=color1, edgecolor='orange', linewidth=2)

                ax1.tick_params(axis = 'y', labelcolor = color1)
                
                for i, valor in enumerate(matplot['Custo Total']):
                    ax1.annotate(f'R$ {valor:.2f}', (i, valor))
                
                ax2 = ax1.twinx()
                ax2.set_ylabel('%', color=color2)

                ax2.plot(matplot['Ocorrências'], matplot['Freq. Acumulada'], color = color2, marker = 's', markersize = 8, linestyle = '-')

            except Exception as e:

                ax1.set_ylabel('Frequência (%)',color=color1)
                
                ax1.bar(matplot['Ocorrências'], matplot['Freq. Relativa'], color=color1, edgecolor='orange', linewidth=2)

                ax1.tick_params(axis = 'y', labelcolor = color1)
                
                for i, valor in enumerate(matplot['Freq. Relativa']):
                    ax1.annotate(f'{valor:.2f} %', (i, valor))
                
                ax2 = ax1.twinx()
                ax2.set_ylabel('%', color=color2)

                ax2.plot(matplot['Ocorrências'], matplot['Freq. Acumulada'], color = color2, marker = 's', markersize = 8, linestyle = '-')

            ax2.tick_params(axis='y',labelcolor=color2)
            ax2.set_ylim([0,120])

            for i in ax1.get_xticklabels():
                i.set_rotation(45)
            plt.show()
        
        #Criar uma tabela nova
        tabela_func_frame = ttk.Frame(
            tela,
            style='custom.TFrame')
        
        criar_tabela_var = ttk.StringVar(value='Criar nova Tabela')
        criar_tabela_entry = ttk.Entry(
            tabela_func_frame,
            textvariable=criar_tabela_var,
            font=self.estilo.fonte)
        criar_tabela_entry.bind(
            '<FocusIn>',
            lambda event: (criar_tabela_var.set(value=''),
                           criar_tabela_entry.unbind('<FocusIn>')))
        
        criar_tabela_botao = ttk.Button(
            tabela_func_frame,
            text='Criar',
            style='Estilo1.TButton',
            command=lambda: criar_tabela()
        )
        
        criar_tabela_label = ttk.Label(
            tabela_func_frame,
            text='Criar uma nova tabela',
            style='Comum.TLabel',
        )
        
        def criar_tabela():
            criar_tabela = tabela(criar_tabela_var.get())
            criar_tabela = criar_tabela.CriarBD('pareto')
            tabela_atual_var.set(value=criar_tabela_var.get())
            analise_pareto()
            bloquear_entrys()
        
        tabela_func_frame.place(relx=0.91, rely=0.45, anchor='center', relheight=0.75, relwidth=0.18)
        
        criar_tabela_label.place(relx=0.5, rely=0.04, anchor=CENTER)
        criar_tabela_entry.place(relx=0.5, rely=0.12, relheight=0.1, relwidth=0.95,anchor=CENTER)
        criar_tabela_botao.place(relx=0.5, rely=0.23, relheight=0.1, relwidth=0.5,anchor=CENTER)
        
        #Abrir tabelas já existentes
        tabelas = tabela()
        
        def abrir_tabela_selecionada():
            tabelas.SelectTabela(abrir_tabela_var.get(), 'pareto')
            analise_pareto()
            tabela_atual_var.set(value=abrir_tabela_var.get())
            bloquear_entrys()
    
        abrir_tabela_var = ttk.StringVar(value='Abrir uma tabela')
        abrir_tabela = ttk.Combobox(tabela_func_frame,
                                    textvariable=abrir_tabela_var,
                                    font=self.estilo.fonte)
        
        abrir_tabela['value'] = tabelas.getTabelas('pareto')
        
        abrir_tabela_btn = ttk.Button(tabela_func_frame,
                                      text='Abrir',
                                      style='Estilo1.TButton',
                                      command=abrir_tabela_selecionada)
        
        abrir_tabela_label = ttk.Label(
            tabela_func_frame,
            text='Abrir uma tabela existente',
            style='Comum.TLabel',
        )
        
        abrir_tabela_label.place(relx=0.5, rely=0.33,anchor=CENTER)
        abrir_tabela_btn.place(relx=0.5, rely=0.49, relheight=0.1, relwidth=0.5,anchor=CENTER)
        abrir_tabela.place(relx=0.5, rely=0.395, relwidth=0.95,anchor=CENTER)
        
        gerar_grafico_label = ttk.Label(
            tabela_func_frame,
            text='Gerar gráfico de Pareto',
            style='Comum.TLabel'
        )
        gerar_grafico_label.place(relx=0.5, rely=0.58,anchor=CENTER)
        gerar_grafico = ttk.Button(tabela_func_frame,text='Gerar gráfico',style='Estilo1.TButton', command=grafico)
        gerar_grafico.place(relx=0.5, rely=0.66, relheight=0.1, relwidth=0.7,anchor=CENTER)
        
        delete_tabela_label = ttk.Label(
            tabela_func_frame,
            text='Deletar Tabela',
            style='Comum.TLabel'
        )
        
        delete_tabela_var = ttk.StringVar(value='Deletar Tabela')
        delete_tabela_entry = ttk.Entry(
            tabela_func_frame,
            textvariable=delete_tabela_var,
            font=self.estilo.fonte)
        delete_tabela_entry.bind(
            '<FocusIn>',
            lambda event: (delete_tabela_var.set(value=''),
                           delete_tabela_entry.unbind('<FocusIn>')))
        
        delete_tabela_botao = ttk.Button(
            tabela_func_frame,
            text='Deletar',
            style='Estilo1.TButton',
            command=lambda: criar_tabela()
        )
        
        delete_tabela_label.place(relx=0.5, rely=0.75, anchor=CENTER)
        delete_tabela_entry.place(relx=0.5, rely=0.82, relheight=0.1, relwidth=0.95,anchor=CENTER)
        delete_tabela_botao.place(relx=0.5, rely=0.93, relheight=0.1, relwidth=0.5,anchor=CENTER)
        
        #Adicionar ocorrencias na tabela aberta
        
        def adicionar_itens_funcao():
            custo = adicionar_custo_var.get()
            try:
                float(custo)
                tabelas.addValor_pareto(adicionar_itens_var.get(), quantidade=quantidade_ocorrencia_var.get(), custo=custo)
            except:
                tabelas.addValor_pareto(adicionar_itens_var.get(), quantidade=quantidade_ocorrencia_var.get())
            analise_pareto()
            bloquear_entrys()
        
        adicionar_itens_frame = ttk.Frame(tela, style='custom.TFrame')
        adicionar_itens_frame.place(relx=0.165, rely=0.915, anchor=CENTER, relheight=0.16, relwidth=0.33)
        
        adicionar_itens_var = ttk.StringVar(value='Ocorrência')
        adicionar_itens = ttk.Entry(adicionar_itens_frame,
                                    textvariable=adicionar_itens_var,
                                    font=self.estilo.fonte)
        adicionar_itens.place(relx=0.02,rely=0.1, relheight=0.35, relwidth=0.72)
        adicionar_itens.bind(
            '<FocusIn>',
            lambda event: (adicionar_itens_var.set(value=''),
                           adicionar_itens.unbind('<FocusIn>')))
        
        adicionar_custo_var = ttk.StringVar(value='Custo Unitário')
        adicionar_custo = ttk.Spinbox(adicionar_itens_frame,
                                    textvariable=adicionar_custo_var,
                                    font=self.estilo.fonte)
        adicionar_custo.place(relx=0.02, rely=0.55, relheight=0.35,relwidth=0.72)
        adicionar_custo.bind(
            '<FocusIn>',
            lambda event: (adicionar_custo_var.set(value=''),
                           adicionar_custo.unbind('<FocusIn>')))
        
        def bloquear_entrys():
            if len(pareto_tabela.get_rows()) < 1 or len(pareto_tabela.get_columns()) == 6:
                adicionar_custo.configure(state='normal')
                alterar_custo.configure(state='normal')
            else:
                adicionar_custo.configure(state="disabled")
                alterar_custo.configure(state='disabled')
                
            if tabela_atual_var.get() == 'SELECIONE UMA TABELA':
                adicionar_itens.configure(state='disabled')
                quantidade_ocorrencia.configure(state='disabled')
                ocorrencia_atual.configure(state='disabled')
                ocorrencia_quantidade.configure(state='disabled')
                ocorrencia_nova.configure(state='disabled')
                adicionar_custo.configure(state="disabled")
                alterar_custo.configure(state='disabled')
                delete_itens.configure(state='disabled')
            else:
                adicionar_itens.configure(state='normal')
                quantidade_ocorrencia.configure(state='normal')
                ocorrencia_atual.configure(state='normal')
                ocorrencia_quantidade.configure(state='normal')
                ocorrencia_nova.configure(state='normal')
                delete_itens.configure(state='normal')
                    
        quantidade_ocorrencia_var = ttk.IntVar(value=1)
        quantidade_ocorrencia = ttk.Spinbox(adicionar_itens_frame,
                                            textvariable=quantidade_ocorrencia_var,
                                            from_=1,
                                            to=10000)
        quantidade_ocorrencia.place(relx=0.78,rely=0.1, relheight=0.35, relwidth=0.2)
        
        adicionar_itens_plus = ttk.Button(adicionar_itens_frame,
                                          text= 'Adicionar',
                                          width=9,
                                          style='Estilo1.TButton',
                                          command=adicionar_itens_funcao)
        adicionar_itens_plus.place(relx=0.78, rely=0.55, relheight=0.35, relwidth=0.2)
        
        # Atualizar ocorrencia
        def atualizar_itens_funcao():
            if len(pareto_tabela.get_columns()) == 6:
                tabelas.atualizar_custo(ocorrencia_atual_var.get(),alterar_custo_var.get())
            tabelas.atualizar_ocorrencia(ocorrencia_atual_var.get(),ocorrencia_nova_var.get(),ocorrencia_quantidade_var.get())
            analise_pareto()
            att_max_att()
            bloquear_entrys()
        
        atualizar_itens_frame = ttk.Frame(tela, style='custom.TFrame')
        atualizar_itens_frame.place(relx=0.5, rely=0.915, anchor=CENTER, relheight=0.16, relwidth=0.33)
        
        ocorrencia_atual_var = ttk.StringVar(value='Ocorrência atual')
        ocorrencia_atual = ttk.Entry(atualizar_itens_frame,
                                    textvariable=ocorrencia_atual_var,
                                    width=30,
                                    font=self.estilo.fonte)
        ocorrencia_atual.place(relx=0.02,rely=0.1, relheight=0.35,relwidth=0.72)
        ocorrencia_atual.bind(
            '<FocusIn>',
            lambda event: (ocorrencia_atual_var.set(value=''),
                           ocorrencia_atual.unbind('<FocusIn>')))
        
        ocorrencia_quantidade_var = ttk.IntVar()
        ocorrencia_quantidade = ttk.Spinbox(atualizar_itens_frame,
                                            textvariable=ocorrencia_quantidade_var,
                                            width=10,
                                            from_=1,
                                            to=10000)
        ocorrencia_quantidade.place(relx=0.78,rely=0.1, relheight=0.35, relwidth=0.2)
        
        ocorrencia_nova_var = ttk.StringVar(value='Nova ocorrência')
        ocorrencia_nova = ttk.Entry(atualizar_itens_frame,
                                    textvariable=ocorrencia_nova_var,
                                    width=15,
                                    font=self.estilo.fonte)
        ocorrencia_nova.bind(
            '<FocusIn>',
            lambda event: (ocorrencia_nova_var.set(value=''),
                           ocorrencia_nova.unbind('<FocusIn>')))
        ocorrencia_nova.place(relx=0.02, rely=0.55, relheight=0.35, relwidth=0.36)
        
        alterar_custo_var = StringVar(value='Custo Unitário')
        alterar_custo = ttk.Spinbox(atualizar_itens_frame,
                                    textvariable=alterar_custo_var,
                                    width=10,
                                    from_=1,
                                    font=self.estilo.fonte)
        alterar_custo.place(relx=0.385, rely=0.55, relheight=0.35,relwidth=0.36)
        alterar_custo.bind(
            '<FocusIn>',
            lambda event: (alterar_custo_var.set(value=''),
                           alterar_custo.unbind('<FocusIn>')))
        
        atualizar_itens_plus = ttk.Button(atualizar_itens_frame,
                                          text= 'Atualizar',
                                          width=9,
                                          style='Estilo1.TButton',
                                          command=atualizar_itens_funcao)
        atualizar_itens_plus.place(relx=0.78, rely=0.55, relheight=0.35,relwidth=0.2)
        
        # Deletar Item da tabela
        delete_itens_frame = ttk.Frame(tela, style='custom.TFrame')
        delete_itens_frame.place(relx=0.835, rely=0.915, anchor=CENTER, relheight=0.16, relwidth=0.33)
        
        delete_itens_var = ttk.StringVar(value='Ocorrência')
        delete_itens = ttk.Entry(delete_itens_frame,
                                    textvariable=delete_itens_var,
                                    font=self.estilo.fonte)
        delete_itens.place(relx=0.375,rely=0.5, relheight=0.35, relwidth=0.72, anchor=CENTER)
        delete_itens.bind(
            '<FocusIn>',
            lambda event: (delete_itens_var.set(value=''),
                           delete_itens.unbind('<FocusIn>')))
        
        delete_itens_plus = ttk.Button(delete_itens_frame,
                                          text= 'Deletar',
                                          width=9,
                                          style='Estilo1.TButton',
                                          command=adicionar_itens_funcao)
        delete_itens_plus.place(relx=0.86, rely=0.5, relheight=0.35, relwidth=0.23, anchor=CENTER)
        
        
        # Display tabela atual
        tabela_atual_var = StringVar(value='SELECIONE UMA TABELA')
        tabela_atual = ttk.Label(tela,textvariable=tabela_atual_var,style='Titulo.TLabel')
        tabela_atual.place(relx=0.35,rely=0.05,anchor=CENTER)
        tabela_atual_var.trace("w", lambda *args: bloquear_entrys())
        
        
        ocorrencia_atual_var.trace("w", lambda *args: alterar_custos())
        
        def alterar_custos():
            linhas_tabela = pareto_tabela.tablerows
            if len(pareto_tabela.get_columns()) == 6:
                for linha in linhas_tabela:
                    if linha.values[0] == ocorrencia_atual_var.get():
                        alterar_custo_var.set(value=linha.values[1])
                        ocorrencia_quantidade.configure(to=linha.values[2])
        
        def att_max_att():
            linhas_tabela = pareto_tabela.tablerows
            for linha in linhas_tabela:
                if linha.values[0] == ocorrencia_atual_var.get():
                    if len(pareto_tabela.get_columns()) == 6:
                        ocorrencia_quantidade.configure(to=linha.values[2])
                    else:
                        ocorrencia_quantidade.configure(to=linha.values[1])
        
        def set_tabela():
            self.tabela_pareto = tabela_atual_var.get()
        tabela_atual_var.trace('w', lambda *args: set_tabela())
            
        tabela_analise_pareto()
        bloquear_entrys()
        return analise_pareto
        
    def telas_medidas(self, tela):
        #Notebok tabelas
        notebook = ttk.Notebook(tela)
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
        
        #Criar uma tabela nova
        tabela_func_frame = ttk.Frame(
            tela,
            style='custom.TFrame')
        
        criar_tabela_var = ttk.StringVar(value='Criar nova Tabela')
        criar_tabela_entry = ttk.Entry(
            tabela_func_frame,
            textvariable=criar_tabela_var,
            font=self.estilo.fonte)
        criar_tabela_entry.bind(
            '<FocusIn>',
            lambda event: (criar_tabela_var.set(value=''),
                           criar_tabela_entry.unbind('<FocusIn>')))
        
        criar_tabela_botao = ttk.Button(
            tabela_func_frame,
            text='Criar',
            style='Estilo1.TButton',
            command=lambda: criar_tabela()
        )
        
        criar_tabela_label = ttk.Label(
            tabela_func_frame,
            text='Criar uma nova tabela',
            style='Comum.TLabel',
        )
        
        tabela_func_frame.place(relx=0.91, rely=0.45, anchor='center', relheight=0.75, relwidth=0.18)
        
        criar_tabela_label.place(relx=0.5, rely=0.04, anchor=CENTER)
        criar_tabela_entry.place(relx=0.5, rely=0.12, relheight=0.1, relwidth=0.95,anchor=CENTER)
        criar_tabela_botao.place(relx=0.5, rely=0.23, relheight=0.1, relwidth=0.5,anchor=CENTER)

        #Abri tabela existente
        abrir_tabela_var = ttk.StringVar(value='Abrir uma tabela')
        abrir_tabela = ttk.Combobox(tabela_func_frame,
                                    width=30,
                                    textvariable=abrir_tabela_var,
                                    font=self.estilo.fonte)
        
        abrir_tabela_btn = ttk.Button(tabela_func_frame,
                                      text='Abrir',
                                      style='Estilo1.TButton',
                                      command= lambda: abrir_tabela_selecionada()
                                    )
        
        abrir_tabela_label = ttk.Label(
            tabela_func_frame,
            text='Abrir uma tabela existente',
            style='Comum.TLabel',
        )
        
        abrir_tabela_label.place(relx=0.5, rely=0.33,anchor=CENTER)
        abrir_tabela_btn.place(relx=0.5, rely=0.49, relheight=0.1, relwidth=0.5,anchor=CENTER)
        abrir_tabela.place(relx=0.5, rely=0.395, relwidth=0.95,anchor=CENTER)
        
        gerar_grafico_label = ttk.Label(
            tabela_func_frame,
            text='Gerar gráficos',
            style='Comum.TLabel'
        )
        gerar_grafico_label.place(relx=0.5, rely=0.58,anchor=CENTER)
        gerar_grafico = ttk.Button(tabela_func_frame,text='Gerar gráfico',style='Estilo1.TButton', command= lambda: grafico())
        gerar_grafico.place(relx=0.5, rely=0.66, relheight=0.1, relwidth=0.7,anchor=CENTER)
        
        delete_tabela_label = ttk.Label(
            tabela_func_frame,
            text='Deletar Tabela',
            style='Comum.TLabel'
        )
        
        delete_tabela_var = ttk.StringVar(value='Deletar Tabela')
        delete_tabela_entry = ttk.Entry(
            tabela_func_frame,
            textvariable=delete_tabela_var,
            font=self.estilo.fonte)
        delete_tabela_entry.bind(
            '<FocusIn>',
            lambda event: (delete_tabela_var.set(value=''),
                           delete_tabela_entry.unbind('<FocusIn>')))
        
        delete_tabela_botao = ttk.Button(
            tabela_func_frame,
            text='Deletar',
            style='Estilo1.TButton',
            command=lambda: criar_tabela()
        )
        
        delete_tabela_label.place(relx=0.5, rely=0.75, anchor=CENTER)
        delete_tabela_entry.place(relx=0.5, rely=0.82, relheight=0.1, relwidth=0.95,anchor=CENTER)
        delete_tabela_botao.place(relx=0.5, rely=0.93, relheight=0.1, relwidth=0.5,anchor=CENTER)
        
        # Display tabela atual
        tabela_atual_var = StringVar(value='SELECIONE UMA TABELA')
        tabela_atual = ttk.Label(tela,textvariable=tabela_atual_var,style='Titulo.TLabel')
        tabela_atual.place(relx=0.35,rely=0.05,anchor=CENTER)
        
        #Adicionar medidas
        conjunto_de_dados_frame = ttk.Frame(tela, style='custom.TFrame')
        conjunto_de_dados_frame.place(relx=0.165, rely=0.915, anchor=CENTER, relheight=0.16, relwidth=0.33)
        
        dados_var = ttk.StringVar(value='Insira o dado')
        dados = ttk.Entry(conjunto_de_dados_frame,
                                    textvariable=dados_var,
                                    font=self.estilo.fonte)
        dados.place(relx=0.02,rely=0.1, relheight=0.35, relwidth=0.65)
        dados.bind(
            '<FocusIn>',
            lambda event: (dados_var.set(value=''),
                           dados.unbind('<FocusIn>')))
        
        conjunto_dados_var = ttk.StringVar(value='Coluna de dados')
        conjunto_dados = ttk.Combobox(conjunto_de_dados_frame,
                                      textvariable=conjunto_dados_var,
                                      width=15,
                                      font=self.estilo.fonte)
        conjunto_dados.place(relx=0.02, rely=0.55, relheight=0.35,relwidth=0.65)
        conjunto_dados.bind('<FocusIn>', lambda event: (conjunto_dados_var.set(value=''), conjunto_dados.unbind('<FocusIn>')))
        
        inserir_dados_btn = ttk.Button(conjunto_de_dados_frame,
                                          text= 'Adicionar',
                                          width=8,
                                          style='Estilo1.TButton',
                                          command= lambda: add_valor_tabela())
        inserir_dados_btn.place(relx=0.83, rely=0.5, relheight=0.35, relwidth=0.3, anchor=CENTER)
        
        #Atualizar dados
        atualizar_itens_frame = ttk.Frame(tela, style='custom.TFrame')
        atualizar_itens_frame.place(relx=0.5, rely=0.915, anchor=CENTER, relheight=0.16, relwidth=0.33)
        
        medida_atual_var = ttk.StringVar(value='Dado atual')
        medida_atual = ttk.Entry(atualizar_itens_frame,
                                    textvariable=medida_atual_var,
                                    width=10,
                                    font=self.estilo.fonte)
        medida_atual.place(relx=0.02,rely=0.1, relheight=0.35, relwidth=0.475)
        medida_atual.bind(
            '<FocusIn>',
            lambda event: (medida_atual_var.set(value=''),
                           medida_atual.unbind('<FocusIn>')))
        
        medida_nova_var = ttk.StringVar(value='Novo dado')
        medida_nova = ttk.Entry(atualizar_itens_frame,
                                    textvariable=medida_nova_var,
                                    width=10,
                                    font=self.estilo.fonte)
        medida_nova.place(relx=0.505, rely=0.1, relheight=0.35, relwidth=0.475)
        medida_nova.bind(
            '<FocusIn>',
            lambda event: (medida_nova_var.set(value=''),
                           medida_nova.unbind('<FocusIn>')))
        
        conjunto_dados_new_var = ttk.StringVar(value='Coluna')
        conjunto_dados_new = ttk.Combobox(atualizar_itens_frame,
                                      textvariable=conjunto_dados_new_var,
                                      width=10,
                                      font=self.estilo.fonte)
        conjunto_dados_new.place(relx=0.02, rely=0.55, relheight=0.35,relwidth=0.65)
        conjunto_dados_new.bind('<FocusIn>', lambda event: (conjunto_dados_new_var.set(value=''),
                                                            conjunto_dados_new.unbind('<FocusIn>')))
        
        atualizar_itens_plus = ttk.Button(atualizar_itens_frame,
                                          text= 'Atualizar',
                                          width=9,
                                          style='Estilo1.TButton',
                                          command= lambda: att_valor_tabela())
        atualizar_itens_plus.place(relx=0.68, rely=0.55, relheight=0.35,relwidth=0.3)
        
        medida_atual_var.trace('w', lambda *args: mudar_conj_dados())
        
        # Deletar item da tabela
        delete_itens_frame = ttk.Frame(tela, style='custom.TFrame')
        delete_itens_frame.place(relx=0.835, rely=0.915, anchor=CENTER, relheight=0.16, relwidth=0.33)
        
        medida_delete_var = ttk.StringVar(value='Dado')
        medida_delete = ttk.Entry(delete_itens_frame,
                                    textvariable=medida_delete_var,
                                    width=10,
                                    font=self.estilo.fonte)
        medida_delete.place(relx=0.02,rely=0.1, relheight=0.35, relwidth=0.65)
        medida_delete.bind(
            '<FocusIn>',
            lambda event: (medida_delete_var.set(value=''),
                           medida_delete.unbind('<FocusIn>')))
        
        conjunto_de_dados_var = ttk.StringVar(value='Coluna de dados')
        conjunto_de_dados = ttk.Combobox(delete_itens_frame,
                                      textvariable=conjunto_de_dados_var,
                                      width=15,
                                      font=self.estilo.fonte)
        conjunto_de_dados.place(relx=0.02, rely=0.55, relheight=0.35,relwidth=0.65)
        conjunto_de_dados.bind('<FocusIn>', lambda event: (conjunto_de_dados_var.set(value=''), conjunto_de_dados.unbind('<FocusIn>')))
        
        delete_dados_btn = ttk.Button(delete_itens_frame,
                                          text= 'Deletar',
                                          width=8,
                                          style='Estilo1.TButton',
                                          command= lambda: add_valor_tabela())
        delete_dados_btn.place(relx=0.83, rely=0.5, relheight=0.35, relwidth=0.3, anchor=CENTER)
        
        def mudar_conj_dados():
            conjunto_dados_new['value'] = tabelas.get_TableColumns('medidas')
        
        tabelas = tabela()
        abrir_tabela['value'] = tabelas.getTabelas('medidas')
        
        def criar_tabela():
            criar_tabela = tabela(criar_tabela_var.get())
            criar_tabela = criar_tabela.CriarBD('medidas')
            tabela_atual_var.set(value=criar_tabela_var.get())
            asyncio.run(tabelas_medidas())

        def abrir_tabela_selecionada():
            tabelas.SelectTabela(abrir_tabela_var.get(), 'medidas')
            tabela_atual_var.set(value=abrir_tabela_var.get())
            conjunto_dados['value'] = tabelas.get_TableColumns('medidas')
            asyncio.run(tabelas_medidas())
        
        def add_valor_tabela():
            medida = dados_var.get()
            conjunto_dado = conjunto_dados_var.get()
            conj_dados = ''
            for caractere in conjunto_dado:
                if caractere.isdigit():
                    conj_dados += caractere
            try:
                conjunto_dado = int(conj_dados)
            except:
                tabelas.add_valor_medidas(medida)
            else:
                tabelas.add_valor_medidas(medida,conj_dados)
            conjunto_dados['value'] = tabelas.get_TableColumns('medidas')    
            asyncio.run(tabelas_medidas())
        
        def att_valor_tabela():
            dado_atual = medida_atual_var.get()
            novo_dado = medida_nova_var.get()
            conjunto_dado = conjunto_dados_new_var.get()
            conj_dados = ''
            for caractere in conjunto_dado:
                if caractere.isdigit():
                    conj_dados += caractere
            try:
                conjunto_dado = int(conj_dados)
            except:
                return 'Não foi possível atualizar, coluna inválida.'
            else:
                tabelas.att_valor_medidas(dado_atual, novo_dado, conjunto_dado)
                
            asyncio.run(tabelas_medidas())
        
        async def tabelas_medidas(tabela=None, nome=None):
            importado = 1
            sqlite_table
            if tabela is None or isinstance(tabela, str) or tabela.empty:
                importado = 0
                tabela_desorganizada, tabela = sqlite_table()
                global tabela_df
                global tabela_matriz
                tabela_desorganizada = [dado for dados in tabela_desorganizada for dado in dados] # Cria uma lista com os valores das colunas da tabela
                tabela_matriz = [dado for dado in tabela_desorganizada if dado is not None] # Separa os valores da lista, excluindo os valores Nulos, para matriz
                
                if not isinstance(tabela, DataFrame):
                    tabela_medidas_matrix.destroy()
                    tabela_medidas_matriz()
                    tabela_medidas_format.destroy()
                    tabela_medidas_formatada()
                    tabela_medidas.destroy()
                    tabela_de_medidas()
                    tabela_medidas_tdf.destroy()
                    tabela_df =([],DataFrame([], columns=['', 'Freq. Relativa %']))
                    tabela_tdf()
                    return None
            else:
                tabela_matriz = tabela.to_numpy().tolist()
                tabela_matriz = [dado for dados in tabela_matriz for dado in dados]
                tabela_atual_var.set(value=nome)
            
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
            media_valores = await media(sqlite_table)
            mediana_valores = await mediana(sqlite_table)
            max_valores = await max(sqlite_table)
            min_valores = await min(sqlite_table)
            amplitude_valores = await amplitude(sqlite_table)
            primeiro_quartil_valores = await primeiro_quartil(sqlite_table)
            terceiro_quartil_valores = await terceiro_quartil(sqlite_table)
            iqr_valores = await iqr(sqlite_table)
            corte_inferior_valores = await corte_inferior(sqlite_table)
            corte_superior_valores = await corte_superior(sqlite_table)
            moda_valores = await moda(sqlite_table)
            
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
            tabela_df = await tdf(sqlite_table)
            
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
        
        # Gerar gráfico com matplotlib
        def grafico():
            popup = ttk.Toplevel(self.home)
            histograma = ttk.Button(popup, text='Histograma', command=lambda: Histograma())
            histograma.pack()
            boxplot = ttk.Button(popup, text='BoxPlot', command=lambda: BoxPlot())
            boxplot.pack()
        
        def Histograma():
            color1 = 'royalblue'
            
            fig,ax1 = plt.subplots(figsize=(15,10))

            ax1.set_title('Distribuição de Frequência')

            ax1.set_ylabel('Frequência (%)',color=color1)

            ax1.bar(tabela_df[1][''], tabela_df[1]['Freq. Relativa %'], color=color1, edgecolor='orange', linewidth=2, width=0.99)
            
            ax1.tick_params(axis = 'y', labelcolor = color1)

            for i in ax1.get_xticklabels():
                i.set_rotation(45)
                
            plt.show()
        
        def BoxPlot():
            color1 = 'royalblue'
            
            plt.subplots(figsize=(15,10))
            
            plt.boxplot(tabela_matriz)
            
            plt.xlabel('Eixo X')
            plt.ylabel('Eixo Y')
            plt.title('Boxplot')
            
            plt.show()
        
        def set_tabela():
            self.tabela_medidas = tabela_atual_var.get()
        tabela_atual_var.trace('w', lambda *args: set_tabela())
            
        tabela_medidas_matriz()
        tabela_medidas_formatada()
        tabela_de_medidas()
        tabela_tdf()
        
        return tabelas_medidas
    
    def analise_pareto(self, *args):
        self.pareto(*args)
        if len(args) > 0:
            sql = sqlite.tabela()
            sql.tabela = args[2]
            sql.CriarBD('pareto')
            dados = args[0].to_numpy().tolist()
            for dado in dados:
                try:
                    sql.add_valor_medidas(dado[0])
                except sqlite3.OperationalError as e:
                    print(e)
                    continue
                edit_config.limpar_temp()
            
    def medidas(self, *args):
        asyncio.run(self.medida(*args))
        
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
    
    def fechar_login(self):
        if edit_config.getSecao() == 'False':
            edit_config.apagar_dados()
        edit_config.limpar_temp()
        self.home.destroy()
        self.login.destroy()