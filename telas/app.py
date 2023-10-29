import ttkbootstrap as ttk
from tkinter import filedialog
from data import edit_config
from bd import tabela_pareto
from telas.telainicial import inicio

class Tela:
    instancia_com_tabela=None
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
        menu_principal = ttk.Menu(self.janela)
        
        arquivo_menu = ttk.Menu(menu_principal, tearoff=False)
        arquivo_menu.add_command(label='Abrir arquivo', command=lambda: print('teste'))
        arquivo_menu.add_command(label='Salvar arquivo', command=lambda: print('teste'))
        arquivo_menu.add_command(label='Salvar Automaticamente', command=lambda: print('teste'))
        
        def apagar_dados():
            if edit_config.getSecao() == 'False':
                edit_config.apagar_dados()
            else:
                pass
        
        arquivo_menu.add_command(label='Sair', command=lambda: (self.janela.destroy(),
                                                                     tela_login.deiconify(),
                                                                     edit_config.apagar_dados()))
        arquivo_menu.add_command(label='Fechar', command=lambda: (self.janela.destroy(),
                                                                       tela_login.destroy(),
                                                                       apagar_dados()))
        
        def import_arquivo(tipo):
            if tipo=='csv':
                arquivo = filedialog.askopenfilename(filetypes=[("CSV", ".csv .txt")])
                csv = tabela_pareto.pareto()
                matplot, tabela = csv.csv(arquivo)
                self.instancia_com_tabela.analise_pareto(tabela=tabela, grafico=matplot)
                
            else:
                arquivo = filedialog.askopenfilename(filetypes=[("Arquivos Excel", ".xlsx .xls")])
        
        importar_menu = ttk.Menu(menu_principal, tearoff=False)
        importar_menu.add_command(label='Importar CSV/TXT', command=lambda: import_arquivo(tipo='csv'))
        importar_menu.add_command(label='Importar arquivo Excel', command=lambda: import_arquivo(tipo='xlsx'))
        
        programa_menu = ttk.Menu(menu_principal, tearoff=False)
        programa_menu.add_command(label='Trocar Tema', command=lambda: self.trocar_tema())
        programa_menu.add_command(label='Versão: 0.3')
        
        menu_principal.add_cascade(label='Arquivo', menu=arquivo_menu)
        menu_principal.add_cascade(label='Importar', menu=importar_menu)
        menu_principal.add_cascade(label='Programa', menu=programa_menu)
        self.janela.config(menu=menu_principal)
        
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