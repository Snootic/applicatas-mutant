from tkinter import *
import ttkbootstrap as ttk
from app import *

#TODO: Tela inicial contendo fields para inserção de dados
# tela para visualização de tabelas
# tela para visualização de gráficos
# botoes/menus para importação de arquivos csv e xsls
# Integrar funções de tabela


class inicio:
    def __init__(self, login):
        self.login = login
        self.home = ttk.Window()
        tela = Tela(self.home, 'Peraeque - Início')
        tela.centralizarTela(900, 600)
        tela.menu()
        
        self.estilo = Estilo()
        
        self.home.protocol("WM_DELETE_WINDOW", self.fechar_login)
        
        self.home.mainloop()
        
    def fechar_login(self):
        self.home.destroy()
        self.login.destroy()