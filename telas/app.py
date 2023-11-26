import ttkbootstrap as ttk
from tkinter import filedialog
from data import edit_config
from bd import tabela_pareto, medidas, sqlite, save
from telas.inicio import inicio
import os, asyncio, ctypes
from functools import partial

class Tela:
    instancia_com_tabela=None
    aba_atual = None
    def __init__(self, janela='', titulo=''):
        try:
            scale = ctypes.windll.shcore.GetScaleFactorForDevice (0) / 100
        except:
            scale = 1
        ttk.utility.enable_high_dpi_awareness(root=janela,scaling=scale)
        self.janela = janela
        self.janela.title(titulo)
        icone_caminho= os.path.abspath('data/icone.png')
        self.janela.iconphoto(False, ttk.PhotoImage(file=icone_caminho))
        self.estilo = Estilo()
        
        if (self.janela.title()) == 'Peraeque - Login':
            global tela_login
            tela_login = self.janela

        self.TELA_LARGURA = self.janela.winfo_screenwidth()
        self.TELA_ALTURA = self.janela.winfo_screenheight()

    def centralizarTela(self,largura,altura,):
            janela_largura = largura
            janela_altura = altura
            MONITOR_HORIZONTAL = int(self.TELA_LARGURA /2 - janela_largura / 2)
            MONITOR_VERTICAL = int(self.TELA_ALTURA /2 - janela_altura /2)
            self.janela.geometry(f'{janela_largura}x{janela_altura}+{MONITOR_HORIZONTAL}+{MONITOR_VERTICAL}')
                
    def trocar_tema(self):
        if tela_login.style.theme.type == 'dark':
            tela_login.style.theme_use("litera")
            edit_config.editTema('litera')
            self.estilo.tema = 'litera'
        else:
            tela_login.style.theme_use("cyborg")
            edit_config.editTema('cyborg')
            self.estilo.tema = 'cyborg'
        self.estilo.refresh()

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
            if self.aba_atual == 0:
                dados = 'pareto'
            elif self.aba_atual == 1:
                dados = 'medidas'
            elif self.aba_atual == 2:
                dados = 'binomial'
            else:
                dados = 'calculadora'
                
            if do == 'save':
                try:
                    if self.aba_atual == 0:
                        tabela = self.instancia_com_tabela.tabela_pareto
                    elif self.aba_atual == 1:
                        tabela = self.instancia_com_tabela.tabela_medidas
                except:
                    ErrorScreen.error(text='Nenhuma tabela selecionada.\nAbra uma tabela para continuar com o backup.')
                    return
                    
                arquivo = filedialog.asksaveasfilename(confirmoverwrite=True,
                                        defaultextension='.sql',
                                        filetypes=[("SQL script file", ".sql")])
                sql.dump(manual=True, dados=dados, path=arquivo, tabela=tabela)
            elif do == 'restore':
                arquivo = filedialog.askopenfilename(filetypes=[("SQL script file", ".sql")])
                
                def restaurar():
                    sql.restore(manual=True, dados=dados, file=arquivo)
                    edit_config.EditarTabela(table=tabela,dados=dados)
                    if self.aba_atual == 0:
                        self.instancia_com_tabela.analise_pareto()
                    elif self.aba_atual == 1:
                        self.instancia_com_tabela.medidas()
                try:        
                    with open(arquivo, 'r', encoding='utf-8') as file:
                        lines = file.readlines()
                        tabela = lines[1].split(' ')
                        tabela = tabela[-1].split('(')[0]
                except Exception as e:
                    print(e)
                    return
                
                tabelas = sql.getTabelas(dados)
                
                for i in tabelas:
                    if tabela in i:
                        substituir = ErrorScreen.error(text=f"A tabela '{tabela}' já existe.\n Deseja substituí-la?",y=100,
                                                       buttons=["Sim:Danger","Cancelar:primary"])
                try:
                    if substituir != 'Sim':
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
                confirmar = ErrorScreen.error(text=f"Há alterações não salvas, deseja salvar?",
                                                buttons=["Não:danger",
                                                        "Sim:primary",
                                                        "Cancelar:primary"],y=80)
                    
                if confirmar != 'Cancelar':
                    saves = save.Salvar()
                    if confirmar == 'Não':
                        saves.dontSave()
                    if confirmar == 'Sim':
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
                if isinstance(e, FileNotFoundError):
                    print(e)
                else:
                    ErrorScreen.error(text='''Ocorreu um erro ao importar. Verifique se eu arquivo está devidamente formatado. Para mais informações acesse no menu superior: Programa -> Como usar.''', y=150)
        
        importar_menu = ttk.Menu(menu_principal, tearoff=False)
        importar_menu.add_command(label='Importar CSV/TXT', command=lambda: import_arquivo(tipo='csv'))
        importar_menu.add_command(label='Importar arquivo Excel', command=lambda: import_arquivo(tipo='xlsx'))
        
        def export_arquivo(tipo):
            dados = 'pareto' if self.aba_atual == 0 else 'medidas'
            try:
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
            except Exception as e:
                if isinstance(e, ValueError):
                    print(e)
                else:
                    ErrorScreen.error(text='''Ocorreu um erro ao exportar.\nVerifique se seus dados, nome e caminho indicado foram corretamente inseridos e se você possui permissão de escrita ao caminho indicado.\nPara mais informações acesse no menu superior: Programa -> Como usar.''',
                                      x=275,
                                      y=200,
                                      wrap=268)
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

class ErrorScreen():
    def error(text, x=210, y=100, wrap=200, buttons='OK') -> str:
        '''
            Cria um popup de erro ou aviso. Aceita os seguintes parâmetros:
            text: str = texto a ser exibido no popup
            x: int =  tamanho horizontal do popup em pixels(padrao 200)
            y: int = tamanho vertical do popup em pixels (padrao 100)
            wrap: int = quantos pixels até o texto quebrar uma linha (padrao 200)
            buttons: str | list = valores aceitos são 'OK' ou uma lista contendo o 
            texto do botão e seu estilo separados por ':'. ex: ['Sim:primary','Não:Danger']
            
            Returns -> str: texto do botão pressionado.
        '''
        try:
                scale = ctypes.windll.shcore.GetScaleFactorForDevice (0) / 100
        except:
                scale = 1
                
        error = ttk.Toplevel()
        ttk.utility.enable_high_dpi_awareness(root=error,scaling=scale)
        error.title('Erro')
        
        TELA_X = error.winfo_screenwidth()
        TELA_Y = error.winfo_screenheight()
        MONITOR_X = int(TELA_X /2 - x/ 2)
        MONITOR_Y = int(TELA_Y /2 - y /2)
        error.geometry(f'{x}x{y}+{MONITOR_X}+{MONITOR_Y}')
        
        error_label = ttk.Label(error, style='Comum.TLabel')
        error_label.pack(fill='both', expand=True)
        button_frame = ttk.Frame(error, padding=(5, 5))
        
        ttk.Separator(error).pack(fill='x')
        button_frame.pack(side='bottom', fill='x', anchor='s')
        
        resposta = ttk.StringVar()
        
        def set_resposta(retorno):
            resposta.set(retorno)

        def fechar():
            error.destroy()

        def button_callback(retorno):
            set_resposta(retorno)
            fechar()
            
        error_label.config(text=text,wraplength=wrap)
        
        if buttons == 'OK':
            sair_button = ttk.Button(button_frame, text='OK', command=partial(button_callback, 'OK'), style='Estilo1.danger.TButton')
            sair_button.pack(anchor='e')
        else:
            retorno = []
            for indice, valor in enumerate(buttons):
                text, estilo = valor.split(':')
                retorno.append(text)
                button = ttk.Button(button_frame, text=text, style=f'Estilo1.{estilo}.TButton')
                button.configure(command=partial(button_callback, retorno[indice]))
                if valor == buttons[0]:
                    button.pack(anchor='e', side='right')
                else:
                    button.pack(anchor='e', side='right',padx=(0,2))
        error.wait_window()

        return resposta.get()
            

class Estilo:
    tema = edit_config.getTema()
    Tfonte = f'Roboto 16'
    gfonte= f'Roboto 12'
    fonte = f'Roboto 10'
    Sfonte = f'Roboto 9'
    largura = None
    altura = None
    def __init__(self):
        self.style = ttk.Style(self.tema)
        self.cores = self.style._theme_definitions.get(self.tema)
        self.background_2 = '#F2F3F5' if self.tema == 'litera' else '#1E1E21'
        self.background_1 = '#D7D9DC' if self.tema == 'litera' else '#111214'
        self.tab_background_1 = '#FFFFFF' if self.tema == 'litera' else '#191919'
        
        self.load_styles()
        
    def font_size(self, largura, altura):
            if (largura,altura) == (self.largura, self.altura):
                return
            else:
                self.largura = largura
                self.altura = altura
                RESOLUCAO = largura * altura
                
                if RESOLUCAO <= 500*600:
                    self.Tfonte = f'Roboto 12'
                    self.gfonte= f'Roboto 8'
                    self.fonte = f'Roboto 7'
                    self.Sfonte = f'Roboto 6'
                
                elif RESOLUCAO <= 700*700:
                    self.Tfonte = f'Roboto 14'
                    self.gfonte= f'Roboto 10'
                    self.fonte = f'Roboto 9'
                    self.Sfonte = f'Roboto 8'
                elif RESOLUCAO <= 900*600:
                    self.Tfonte = f'Roboto 16'
                    self.gfonte= f'Roboto 12'
                    self.fonte = f'Roboto 10'
                    self.Sfonte = f'Roboto 9'
                elif RESOLUCAO <= 1280*800:
                    self.Tfonte = f'Roboto 18'
                    self.gfonte= f'Roboto 13'
                    self.fonte = f'Roboto 11'
                    self.Sfonte = f'Roboto 10'
                elif RESOLUCAO <= 1600 * 800:
                    self.Tfonte = f'Roboto 20'
                    self.gfonte= f'Roboto 15'
                    self.fonte = f'Roboto 13'
                    self.Sfonte = f'Roboto 12'
                elif RESOLUCAO <= 1920 * 900:
                    self.Tfonte = f'Roboto 22'
                    self.gfonte= f'Roboto 17'
                    self.fonte = f'Roboto 15'
                    self.Sfonte = f'Roboto 14'
                elif RESOLUCAO >= 1920 * 900:
                    self.Tfonte = f'Roboto 24'
                    self.gfonte= f'Roboto 19'
                    self.fonte = f'Roboto 17'
                    self.Sfonte = f'Roboto 16'
                    
                self.refresh()
                    
    def load_styles(self):
        self.style.configure('.', f=self.fonte)
        self.style.configure("TCheckbutton", font=self.Sfonte)
        self.style.configure('Estilo1.TButton', font=self.fonte)
        self.style.configure('Estilo1.primary.TButton', font=self.fonte)
        self.style.configure('Estilo1.info.TButton', font=self.fonte)
        self.style.configure('Estilo1.danger.TButton', font=self.fonte)
        self.style.configure('Estilo1.Link.TButton', font=self.Sfonte,
                            focuscolor=self.cores.colors.primary,
                            foreground=self.cores.colors.primary,)
        self.style.configure('Estilo2.Link.TButton', font=self.fonte,
                             focuscolor=self.cores.colors.primary,
                             foreground=self.cores.colors.primary,
                             )
        self.style.configure('Titulo.TLabel', font=self.Tfonte, foreground=self.cores.colors.info)
        self.style.configure('Titulo2.TLabel', font=self.Tfonte, foreground=self.cores.colors.info, background=self.background_2)
        self.style.configure('Comum.TLabel', font=self.fonte)
        self.style.configure('Comum2.TLabel', font=self.fonte, background=self.background_1)
        self.style.configure('Error.TLabel', font=self.fonte, foreground=self.cores.colors.danger)
        self.style.configure('Pequeno.TLabel', font=self.Sfonte)
        self.style.configure('Grande.TLabel', font=self.gfonte)
        self.style.configure('TCombobox', font=self.fonte)
        self.style.configure('Table.Treeview',font=self.fonte, rowheight=30)
        self.style.configure('Table.Treeview.Heading', font=self.Sfonte)
        self.style.configure('custom.TFrame', relief='solid')
        self.style.configure('custom2.TFrame', background=self.background_2)
        self.style.configure('custom3.TFrame', background=self.background_1, relief='solid')
        self.style.configure('custom.TNotebook',
                             background=self.background_2,
                             foreground=self.background_2)
        self.style.configure('custom2.TNotebook')
        self.style.map('custom.TNotebook.Tab',
                             background=[("selected", self.tab_background_1),("!selected", self.background_2)],
                             font=self.Sfonte)
        self.style.map('custom2.TNotebook.Tab',
                             background=[("selected", self.background_2)],
                             font=self.Sfonte)
        self.style.configure('custom.TEntry', font=self.fonte)
        #self.style.configure('custom.TCombobox', font=self.fonte)
        #self.style.configure('custom.TSpinbox', font=self.fonte)
    
    def refresh(self):
        self.tema = edit_config.getTema()
        self.style = ttk.Style(self.tema)
        self.cores = self.style._theme_definitions.get(self.tema)
        self.background_2 = '#F2F3F5' if self.tema == 'litera' else '#1E1E21'
        self.background_1 = '#D7D9DC' if self.tema == 'litera' else '#111214'
        self.tab_background_1 = '#FFFFFF' if self.tema == 'litera' else '#191919'
        
        self.load_styles()