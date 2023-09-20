from tkinter import *
import ttkbootstrap as ttk

#TODO: Tela inicial contendo fields para inserção de dados
# tela para visualização de tabelas
# tela para visualização de gráficos
# botoes/menus para importação de arquivos csv e xsls
# Integrar funções de tabela


class inicio:
    def __init__(self) -> None:
        home = ttk.Window(themename='darkly')
        home.geometry('600x400')
        home.title("Peraeque - HOME")
        #rodar tela
        home.mainloop()