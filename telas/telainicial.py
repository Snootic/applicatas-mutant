from telas import app
from tkinter import *
import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import *
from bd.tabela_pareto import *
from bd.sqlite import tabela
import matplotlib.pyplot as plt

#TODO:
# Funcoes de importação de xlsx
# Salvamento de arquivos em tabelas sqlite
# exportacao de arquivos em xlsx e csv
# adicionar custo em tabelas com zero dados e tabelas com custo ja adicionado
# notebook
# melhorar layout dos botoes para caber o resto que precisa ser adicionado e o notebook futuramente

# TRATAMENTO DE ERROS E RETORNO VISUAL PARA O USUARIO COM POPUPS - URGENTE


class inicio:
    def __init__(self, login=''):
        self.login = login
        self.home = ttk.Toplevel()
        tela = app.Tela(self.home, 'Peraeque - Início')
        tela.centralizarTela(900, 600)
        tela.menu()
        tela.instancia_com_tabela = self
        
        #Estilo da tela
        colors = self.login.style.colors
        self.estilo = app.Estilo()
        
        #notebook
        notebook = ttk.Notebook(self.home)
        notebook.pack(expand=True)
        
        tela_pareto = ttk.Frame(notebook, width=900, height=600)
        tela_pareto.pack(fill='both', expand=True)
        tela_medidas = ttk.Frame(notebook, width=900, height=600)
        tela_medidas.pack(fill='both',expand=True)
        
        notebook.add(tela_pareto, text='Pareto')
        notebook.add(tela_medidas, text='Medidas')
        
        self.tela_pareto(tela_pareto)
        # self.tela_medidas(tela_medidas)
        
        self.home.protocol("WM_DELETE_WINDOW", self.fechar_login)
        
        self.home.mainloop()   
        
    def tela_pareto(self, tela): 
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
            pareto_tabela.place(relx=0.5,y=275,anchor=CENTER, width=900)
        
        def analise_pareto(tabela=None, grafico=None):
            global matplot
            if tabela is not None and not tabela.empty:
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
        
        
        #Criar uma tabela nova
        criar_tabela_frame = ttk.Frame(
            tela,
            style='custom.TFrame',
            width=500,
            height=200)
        
        criar_tabela_var = ttk.StringVar(value='Criar nova Tabela')
        criar_tabela_entry = ttk.Entry(
            criar_tabela_frame,
            textvariable=criar_tabela_var,
            width=30,
            font=self.estilo.fonte)
        criar_tabela_entry.bind(
            '<FocusIn>',
            lambda event: (criar_tabela_var.set(value=''),
                           criar_tabela_entry.unbind('<FocusIn>')))
        
        criar_tabela_botao = ttk.Button(
            criar_tabela_frame,
            text='Criar',
            style='Estilo1.TButton',
            command=lambda: criar_tabela()
        )
        
        criar_tabela_label = ttk.Label(
            criar_tabela_frame,
            style='Comum.TLabel',
            text='TESTE'
        )
        
        def criar_tabela():
            criar_tabela = tabela(criar_tabela_var.get())
            criar_tabela = criar_tabela.CriarBD('pareto')
            criar_tabela_label.configure(text=criar_tabela)
            tabela_atual_var.set(value=criar_tabela_var.get())
            analise_pareto()
        
        criar_tabela_entry.pack(padx=(10,5),ipady=5,side=LEFT)
        criar_tabela_botao.pack(padx=(5,10),side=RIGHT)
        criar_tabela_frame.place(x=240, y=40, anchor='center', height=60)
        
        
        #Abrir tabelas já existentes
        tabelas = tabela()
        
        def abrir_tabela_selecionada():
            tabelas.SelectTabela(abrir_tabela_var.get(), 'pareto')
            analise_pareto()
            tabela_atual_var.set(value=abrir_tabela_var.get())
        
        abrir_tabela_frame = ttk.Frame(
            tela,
            width=500,
            height=200)
    
        abrir_tabela_var = ttk.StringVar(value='Abrir uma tabela')
        abrir_tabela = ttk.Combobox(abrir_tabela_frame,
                                    width=30,
                                    textvariable=abrir_tabela_var,
                                    font=self.estilo.fonte)
        
        abrir_tabela['value'] = tabelas.getTabelas('pareto')
        
        abrir_tabela_btn = ttk.Button(abrir_tabela_frame,
                                      text='Abrir',
                                      style='Estilo1.TButton',
                                      command=abrir_tabela_selecionada)
        
        abrir_tabela_btn.pack(side=RIGHT,padx=5)
        abrir_tabela.pack(side=LEFT,padx=5)
        abrir_tabela_frame.place(x=670,y=25, anchor='center')
        
        #Adicionar ocorrencias na tabela aberta
        
        def adicionar_itens_funcao():
            custo = adicionar_custo_var.get()
            try:
                float(custo)
                tabelas.addValor_pareto(adicionar_itens_var.get(), quantidade=quantidade_ocorrencia_var.get(), custo=custo)
            except:
                tabelas.addValor_pareto(adicionar_itens_var.get(), quantidade=quantidade_ocorrencia_var.get())
            analise_pareto()
        
        adicionar_itens_frame = ttk.Frame(tela, style='custom.TFrame')
        adicionar_itens_frame.place(x=225, y=510, anchor=CENTER,height=100,width=430)
        
        adicionar_itens_var = ttk.StringVar(value='Ocorrência')
        adicionar_itens = ttk.Entry(adicionar_itens_frame,
                                    textvariable=adicionar_itens_var,
                                    width=30,
                                    font=self.estilo.fonte)
        adicionar_itens.place(x=13,y=10)
        adicionar_itens.bind(
            '<FocusIn>',
            lambda event: (adicionar_itens_var.set(value=''),
                           adicionar_itens.unbind('<FocusIn>')))
        
        adicionar_custo_var = ttk.StringVar(value='Custo Unitário')
        adicionar_custo = ttk.Entry(adicionar_itens_frame,
                                    textvariable=adicionar_custo_var,
                                    width=30,
                                    font=self.estilo.fonte)
        adicionar_custo.place(x=13, y=50)
        adicionar_custo.bind(
            '<FocusIn>',
            lambda event: (adicionar_custo_var.set(value=''),
                           adicionar_custo.unbind('<FocusIn>')))
        adicionar_custo.configure(state="disabled")
        
        def bloquear_entrys():
            if len(pareto_tabela.get_rows()) < 1 or len(pareto_tabela.get_columns()) == 6:
                adicionar_custo.configure(state='normal')
            else:
                adicionar_custo.configure(state="disabled")
                    
        quantidade_ocorrencia_var = ttk.IntVar(value=1)
        quantidade_ocorrencia = ttk.Spinbox(adicionar_itens_frame,
                                            textvariable=quantidade_ocorrencia_var,
                                            width=10,
                                            from_=1,
                                            to=10000)
        quantidade_ocorrencia.place(x=310,y=10)
        
        adicionar_itens_plus = ttk.Button(adicionar_itens_frame,
                                          text= 'Adicionar',
                                          width=9,
                                          style='Estilo1.TButton',
                                          command=adicionar_itens_funcao)
        adicionar_itens_plus.place(x=311,y=50)
        
        # Atualizar ocorrencia
        def atualizar_itens_funcao():
            tabelas.atualizar_ocorrencia(ocorrencia_atual_var.get(),ocorrencia_nova_var.get(),ocorrencia_quantidade_var.get())
            analise_pareto()
        
        atualizar_itens_frame = ttk.Frame(tela, style='custom.TFrame')
        atualizar_itens_frame.place(x=670, y=510, anchor=CENTER,height=100,width=430)
        
        ocorrencia_atual_var = ttk.StringVar(value='Ocorrência atual')
        ocorrencia_atual = ttk.Entry(atualizar_itens_frame,
                                    textvariable=ocorrencia_atual_var,
                                    width=30,
                                    font=self.estilo.fonte)
        ocorrencia_atual.place(x=13,y=10)
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
        ocorrencia_quantidade.place(x=310,y=10)
        
        ocorrencia_nova_var = ttk.StringVar(value='Nova ocorrência')
        ocorrencia_nova = ttk.Entry(atualizar_itens_frame,
                                    textvariable=ocorrencia_nova_var,
                                    width=30,
                                    font=self.estilo.fonte)
        ocorrencia_nova.bind(
            '<FocusIn>',
            lambda event: (ocorrencia_nova_var.set(value=''),
                           ocorrencia_nova.unbind('<FocusIn>')))
        ocorrencia_nova.place(x=13, y=50)
        
        
        atualizar_itens_plus = ttk.Button(atualizar_itens_frame,
                                          text= 'Atualizar',
                                          width=9,
                                          style='Estilo1.TButton',
                                          command=atualizar_itens_funcao)
        atualizar_itens_plus.place(x=311,y=50)
        
        # Display tabela atual
        tabela_atual_var = StringVar(value='SELECIONE UMA TABELA')
        tabela_atual = ttk.Label(tela,textvariable=tabela_atual_var,style='Titulo.TLabel')
        tabela_atual.lower()
        tabela_atual.place(relx=0.5,y=85,anchor=CENTER)
        tabela_atual_var.trace("w", lambda *args: bloquear_entrys())
        
        # Gerar gráfico com matplotlib
        def grafico():
            
            color1 = 'royalblue'
            color2 = 'black'

            fig,ax1 = plt.subplots(figsize=(15,10))

            ax1.set_title('Pareto')

            ax1.set_ylabel('Frequência (%)',color=color1)

            ax1.bar(matplot['Ocorrências'], matplot['Freq. Relativa'], color=color1, edgecolor='orange', linewidth=2)

            ax1.tick_params(axis = 'y', labelcolor = color1)

            ax2 = ax1.twinx()
            ax2.set_ylabel('%', color=color2)

            ax2.plot(matplot['Ocorrências'], matplot['Freq. Acumulada'], color = color2, marker = 's', markersize = 8, linestyle = '-')

            ax2.tick_params(axis='y',labelcolor=color2)
            ax2.set_ylim([0,120])

            for i in ax1.get_xticklabels():
                i.set_rotation(45)
            plt.show()
        
        gerar_grafico = ttk.Button(tela,text='Gerar gráfico',style='Estilo1.TButton', command=grafico)
        gerar_grafico.place(x=795,y=65,anchor=CENTER)
    
        tabela_analise_pareto()
        
    def tela_medidas(self, tela):
        pass

    def fechar_login(self):
        if edit_config.getSecao() == 'False':
            edit_config.apagar_dados()
        self.home.destroy()
        self.login.destroy()