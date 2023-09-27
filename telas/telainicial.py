# from tkinter import *
from app import *
import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import *
from bd.criar_tabela import *
from bd.analise_pareto_tabela import *

#TODO: Tela inicial contendo fields para inserção de dados
# tela para visualização de tabelas
# tela para visualização de gráficos
# botoes/menus para importação de arquivos csv e xsls
# Integrar funções de tabela


class inicio:
    def __init__(self, login=''):
        self.login = login
        self.home = ttk.Toplevel()
        tela = Tela(self.home, 'Peraeque - Início')
        tela.centralizarTela(900, 600)
        tela.menu()
        
        Frame_geral = ttk.Frame(self.home)
        
        colors = self.home.style.colors
        self.estilo = Estilo()
        self.estilo.style.configure('Table.Treeview',font=self.estilo.fonte, rowheight=30)
        self.estilo.style.configure('Table.Treeview.Heading', font=self.estilo.fonte)
        self.estilo.style.configure('custom.TFrame', relief='solid')
        
        criar_tabela_frame = ttk.Frame(
            Frame_geral,
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
        
        criar_tabela_entry.pack(padx=(10,0),ipady=5,side=LEFT)
        criar_tabela_botao.pack(padx=(0,10),side=RIGHT)
        criar_tabela_label.pack(side=BOTTOM,pady=10)
        criar_tabela_frame.pack(ipadx=5, ipady=15, pady=10)
        
        tabela_atual = ttk.Label(Frame_geral,text=f'tabela',style='Titulo.TLabel')
        tabela_atual.pack()
        
        sqlite = pareto()
        DataFrame=sqlite.sqlite()
        colunas=list(DataFrame)
        colunas_novas = []
        for item in colunas:
            if isinstance(item, str):
                dicionario = {"text": item, "stretch": True, "width": 120}
            elif isinstance(item, dict):
                dicionario = item
            colunas_novas.append(dicionario)
            
        dados=DataFrame.to_numpy().tolist()
        
        pareto_tabela = Tableview(
            Frame_geral,
            coldata=colunas_novas,
            rowdata=dados,
            autofit=True,
            autoalign=False,
            stripecolor=(colors.active, None)
        )
        pareto_tabela.pack(ipadx=25)
        pareto_tabela.bind("<Return>", lambda e: print('opa'))
        
        self.home.protocol("WM_DELETE_WINDOW", self.fechar_login)
        
        Frame_geral.pack(fill=BOTH)
        
        self.home.mainloop()
        
    def fechar_login(self):
        self.home.destroy()
        self.login.destroy()