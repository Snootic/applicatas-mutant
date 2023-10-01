import ttkbootstrap as ttk
import asyncio
from data import edit_config

class Tela:
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
    
    def trocar_tema(self):
        if tela_login.style.theme.type == 'dark':
            tela_login.style.theme_use("journal")
            edit_config.editTema('journal')
            Estilo.tema = 'journal'
        else:
            tela_login.style.theme_use("cyborg")
            edit_config.editTema('cyborg')
            Estilo.tema = 'cyborg'
        
        estilo = Estilo()

    def menu(self):
        self.menu_principal = ttk.Menu(self.janela)
        
        self.arquivo_menu = ttk.Menu(self.menu_principal, tearoff=False)
        self.arquivo_menu.add_command(label='Abrir arquivo', command=lambda: print('teste'))
        self.arquivo_menu.add_command(label='Salvar arquivo', command=lambda: print('teste'))
        self.arquivo_menu.add_command(label='Salvar Automaticamente', command=lambda: print('teste'))
        self.arquivo_menu.add_command(label='Sair', command=lambda: (self.janela.destroy(),
                                                                     tela_login.deiconify(),
                                                                     edit_config.apagar_dados()))
        self.arquivo_menu.add_command(label='Fechar', command=lambda: (self.janela.destroy(),
                                                                       tela_login.destroy(),
                                                                       edit_config.apagar_dados()))
        
        self.importar_menu = ttk.Menu(self.menu_principal, tearoff=False)
        self.importar_menu.add_command(label='Importar CSV', command=lambda: print('alo'))
        self.importar_menu.add_command(label='Importar XSLS', command=lambda: print('yes'))
        
        self.programa_menu = ttk.Menu(self.menu_principal, tearoff=False)
        self.programa_menu.add_command(label='Trocar Tema', command=lambda: self.trocar_tema())
        self.programa_menu.add_command(label='Versão: 0.1')
        
        self.menu_principal.add_cascade(label='Arquivo', menu=self.arquivo_menu)
        self.menu_principal.add_cascade(label='Importar', menu=self.importar_menu)
        self.menu_principal.add_cascade(label='Programa', menu=self.programa_menu)
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
                            focuscolor=cores.colors.primary,
                            foreground=cores.colors.primary,)
        self.style.configure('Estilo2.Link.TButton', font=self.fonte,
                             focuscolor=cores.colors.primary,
                             foreground=cores.colors.primary,
                             )
        self.style.configure('Titulo.TLabel', font=self.Tfonte, foreground=cores.colors.info)
        self.style.configure('Comum.TLabel', font=self.fonte)
        self.style.configure('Pequeno.TLabel', font=self.Sfonte)
        self.style.configure('TCombobox', font=self.fonte)
        self.style.configure('Table.Treeview',font=self.fonte, rowheight=30)
        self.style.configure('Table.Treeview.Heading', font=self.fonte)
        self.style.configure('custom.TFrame', relief='solid')
        
class centralizar_widget:
    def __init__(self, tela, widget):
        tela = Tela(janela=tela)
        self.x = ((tela.TELA_LARGURA - widget.winfo_width()) // 2)
        self.y = ((tela.TELA_ALTURA - widget.winfo_height()) // 2) 