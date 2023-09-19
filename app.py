'''Arquivo principal do programa'''

from tkinter import *
import ttkbootstrap as ttk
from telas import telalogin
from data import edit_config

class Tela:
    def __init__(self, janela, titulo):
        self.janela = janela
        self.janela.title(f"{titulo}")
        self.TELA_LARGURA = self.janela.winfo_screenwidth()
        self.TELA_ALTURA = self.janela.winfo_screenheight()

    def centralizarTela(self,largura,altura):
            janela_largura = largura
            janela_altura = altura
            HORIZONTAL = int(self.TELA_LARGURA /2 - janela_largura / 2)
            VERTICAL = int(self.TELA_ALTURA /2 - janela_altura /2)
            
            self.janela.geometry(f'{janela_largura}x{janela_altura}+{HORIZONTAL}+{VERTICAL}')
            
    def menu(self):
        self.menu = Menu(self.janela)
        self.importar_menu = ttk.Menu(self.menu, tearoff=False)
        self.importar_menu.add_command(label = 'Importar CSV', command = lambda: print('alo'))
        self.importar_menu.add_command(label = 'Importar XSLS', command = lambda: print('yes'))
        self.menu.add_cascade(label='Importar', menu = self.importar_menu)
    
class Estilo:
    tema = edit_config.getTema()
    Tfonte = 'Nexa 20'
    fonte = 'Nexa 12'
    Sfonte = 'Nexa 10'
    def __init__(self):
        self.style = ttk.Style(self.tema)
        self.style.configure("TCheckbutton", font=self.Sfonte)
        self.style.configure('Estilo1.info.TButton', font=self.fonte)
        self.style.configure('Estilo1.Link.TButton', font=self.Sfonte)
        self.style.configure('Titulo.TLabel', font=self.Tfonte)
        self.style.configure('Comum.TLabel', font=self.fonte)
        self.style.configure('Pequeno.TLabel', font=self.Sfonte)
        self.style.configure('Estilo2.Link.TButton', font=self.fonte, fg='red')
        # self.style.configure('TEntry', font=self.fonte)

if __name__ == '__main__':
    telalogin.login()