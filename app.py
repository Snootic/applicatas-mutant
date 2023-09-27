'''Arquivo principal do programa'''

# from tkinter import *
import ttkbootstrap as ttk
from data import edit_config

class Tela:
    tela_login = ''
    def __init__(self, janela='', titulo=''):
        self.janela = janela
        self.janela.title(titulo)
        
        if (self.janela.title()) == 'Peraeque - Login':
            global tela_login
            tela_login = self.janela

        self.TELA_LARGURA = self.janela.winfo_screenwidth()
        self.TELA_ALTURA = self.janela.winfo_screenheight()

    def centralizarTela(self,largura,altura):
            janela_largura = largura
            janela_altura = altura
            MONITOR_HORIZONTAL = int(self.TELA_LARGURA /2 - janela_largura / 2)
            MONITOR_VERTICAL = int(self.TELA_ALTURA /2 - janela_altura /2)
            
            self.janela.geometry(f'{janela_largura}x{janela_altura}+{MONITOR_HORIZONTAL}+{MONITOR_VERTICAL}')
            
    def menu(self):
        self.menu_principal = ttk.Menu(self.janela)
        
        self.arquivo_menu = ttk.Menu(self.menu_principal, tearoff=False)
        self.arquivo_menu.add_command(label='Abrir arquivo', command=lambda: print('pinto'))
        self.arquivo_menu.add_command(label='Salvar arquivo', command=lambda: print('pinto'))
        self.arquivo_menu.add_command(label='Salvar Automaticamente', command=lambda: print('pinto'))
        self.arquivo_menu.add_command(label='Sair', command=lambda: (self.janela.destroy(), tela_login.deiconify()))
        self.arquivo_menu.add_command(label='Fechar', command=lambda: (self.janela.destroy(), tela_login.destroy()))
        
        self.importar_menu = ttk.Menu(self.menu_principal, tearoff=False)
        self.importar_menu.add_command(label='Importar CSV', command=lambda: print('alo'))
        self.importar_menu.add_command(label='Importar XSLS', command=lambda: print('yes'))
        
        self.menu_principal.add_cascade(label='Arquivo', menu=self.arquivo_menu)
        self.menu_principal.add_cascade(label='Importar', menu=self.importar_menu)
        self.janela.config(menu=self.menu_principal)
        
class Estilo:
    tema = edit_config.getTema()
    Tfonte = 'Nexa 20'
    fonte = 'Nexa 12'
    Sfonte = 'Nexa 10'
    def __init__(self):
        self.style = ttk.Style(self.tema)
        cores = self.style._theme_definitions.get(self.tema)
        self.style.configure('.', f=self.fonte)
        self.style.configure("TCheckbutton", font=self.Sfonte)
        self.style.configure('Estilo1.TButton', font=self.fonte)
        self.style.configure('Estilo1.info.TButton', font=self.fonte)
        self.style.configure('Estilo1.Link.TButton', font=self.Sfonte,
                            focuscolor=cores.colors.warning,
                            foreground=cores.colors.warning,)
        self.style.configure('Estilo2.Link.TButton', font=self.fonte,
                             focuscolor=cores.colors.warning,
                             foreground=cores.colors.warning,
                             )
        self.style.configure('Titulo.TLabel', font=self.Tfonte, foreground=cores.colors.info)
        self.style.configure('Comum.TLabel', font=self.fonte)
        self.style.configure('Pequeno.TLabel', font=self.Sfonte)
class centralizar_widget:
    def __init__(self, tela, widget):
        tela = Tela(janela=tela)
        self.x = ((tela.TELA_LARGURA - widget.winfo_width()) // 2)
        self.y = ((tela.TELA_ALTURA - widget.winfo_height()) // 2) 