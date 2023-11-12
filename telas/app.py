import ttkbootstrap as ttk
from tkinter import filedialog
from data import edit_config
from bd import tabela_pareto, medidas, sqlite
from telas.telainicial import inicio
import os, asyncio

class Tela:
    instancia_com_tabela=None
    aba_atual = None
    def __init__(self, janela='', titulo=''):
        self.janela = janela
        self.janela.title(titulo)
        icone_caminho= os.path.abspath('data/icone.png')
        self.janela.iconphoto(False, ttk.PhotoImage(file=icone_caminho))
        
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
        
        def undoRedo(do):
            sql = sqlite.tabela()
            dados = 'pareto' if self.aba_atual == 0 else 'medidas'
            if do == 'undo':
                sql.restore(dados=dados, redo=False)
                
            elif do == 'redo':
                sql.restore(dados=dados, redo=True)
            
            if dados == 'pareto':
                self.instancia_com_tabela.analise_pareto()
            else:
                self.instancia_com_tabela.medidas()
                
        arquivo_menu = ttk.Menu(menu_principal, tearoff=False)
        arquivo_menu.add_command(label='Abrir arquivo', command=lambda: print('teste'))
        arquivo_menu.add_command(label='Salvar arquivo', command=lambda: print('teste'))
        arquivo_menu.add_command(label='Salvar Automaticamente', command=lambda: print('teste'))
        arquivo_menu.add_command(label='Desfazer', command=lambda: undoRedo('undo'))
        arquivo_menu.add_command(label='Refazer', command=lambda: undoRedo('redo'))
        
        def apagar_dados():
            if edit_config.getSecao() == 'False':
                edit_config.apagar_dados()
            sql = sqlite.tabela()
            tabelas_pareto = sql.getTabelas('pareto')
            tabelas_medidas = sql.getTabelas('medidas')
            
            for tabela in tabelas_pareto:
                if tabela[0].split('_')[-1] == 'temp':
                    sql.DropTable(tabela[0],'pareto')
                    
            for tabela in tabelas_medidas:
                if tabela[0].split('_')[-1] == 'temp':
                    sql.DropTable(tabela[0],'medidas')
                    
            edit_config.limpar_temp()
        
        arquivo_menu.add_command(label='Sair', command=lambda: (self.janela.destroy(),
                                                                     tela_login.deiconify(),
                                                                     edit_config.apagar_dados()))
        arquivo_menu.add_command(label='Fechar', command=lambda: (self.janela.destroy(),
                                                                       tela_login.destroy(),
                                                                       apagar_dados()))
        
        def import_arquivo(tipo):
            if tipo=='csv':
                arquivo = filedialog.askopenfilename(filetypes=[("CSV", ".csv .txt")])
                nome = arquivo.split("/")[-1]
                nome = nome.split('.')[0]
                nome = f'{nome}_temp'
                
                if self.aba_atual == None or self.aba_atual == 0:
                    csv = tabela_pareto.pareto()
                    matplot, tabela = csv.csv(arquivo)
                    self.instancia_com_tabela.analise_pareto(tabela, matplot, nome)
                
                elif self.aba_atual == 1:
                    csv = asyncio.run(medidas.imports(arquivo, 'csv', nome))
                    self.instancia_com_tabela.medidas(csv,nome)
            elif tipo == 'xlsx':
                arquivo = filedialog.askopenfilename(filetypes=[("Arquivos Excel", ".xlsx .xls")])
                nome = arquivo.split("/")[-1]
                nome = nome.split('.')[0]
                nome = f'{nome}_temp'
                
                if self.aba_atual == 0:
                    pass
                
                elif self.aba_atual == 1:
                    excel = asyncio.run(medidas.imports(arquivo, 'xlsx', nome))
                    self.instancia_com_tabela.medidas(excel,nome)
        
        importar_menu = ttk.Menu(menu_principal, tearoff=False)
        importar_menu.add_command(label='Importar CSV/TXT', command=lambda: import_arquivo(tipo='csv'))
        importar_menu.add_command(label='Importar arquivo Excel', command=lambda: import_arquivo(tipo='xlsx'))
        
        def export_arquivo(tipo):
            dados = 'pareto' if self.aba_atual == 0 else 'medidas'
            if tipo == 'csv':
                arquivo = filedialog.asksaveasfilename(confirmoverwrite=True,
                                                       defaultextension='.csv',
                                                       filetypes=[("CSV", ".csv")])
                self.instancia_com_tabela.exportar(arquivo, 'csv' ,dados)
            else:
                arquivo = filedialog.asksaveasfilename(confirmoverwrite=True,
                                                       defaultextension='.xlsx',
                                                       filetypes=[("Arquivos Excel", ".xlsx")])
                self.instancia_com_tabela.exportar(arquivo, 'xlsx' ,dados)
        
        exportar_menu = ttk.Menu(menu_principal, tearoff=False)
        exportar_menu.add_command(label='Exportar - CSV', command=lambda: export_arquivo(tipo='csv'))
        exportar_menu.add_command(label='Exportar - Excel', command=lambda: export_arquivo(tipo='xlsx'))
        
        programa_menu = ttk.Menu(menu_principal, tearoff=False)
        programa_menu.add_command(label='Trocar Tema', command=lambda: self.trocar_tema())
        version = os.path.abspath('VERSION')
        with open(version, 'r') as version:
            versao = version.readlines()
            versao = versao[0]
        programa_menu.add_command(label=f'Versão: {versao}')
        
        menu_principal.add_cascade(label='Arquivo', menu=arquivo_menu)
        menu_principal.add_cascade(label='Importar', menu=importar_menu)
        menu_principal.add_cascade(label='Exportar', menu=exportar_menu)
        menu_principal.add_cascade(label='Programa', menu=programa_menu)
        self.janela.config(menu=menu_principal)
        
class Estilo:
    tema = edit_config.getTema()
    Tfonte = 'Nexa 16'
    fonte = 'Nexa 10'
    Sfonte = 'Nexa 8'
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