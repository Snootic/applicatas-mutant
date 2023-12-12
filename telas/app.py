import ttkbootstrap as ttk
import os, asyncio, ctypes, sys
from ttkbootstrap.style import StyleBuilderTTK
from tkinter import filedialog
from data import edit_config
from data.users import UsuariosFunc
from data.auth import cadastro
from bd import tabela_pareto, medidas, sqlite, save
from telas.inicio import inicio
from functools import partial

class Tela:
    instancia_com_tabela=None
    aba_atual = None
    def __init__(self, janela='', titulo=''):
        self.scale = edit_config.get_scale()
        if self.scale == None:
            try:
                self.scale = ctypes.windll.shcore.GetScaleFactorForDevice (0) / 100
            except:
                self.scale = 1
        ttk.utility.enable_high_dpi_awareness(root=janela,scaling=self.scale)
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
            self.janela.update_idletasks()
                
    def trocar_tema(self, tema=''):
        if tema != '':
            tela_login.style.theme_use(tema)
            edit_config.editTema(tema)
            self.estilo.tema = tema
        else:
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
                is_saved = True if is_saved == 'True' else False
                if is_saved:
                    edit_config.setAutoSave(False)
                    save_variable.set(False)
                else:
                    edit_config.setAutoSave(True)
                    save_variable.set(True)
            elif do == 'get_autosave':
                is_saved = edit_config.getAutoSave()
                is_saved = True if is_saved == 'True' else False
                return is_saved
                
        arquivo_menu = ttk.Menu(menu_principal, tearoff=False)
        arquivo_menu.add_command(label='Restaurar Backup', command=lambda: manual_backup(do='restore'))
        arquivo_menu.add_command(label='Salvar Backup', command=lambda: manual_backup(do='save'))
        arquivo_menu.add_command(label='Salvar arquivo', command=lambda: salvar('save'))
        save_variable = ttk.BooleanVar()
        arquivo_menu.add_checkbutton(label='Salvar Automaticamente', command=lambda: salvar('autosave'), variable=save_variable, onvalue=True, offvalue=False)
        autosave = salvar('get_autosave')
        save_variable.set(autosave)
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
            autosave = salvar('get_autosave')
            if not autosave:
                pass
            else:
                salvar('save')
            
            is_saved = edit_config.getIsSaved()
            is_saved = True if is_saved == 'True' else False
            
            if is_saved:
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
                                      y=200)
        exportar_menu = ttk.Menu(menu_principal, tearoff=False)
        exportar_menu.add_command(label='Exportar - CSV', command=lambda: export_arquivo(tipo='csv'))
        exportar_menu.add_command(label='Exportar - Excel', command=lambda: export_arquivo(tipo='xlsx'))
        
        programa_menu = ttk.Menu(menu_principal, tearoff=False)
        escala_menu = ttk.Menu(programa_menu)
        programa_menu.add_cascade(label='Escala', menu=escala_menu)
        escala_menu.add_command(label='Aumentar', command=lambda: self.setScale('soma'))
        escala_menu.add_command(label='Diminuir', command=lambda: self.setScale('sub'))
        programa_menu.add_command(label='Trocar Tema', command=lambda: self.trocar_tema())
        version = os.path.abspath('VERSION')
        with open(version, 'r') as version:
            versao = version.readlines()
            self.data = versao[1]
            self.versao = versao[0]
            self.python_v = versao[2]
        programa_menu.add_command(label=f'Versão: {self.versao}')
        
        def about_screen(master):
            master.update()
            wrap = master.winfo_width()
            if not isinstance(master, ttk.Frame):
                master = ttk.Frame(master, style='custom2.TFrame')
                master.pack(expand=True, fill='both')
            titulo = ttk.Label(master, text='Applicatas Mutant', style='Titulo2.TLabel')
            sub_titulo = ttk.Label(master, text='Obrigado por usar nosso programa!', style='Grande2.TLabel')
            
            if wrap == 1:
                wrap = 290
            
            desenvolvedores = ['Kaik Mendes - @Snootic | @Snootic_']
            desenvolvedores_text = ""
            for i in desenvolvedores:
                desenvolvedores_text += f'{i}\n'
            desenvolvedor = ttk.Label(master, text='Desenvolvedor:', style='Comum3.TLabel')
            desenvolvedores = ttk.Label(master, text=f'{desenvolvedores_text}', style = 'Comum3.TLabel')
            
            contribuidores = ['Luis Guilherme Silva de Sousa - @LGSS18']
            contribuidores_text = ""
            for i in contribuidores:
                contribuidores_text += f'{i}\n'
            contribuidor = ttk.Label(master, text='Contribuidores:', style='Comum3.TLabel')
            contribuidores = ttk.Label(master, text=f'{contribuidores_text}', style = 'Comum3.TLabel')
            
            versao = ttk.Label(master, text=f"Versão: {self.versao}", style='Comum3.TLabel')
            data = ttk.Label(master, text=f"Data: {self.data}", style='Comum3.TLabel')
            python = ttk.Label(master, text=f"Python: {self.python_v}", style='Comum3.TLabel', wraplength=wrap)
            
            titulo.place(anchor='center', relx=0.5, rely=0.05)
            sub_titulo.place(anchor='center', relx=0.5, rely=0.13)
            desenvolvedor.place(relx=0, rely=0.25)
            desenvolvedores.place(relx=0, rely=0.3)
            contribuidor.place(relx=0, rely=0.5)
            contribuidores.place(relx=0, rely=0.55)
            versao.place(relx=0, rely=0.7)
            data.place(relx=0, rely=0.75)
            python.place(relx=0, rely=0.8)
            
        about_title = 'Sobre - Applicatas Mutant'
        programa_menu.add_command(label='Sobre', command= lambda: ErrorScreen.error(about_screen, titulo=about_title, x=350,y=400, buttons=['OK:info']))
        
        def config_screen(master):
            notebook = ttk.Notebook(master, style='custom2.TNotebook')
            notebook.pack(expand=True, fill='both')
            
            visual_frame = ttk.Frame(notebook, style='custom2.TFrame')
            edit_user_frame = ttk.Frame(notebook, style='custom2.TFrame')
            about_frame = ttk.Frame(notebook, style='custom2.TFrame')
            edit_user_frame.pack(expand=True, fill='both')
            visual_frame.pack(expand=True, fill='both')
            about_frame.pack(expand=True, fill='both')
            
            notebook.add(visual_frame, text='Visual')
            notebook.add(edit_user_frame, text='Editar Conta')
            notebook.add(about_frame, text='Sobre')
            
            def visual_programa():
                def salvar():
                    if trocar_tema_var.get() not in style.theme_names():
                        trocar_tema.configure(bootstyle="Danger")
                        master.after(3000,lambda: trocar_tema.configure(bootstyle="default"))
                        return
                    elif trocar_tema_var.get() != '':
                        self.trocar_tema(trocar_tema_var.get())

                    if escala_programa_var.get() != '':
                        try:
                            float(escala_programa_var.get())
                        except:
                            escala_programa.configure(bootstyle="Danger")
                            master.after(3000,lambda: escala_programa.configure(bootstyle='default'))
                        else:
                            edit_config.set_scale(escala_programa_var.get())
                            confirmar = ErrorScreen.error(titulo='Reinicialização pendente',
                                                        text='O programa precisa ser reiniciado para que as alterações sejam feitas. Deseja continuar? Nenhuma alteração será perdida.',
                            buttons=['Sim:info', 'Não:info'], y=120)
                            if confirmar == 'Não':
                                return
                            elif confirmar == 'Sim':
                                self.restart()
                    
                trocar_tema_label = ttk.Label(visual_frame, text='Tema', style='Comum3.TLabel')
                trocar_tema_var = ttk.StringVar(value=Estilo.tema)
                trocar_tema = ttk.Combobox(visual_frame, textvariable=trocar_tema_var)
                
                escala_programa_label = ttk.Label(visual_frame, text='Escala do programa', style='Comum3.TLabel')
                escala_programa_var = ttk.StringVar()
                escala_programa = ttk.Combobox(visual_frame, textvariable=escala_programa_var)
                
                trocar_tema_label.place(relx=0.05, rely=0.05, relwidth=0.5)
                trocar_tema.place(relx=0.05, rely=0.11, relwidth=0.75)
                escala_programa_label.place(relx=0.05, rely=0.24, relwidth=0.5)
                escala_programa.place(relx=0.05, rely=0.3, relwidth=0.75)
                
                salvar_botao = ttk.Button(visual_frame, text='Salvar', style='Estilo1.TButton', command=salvar)
                salvar_botao.place(relx=0.05, rely=0.5, relwidth=0.25, relheight=0.1)
                
                style = ttk.Style()
                trocar_tema['value'] = style.theme_names()
                
                escalas = [1.0, 1.25, 1.50, 1.75, 2.0]
                escala_programa['value'] = escalas
                
            def editar_usuario():
                def salvar():
                    if edit_user_var.get() == '':
                        user = edit_config.getUser()
                        old_user = user
                    else:
                        old_user = edit_config.getUser()
                        user = edit_user_var.get()
                        if not usuario():
                            user_error()
                            return
                    users = UsuariosFunc.getDados(edit_config.getUser())
                    if edit_email_var.get() == '':
                        new_email = users.get_email()[0]
                        old_email = new_email
                    else:
                        old_email = users.get_email()[0]
                        new_email = edit_email_var.get()
                        if not email():
                            email_error()
                            return

                    if edit_senha_var.get().strip() != "" or confirm_senha_var.get().strip() != "":
                        if not senha():
                            print('a')
                            senha_error()
                            return
                        elif not confirmar_senha():
                            print('b')
                            senha_error(same=True)
                            return
                        
                    users = UsuariosFunc.InserirDados(user, new_email, edit_senha_var.get(), old_user, old_email) 
                    users.alterarUser()
                    users.alterarEmail()
                    if edit_senha_var.get() != '':
                        users.alterarSenha()
                
                    edit_config.editUser(user)
                    confirmar = ErrorScreen.error(titulo='Reinicialização pendente',
                        text='O programa precisa ser reiniciado para que as alterações sejam feitas. Deseja continuar? Nenhuma alteração será perdida.',
                        buttons=['OK:info'], y=120)
                    self.restart(users.rename_database)
                
                def user_error():
                    edit_user.configure(bootstyle="Danger")
                    master.after(3000,lambda: edit_user.configure(bootstyle="default"))
                def email_error():
                    edit_email.configure(bootstyle="Danger")
                    master.after(3000,lambda: edit_email.configure(bootstyle="default"))
                def senha_error(same=False):
                    if same == True:
                        confirm_senha.configure(bootstyle="Danger")
                        master.after(3000,lambda: confirm_senha.configure(bootstyle="default"))
                        edit_senha.configure(bootstyle="Danger")
                        master.after(3000,lambda: edit_senha.configure(bootstyle="default"))
                    else:
                        edit_senha.configure(bootstyle="Danger")
                        master.after(3000,lambda: edit_senha.configure(bootstyle="default"))
                
                def usuario():
                    usuario = cadastro.credenciais(usuario=edit_user.get())
                    usuario = usuario.user()
                    if usuario != True:
                        retorno.configure(text=usuario)
                        user_error()
                        return False
                    else:
                        retorno.configure(text='usuario')
                        return True
                
                def email():
                    email = cadastro.credenciais(email=edit_email.get())
                    email = email.Email()
                    if email != True:
                        retorno.configure(text=email)
                        email_error()
                        return False
                    else:
                        retorno.configure(text='')
                        return True
                
                def senha(*args):
                    senha = cadastro.credenciais(senha=edit_senha_var.get())
                    senha = senha.passw()
                    if senha != True:
                        retorno.configure(text=senha)
                        senha_error()
                        return False
                    else:
                        retorno.configure(text='')
                        return True
                
                def confirmar_senha(*args):
                    confirmar_senha = confirm_senha_var.get()
                    senha = edit_senha_var.get()
                    if confirmar_senha != senha:
                        retorno.configure(text='As senhas não coincidem')
                        return False
                    else:
                        retorno.configure(text='')
                        return True
                        
                edit_user_var = ttk.StringVar()
                edit_email_var = ttk.StringVar()
                edit_senha_var = ttk.StringVar()
                confirm_senha_var = ttk.StringVar()
                
                edit_user_label = ttk.Label(edit_user_frame, text='Alterar Usuário', style='Comum3.TLabel')
                edit_email_label = ttk.Label(edit_user_frame, text='Alterar E-mail', style='Comum3.TLabel')
                edit_senha_label = ttk.Label(edit_user_frame, text='Alterar Senha', style='Comum3.TLabel')
                confirm_senha_label = ttk.Label(edit_user_frame, text='Confirmar nova senha', style='Comum3.TLabel')
                
                edit_user = ttk.Entry(edit_user_frame, textvariable=edit_user_var, style='Custom.TEntry')
                edit_email = ttk.Entry(edit_user_frame, textvariable=edit_email_var, style='Custom.TEntry')
                edit_senha = ttk.Entry(edit_user_frame, textvariable=edit_senha_var, style='Custom.TEntry')
                confirm_senha = ttk.Entry(edit_user_frame, textvariable=confirm_senha_var, style='Custom.TEntry')
                
                edit_user_label.place(relx=0.05, rely=0.05, relwidth=0.55)
                edit_user.place(relx=0.05, rely=0.11, relwidth=0.75)
                
                edit_email_label.place(relx=0.05, rely=0.24, relwidth=0.55)
                edit_email.place(relx=0.05, rely=0.3, relwidth=0.75)
                
                edit_senha_label.place(relx=0.05, rely=0.43, relwidth=0.55)
                edit_senha.place(relx=0.05, rely=0.49, relwidth=0.75)
                
                confirm_senha_label.place(relx=0.05, rely=0.62, relwidth=0.75)
                confirm_senha.place(relx=0.05, rely=0.67, relwidth=0.75)
                
                retorno = ttk.Label(edit_user_frame, style='Comum3.TLabel', text='')
                retorno.place(relx=0.05, rely=0.79)
                
                salvar_botao = ttk.Button(edit_user_frame, text='Salvar', style='Estilo1.TButton', command=salvar)
                salvar_botao.place(relx=0.05, rely=0.88, relwidth=0.25, relheight=0.1)
                
                deletar_conta = ttk.Button(edit_user_frame, text='Deletar Conta', style='Estilo1.danger.Button')
                deletar_conta.place(relx=0.35, rely=0.88, relwidth=0.45, relheight=0.1)

            about_screen(about_frame)
            
            visual_programa()
            editar_usuario()
            
        menu_principal.add_cascade(label='Arquivo', menu=arquivo_menu)
        menu_principal.add_cascade(label='Importar', menu=importar_menu)
        menu_principal.add_cascade(label='Exportar', menu=exportar_menu)
        menu_principal.add_cascade(label='Programa', menu=programa_menu)
        menu_principal.add_command(label='Configurações', command=lambda: ErrorScreen.error(config_screen, 
                                                                                            titulo='Peraeque - Configurações',
                                                                                            x=270,
                                                                                            y=400,
                                                                                            buttons=['Fechar:default']))
        self.janela.config(menu=menu_principal)
    
    def restart(self, *args):
        python = sys.executable
        for i in args:
            i()
        edit_config.limpar_temp()
        os.execl(python, python, * sys.argv)
        
    
    def setScale(self, operação):
        '''
            operação: 'soma'|'sub'
            Aumenta ou diminui a escala do programa
        '''
        if operação == 'soma':
            if self.scale < 2:
                self.scale += 0.25
        elif operação == 'sub':
            if self.scale > 1:
                self.scale -= 0.25
        
        ttk.utility.enable_high_dpi_awareness(root=self.janela,scaling=self.scale)

        edit_config.set_scale(self.scale)
        
        confirmar = ErrorScreen.error(titulo='Reinicialização pendente', text='O programa precisa ser reiniciado para que as alterações sejam feitas. Deseja continuar? Nenhuma alteração será perdida.',
                          buttons=['Sim:info', 'Não:info'], y=120)
        if confirmar == 'Não':
            return
        elif confirmar == 'Sim':
            self.restart()
                                 
class ErrorScreen():
    def error(*args, text='Lore Ipsum', x=210, y=100, buttons='OK', titulo='Erro') -> str:
        '''
            Cria um popup de erro ou aviso. Aceita os seguintes parâmetros:
            text: str = texto a ser exibido no popup
            x: int =  tamanho horizontal do popup em pixels(padrao 200)
            y: int = tamanho vertical do popup em pixels (padrao 100)
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
        error.title(titulo)
        error.resizable(False,False)
        
        TELA_X = error.winfo_screenwidth()
        TELA_Y = error.winfo_screenheight()
        MONITOR_X = int(TELA_X /2 - x/ 2)
        MONITOR_Y = int(TELA_Y /2 - y /2)
        
        estilo = ttk.Style(edit_config.getTema())
        fonte = estilo.lookup('Comum.TLabel', 'font')
        fonte = int(fonte.split(' ')[1])
        
        adjust_geometry = (fonte / 10)
        x = int(round(x * adjust_geometry))
        y = int(round(y * adjust_geometry))
        
        error.geometry(f'{x}x{y}+{MONITOR_X}+{MONITOR_Y}')
        
        try:
            for i in args:
                widget = partial(i, error) # pack the widgets from args
                widget()
        except Exception as e:
            print(e)
        
        if not args:
            error_label = ttk.Label(error, style='Comum.TLabel')
            error_label.pack(fill='both', expand=True)
            error_label.config(text=text,wraplength=x)
            
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
    def __init__(self):
        self.Tfonte = f'Roboto 16'
        self.gfonte= f'Roboto 12'
        self.fonte = f'Roboto 10'
        self.Sfonte = f'Roboto 9'
        self.largura = None
        self.altura = None
        
        self.refresh()
        
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
        self.style.configure('Estilo1.default.TButton', font=self.fonte)
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
        self.style.configure('Comum3.TLabel', font=self.fonte, background=self.background_2)
        self.style.configure('Error.TLabel', font=self.fonte, foreground=self.cores.colors.danger)
        self.style.configure('Pequeno.TLabel', font=self.Sfonte)
        self.style.configure('Grande.TLabel', font=self.gfonte)
        self.style.configure('Grande2.TLabel', font=self.gfonte, background=self.background_2)
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
        self.style.configure('custom.Table.Treeview', font=self.Tfonte)
        self.style.configure('custom.Table.Treeview.Heading', font=self.Tfonte)
        #self.style.configure('custom.TCombobox', font=self.fonte)
        #self.style.configure('custom.TSpinbox', font=self.fonte)
    
    def refresh(self):
        self.tema = edit_config.getTema()
        self.style = ttk.Style(self.tema)
        self.cores = self.style._theme_definitions.get(self.tema)
        self.background_2 = '#E3E5E8' if self.style.theme.type == 'light' else '#1E1E21'
        self.background_1 = '#D7D9DC' if self.style.theme.type == 'light'else '#111214'
        self.tab_background_1 = '#FFFFFF' if self.style.theme.type == 'light' else '#191919'
        
        self.load_styles()