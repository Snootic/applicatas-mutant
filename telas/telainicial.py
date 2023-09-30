from telas.app import *
import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import *
from bd.criar_tabela import *
from bd.analise_pareto_tabela import *
from bd.tabela_sqlite import tabela
import matplotlib.pyplot as plt

#TODO:
# Funcoes de importação de xlsx e csv
# Salvamento de arquivos em tabelas sqlite
# exportacao de arquivos em xlsx e csv


class inicio:
    def __init__(self, login=''):
        self.login = login
        self.home = ttk.Toplevel()
        tela = Tela(self.home, 'Peraeque - Início')
        tela.centralizarTela(900, 600)
        tela.menu()
        
        #Estilo da tela
        colors = self.home.style.colors
        self.estilo = Estilo()
        self.estilo.style.configure('Table.Treeview',font=self.estilo.fonte, rowheight=30)
        self.estilo.style.configure('Table.Treeview.Heading', font=self.estilo.fonte)
        self.estilo.style.configure('custom.TFrame', relief='solid')
        
        
        #Criar uma tabela nova
        criar_tabela_frame = ttk.Frame(
            self.home,
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
            criar_tabela = sql_tabela()
            criar_tabela = criar_tabela.criar_tabela(criar_tabela_var.get())
            criar_tabela_label.configure(text=criar_tabela)
            tabela_atual.configure(text=criar_tabela_var.get())
            analise_pareto()
        
        criar_tabela_entry.pack(padx=(10,5),ipady=5,side=LEFT)
        criar_tabela_botao.pack(padx=(5,10),side=RIGHT)
        criar_tabela_frame.place(relx=0.28, y=40, anchor='center', height=60)
        
        
        #Abrir tabelas já existentes
        tabelas = tabela()
        
        def abrir_tabela_selecionada():
            tabelas.SelectTabela(abrir_tabela_var.get())
            analise_pareto()
            tabela_atual.configure(text=abrir_tabela_var.get())
        
        abrir_tabela_frame = ttk.Frame(
            self.home,
            width=500,
            height=200)
    
        abrir_tabela_var = ttk.StringVar(value='Abrir uma tabela')
        abrir_tabela = ttk.Combobox(abrir_tabela_frame,
                                    width=30,
                                    textvariable=abrir_tabela_var,
                                    font=self.estilo.fonte)
        
        abrir_tabela['value'] = tabelas.getTabelas()
        
        abrir_tabela_btn = ttk.Button(abrir_tabela_frame,
                                      text='Abrir',
                                      style='Estilo1.TButton',
                                      command=abrir_tabela_selecionada)
        
        abrir_tabela_btn.pack(side=RIGHT,padx=5)
        abrir_tabela.pack(side=LEFT,padx=5)
        abrir_tabela_frame.place(relx=0.75,y=25, anchor='center')
        
        #Adicionar ocorrencias na tabela aberta
        
        def adicionar_itens_funcao():
            tabelas.addValor(adicionar_itens_var.get(), quantidade=quantidade_ocorrencia_var.get())
            analise_pareto()
        
        adicionar_itens_frame = ttk.Frame(self.home, style='custom.TFrame')
        adicionar_itens_frame.place(relx=0.245, y=520, anchor=CENTER,height=100,width=430)
        
        adicionar_itens_var = ttk.StringVar(value='Ocorrência')
        adicionar_itens = ttk.Entry(adicionar_itens_frame,
                                    textvariable=adicionar_itens_var,
                                    width=30,
                                    font=self.estilo.fonte)
        adicionar_itens.place(relx=0.03,y=10)
        
        quantidade_ocorrencia_var = ttk.IntVar()
        quantidade_ocorrencia = ttk.Spinbox(adicionar_itens_frame,
                                            textvariable=quantidade_ocorrencia_var,
                                            width=10,
                                            from_=1,
                                            to=10000)
        quantidade_ocorrencia.place(relx=0.72,y=10)
        
        adicionar_itens_plus = ttk.Button(adicionar_itens_frame,
                                          text= 'Adicionar',
                                          width=10,
                                          style='Estilo1.TButton',
                                          command=adicionar_itens_funcao)
        adicionar_itens_plus.place(relx=0.37,y=60)
        
        # Atualizar ocorrencia
        def atualizar_itens_funcao():
            tabelas.atualizar_ocorrencia(ocorrencia_atual_var.get(),ocorrencia_nova_var.get())
            analise_pareto()
        
        atualizar_itens_frame = ttk.Frame(self.home, style='custom.TFrame')
        atualizar_itens_frame.place(relx=0.75, y=520, anchor=CENTER,height=100,width=430)
        
        ocorrencia_atual_var = ttk.StringVar(value='Ocorrência atual')
        ocorrencia_atual = ttk.Entry(atualizar_itens_frame,
                                    textvariable=ocorrencia_atual_var,
                                    width=30,
                                    font=self.estilo.fonte)
        ocorrencia_atual.place(relx=0.03,y=10)
        
        ocorrencia_quantidade_var = ttk.IntVar()
        ocorrencia_quantidade = ttk.Spinbox(atualizar_itens_frame,
                                            textvariable=ocorrencia_quantidade_var,
                                            width=10,
                                            from_=1,
                                            to=10000)
        ocorrencia_quantidade.place(relx=0.72,y=10)
        
        ocorrencia_nova_var = ttk.StringVar(value='Nova ocorrência')
        ocorrencia_nova = ttk.Entry(atualizar_itens_frame,
                                    textvariable=ocorrencia_nova_var,
                                    width=30,
                                    font=self.estilo.fonte)
        ocorrencia_nova.place(relx=0.03,y=50)
        
        
        atualizar_itens_plus = ttk.Button(atualizar_itens_frame,
                                          text= 'Atualizar',
                                          width=9,
                                          style='Estilo1.TButton',
                                          command=atualizar_itens_funcao)
        atualizar_itens_plus.place(relx=0.72,y=50)
        
        
        # Display tabela atual
        tabela_atual = ttk.Label(self.home,text='SELECIONE UMA TABELA',style='Titulo.TLabel')
        tabela_atual.place(relx=0.5,y=100,anchor=CENTER)
        
        #Pegar dados para criar tabela análise de pareto
        sqlite = pareto()
        def analise_pareto():
            global matplot
            matplot, DataFrame=sqlite.sqlite()
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
            tabela_analise_pareto()
            pareto_tabela.insert_rows(index = 'end', rowdata = dados)
            pareto_tabela.load_table_data()
        
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
        
        gerar_grafico = ttk.Button(self.home,text='Gerar gráfico',style='Estilo1.TButton', command=grafico)
        gerar_grafico.place(relx=0.75,y=65,anchor=CENTER)
        
        #Tabela da análise de pareto
        def tabela_analise_pareto():
            global pareto_tabela
            pareto_tabela = Tableview(
                self.home,
                coldata=[{"text": "Ocorrências", "stretch": True, "width": 200},
                        {"text": "No. Ocorrências", "stretch": True, "width": 200},
                        {"text": "Freq. Relativa", "stretch": True, "width": 200},
                        {"text": "Freq. Acumulada", "stretch": True, "width": 200}
                        ],
                rowdata=[],
                autofit=True,
                autoalign=False,
                stripecolor=(colors.active, None)
            )
            pareto_tabela.place(relx=0.5,y=290,anchor=CENTER, width=900)
        
        tabela_analise_pareto()
        
        self.home.protocol("WM_DELETE_WINDOW", self.fechar_login)
        
        self.home.mainloop()
        
    def fechar_login(self):
        self.home.destroy()
        self.login.destroy()