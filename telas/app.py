import ttkbootstrap as ttk
from ttkbootstrap import dialogs
from tkinter import filedialog
from data import edit_config
from bd import tabela_pareto, medidas, sqlite, save
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
            '''
                Do Undo and Redo of changes. 
                do: accepts 'undo' and 'redo'
            '''
            sql = sqlite.tabela()
            dados = 'pareto' if self.aba_atual == 0 else 'medidas'
            if do == 'undo':
                sql.restore(dados=dados, redo=False)
                
            elif do == 'redo':
                sql.restore(dados=dados, redo=True)
            
            if dados == 'pareto':
                self.instancia_com_tabela.analise_pareto()
            elif dados == 'medidas':
                self.instancia_com_tabela.medidas()
        
        def manual_backup(do):
            '''
                Manual Backup of changes. Calls filedialog, sqlite dump and restore functions.
                do: accepts 'save' and 'restore'
            '''
            sql = sqlite.tabela()
            dados = 'pareto' if self.aba_atual == 0 else 'medidas'
            
            if do == 'save':
                if self.aba_atual == 0:
                    tabela = self.instancia_com_tabela.tabela_pareto()
                elif self.aba_atual == 1:
                    tabela = self.instancia_com_tabela.tabela_medidas()
                    
                arquivo = filedialog.asksaveasfilename(confirmoverwrite=True,
                                        defaultextension='.sql',
                                        filetypes=[("SQL script file", ".sql")])
                sql.dump(manual=True, dados=dados, path=arquivo, tabela=tabela)
            elif do == 'restore':
                arquivo = filedialog.askopenfilename(filetypes=[("SQL script file", ".sql")])
                
                def restaurar():
                    sql.restore(manual=True, dados=dados, file=arquivo)
                    if self.aba_atual == 0:
                        self.instancia_com_tabela.analise_pareto()
                    elif self.aba_atual == 1:
                        self.instancia_com_tabela.medidas()
                        
                with open(arquivo, 'r', encoding='utf-8') as file:
                    lines = file.readlines()
                    tabela = lines[1].split(' ')
                    tabela = tabela[-1].split('(')[0]
                
                tabelas = sql.getTabelas(dados)
                for i in tabelas:
                    if tabela in i:
                        substituir = dialogs.MessageDialog(parent=self.instancia_com_tabela.home,
                                                           title="Tabela já existente",
                                                           message=f"A tabela '{tabela}' já existe.\n Deseja substituí-la?",
                                                           buttons=["Sim:danger",
                                                                    "Cancelar:primary"],
                                                           alert=True)
                        substituir.show()
                
                try:
                    if substituir.result != 'Sim':
                        return
                    else:
                        restaurar()
                except UnboundLocalError:
                    restaurar()
                    
        def salvar(do):
            saves = save.Salvar()
            if do == 'save':
                edit_config.setIsSaved(True)
                saves.save()
                
            elif do == 'autosave':
                is_saved = edit_config.getAutoSave()
                if is_saved == 'True':
                    edit_config.setAutoSave(False)
                else:
                    edit_config.setAutoSave(True)
               
        arquivo_menu = ttk.Menu(menu_principal, tearoff=False)
        arquivo_menu.add_command(label='Restaurar Backup', command=lambda: manual_backup(do='restore'))
        arquivo_menu.add_command(label='Salvar Backup', command=lambda: manual_backup(do='save'))
        arquivo_menu.add_command(label='Salvar arquivo', command=lambda: salvar('save'))
        arquivo_menu.add_command(label='Salvar Automaticamente', command=lambda: salvar('autosave'))
        arquivo_menu.add_command(label='Desfazer', command=lambda: undoRedo('undo'))
        arquivo_menu.add_command(label='Refazer', command=lambda: undoRedo('redo'))
        
        def apagar_dados(command=''):
            sql = sqlite.tabela()
            tabelas_pareto = sql.getTabelas('pareto')
            tabelas_medidas = sql.getTabelas('medidas')
            
            for tabela in tabelas_pareto:
                if tabela[0].split('_')[-1] == 'temp':
                    sql.DropTable(tabela[0],'pareto')
                    
            for tabela in tabelas_medidas:
                if tabela[0].split('_')[-1] == 'temp':
                    sql.DropTable(tabela[0],'medidas')
                    
            if edit_config.getSecao() == 'False' or command == 'Sair':
                edit_config.apagar_dados()
            
            edit_config.setIsSaved(True)
            edit_config.limpar_temp()
        
        def checkSave(command):
            '''
                Checa se o arquivo foi salvo ao fechar o programa. Se não, pergunta se o usuário deseja salvar.
            '''
            is_saved = edit_config.getIsSaved()
            if is_saved == 'True':
                if command == 'Fechar':
                        apagar_dados()
                        tela_login.destroy()
                elif command == 'Sair':
                    apagar_dados('Sair')
                    self.janela.destroy()
                    tela_login.deiconify()
            else:
                confirmar = dialogs.MessageDialog(parent=self.instancia_com_tabela.home,
                                                title="Tabela já existente",
                                                message=f"Há alterações não salvas, deseja salvar?",
                                                buttons=["Não:danger",
                                                        "Sim:primary",
                                                        "Cancelar:primary"],
                                                alert=True)
                confirmar.show()
                    
                if confirmar.result != 'Cancelar':
                    saves = save.Salvar()
                    if confirmar.result == 'Não':
                        saves.dontSave()
                    if confirmar.result == 'Sim':
                        saves.save()
                        
                    if command == 'Fechar':
                        apagar_dados()
                        tela_login.destroy()
                    elif command == 'Sair':
                        apagar_dados('Sair')
                        self.janela.destroy()
                        tela_login.deiconify()
            
            
                
        arquivo_menu.add_command(label='Sair', command=lambda: checkSave('Sair'))
        arquivo_menu.add_command(label='Fechar', command=lambda: checkSave('Fechar'))
        
        def import_arquivo(tipo):
            try:
                if tipo=='csv':
                    arquivo = filedialog.askopenfilename(filetypes=[("CSV", ".csv .txt")])
                    nome = arquivo.split("/")[-1]
                    nome = nome.split('.')[0]
                    nome = f'{nome}_temp'
                    
                    if self.aba_atual == None or self.aba_atual == 0:
                        csv = tabela_pareto.pareto()
                        matplot, tabela = csv.imports(arquivo, 'csv')
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
                        excel = tabela_pareto.pareto()
                        matplot, tabela = excel.imports(arquivo, 'excel')
                        self.instancia_com_tabela.analise_pareto(tabela, matplot, nome)
                    
                    elif self.aba_atual == 1:
                        excel = asyncio.run(medidas.imports(arquivo, 'xlsx', nome))
                        self.instancia_com_tabela.medidas(excel,nome)
            except Exception as e:
                print(e)
        
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