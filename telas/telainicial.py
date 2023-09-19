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

        #menu
        menu = ttk.Menu(home)
        importar_menu = ttk.Menu(menu, tearoff=False)
        importar_menu.add_command(label = 'Importar CSV', command = lambda: print('alo'))
        importar_menu.add_command(label = 'Importar XSLS', command = lambda: print('yes'))
        menu.add_cascade(label='Importar', menu = importar_menu)

        botao2 = ttk.Button(home, text='Botao1',)
        botao3 = Button(home, text='Botao2')
        botao2.pack()
        botao3.pack()
        
        #Abas
        notebook = ttk.Notebook(home)


        #configurações tela
        home.configure(menu = menu)

        #rodar tela
        home.mainloop()
        
tela = inicio()