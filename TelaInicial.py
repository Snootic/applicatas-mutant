import tkinter as tk
import ttkbootstrap as tkb
from tkinter import ttk
from tkinter import scrolledtext

#TODO: Tela inicial contendo fields para inserção de dados
# tela para visualização de tabelas
# tela para visualização de gráficos
# botoes/menus para importação de arquivos csv e xsls

home = tkb.Window()
home.geometry('600x400')
home.title("Peraeque - HOME")

#menu
menu = tk.Menu(home)
importar_menu = tk.Menu(menu, tearoff=False)
importar_menu.add_command(label = 'Importar CSV', command = lambda: print('alo'))
importar_menu.add_command(label = 'Importar XSLS', command = lambda: print('yes'))
menu.add_cascade(label='Importar', menu = importar_menu)

#Abas
notebook = tkb.Notebook(home)


#configurações tela
home.configure(menu = menu)

#rodar tela
home.mainloop()