from tkinter import *
import ttkbootstrap as ttk
from telas.app import *
from data.auth import login, cadastro
from telas import inicio
from data.edit_config import getUser, getSenha
import os
from data.users import UsuariosFunc

class telalogin:
    def __init__(self):
        self.login = ttk.Window()
        tela = Tela(self.login, 'Peraeque - Login')
        tela.centralizarTela(600,600)
        self.login.resizable(False,False)
        
        self.login.bind("<Map>", lambda event: self.size_change())
        
        self.estilo = tela.estilo

        titulo = ttk.Label(self.login,
                           text='Applicatas Mutant',
                           style='Titulo.TLabel')
        subtitulo = ttk.Label(self.login,
                              text='Bem vindo! Faça login para continuar',
                              style='Grande.TLabel')
        titulo.place(x=300,y=70,anchor='center')
        subtitulo.place(x=300,y=100,anchor='center')
        
        retorno = ttk.Label(self.login,
                            text='',
                            style='Comum.TLabel')
        retorno.place(x=300,y=345,anchor='center')
        retorno.update_idletasks()
        
        def user_entry(self):
            self.user_var = StringVar(value='Usuário / E-mail')
            self.user_entry = ttk.Entry(self.login,
                                textvariable=self.user_var,
                                style='custom.TEntry', width=35)
            self.user_entry.place(x=300,y=200,anchor='center', height=60)
            self.user_entry.bind('<FocusIn>',lambda event: (self.user_var.set(value=''),
                                                            self.user_entry.unbind('<FocusIn>')))
        def senha_entry(self):
            self.senha_var = StringVar(value='Senha')
            self.senha_entry = ttk.Entry(self.login, textvariable=self.senha_var, style='custom.TEntry',width=35)
            self.senha_entry.place(x=300,y=280,anchor='center', height=60)
            self.senha_entry.bind('<FocusIn>',lambda event: (self.senha_var.set(value=''),
                                                            self.senha_entry.unbind('<FocusIn>'),
                                                            self.senha_entry.configure(show='*')))
        user_entry(self)
        senha_entry(self)
        
        def manter_logado(self):
            self.texto_secao_var = StringVar(value='Manter seção')
            self.manter_secao_var= BooleanVar(value=False)
            self.manter_secao = ttk.Checkbutton(self.login,
                                        var=self.manter_secao_var,
                                        textvariable=self.texto_secao_var,
                                        style='TCheckbutton',
                                        bootstyle='info')
            self.manter_secao.place(x=165,y=460,anchor='center')
            
        manter_logado(self)
            
        def logando(user, senha, manter_secao=False):
            global inicio
            log = login.login(user,senha,manter_secao)
            retorno.configure(text=log)
            if log == 'Senha incorreta':
                self.senha_entry.configure(bootstyle="danger")
                self.login.after(3000,lambda: self.senha_entry.configure(bootstyle="default"))
            elif log == 'Usuário ou E-mail não cadastrados':
                self.user_entry.configure(bootstyle="danger")
                self.login.after(3000,lambda: self.user_entry.configure(bootstyle="default"))
            elif log == 'Logado':
                retorno.configure(text='')
                self.senha_entry.destroy()
                self.user_entry.destroy()
                self.manter_secao_var.set(value=False)
                user_entry(self)
                senha_entry(self)
                self.login.withdraw()
                inicio = inicio.inicio(self.login,self.estilo)
                
        logar_var = StringVar(value='Entrar')
        logar = ttk.Button(self.login,
                           width=38,
                           textvariable=logar_var,
                           style='Estilo1.info.TButton',
                           command=lambda: logando(self.user_var.get(),self.senha_var.get(),self.manter_secao_var.get()))
        logar.place(x=300,y=400,anchor='center', height=70)
        
        
        esqueci_senha_var = StringVar(value='Esqueci minha senha')
        esqueci_senha = ttk.Button(self.login,
                                   textvariable=esqueci_senha_var,
                                   style='Estilo1.Link.TButton',
                                   command=lambda: self.esqueceu_senha())
        esqueci_senha.place(x=420,y=460,anchor='center')
        
        registrar_label = ttk.Label(text='Não tem conta?',
                                    style='Comum.TLabel')
        registrar = ttk.Button(self.login, text='Registre-se aqui',
                               style='Estilo2.Link.TButton',
                               command=self.registro)
        registrar_label.place(x=210,y=550,anchor='center')
        registrar.place(x=365, y=550, anchor='center')
        
        trocar_tema = ttk.Checkbutton(self.login, bootstyle="info-round-toggle", text='Tema', command=tela.trocar_tema)
        trocar_tema.place(relx=0.85,rely=0.96)
        
        aumentar_escala = ttk.Button(self.login, text='+', command=lambda: tela.setScale('soma'), style='Estilo1.info.TButton')
        diminuir_escala = ttk.Button(self.login, text='-', command=lambda: tela.setScale('sub'), style='Estilo1.info.TButton')
        aumentar_escala.place(relx=0.85,rely=0.6, relheight=0.06, relwidth=0.06)
        diminuir_escala.place(relx=0.85,rely=0.67, relheight=0.06, relwidth=0.06)
        
        self.login.protocol("WM_DELETE_WINDOW", self.login.destroy)
        try:
            usuario = getUser()
            senha = getSenha()
            if usuario == '' and senha == '':
                pass
            else:
                logando(usuario,senha,manter_secao=True)
        except Exception as e:
            retorno.configure(text=e)
        
        self.login.mainloop()
    
    def size_change(self):
        self.login.update()
        self.login.update_idletasks()
        
        tela_largura = self.login.winfo_width()
        tela_altura = self.login.winfo_height()
        
        # Define o tamanho da fonte
        self.estilo.font_size(tela_largura, tela_altura)
        self.estilo.refresh()
             
    def registro(self):
        registro = ttk.Toplevel(self.login)
        registro.geometry('400x500')
        registro.resizable(False, False)
        registro.title('Registrar-se')

        titulo = ttk.Label(registro, text='Registrar-se', font='Nexa 20')
        titulo.pack(pady=20)
        
        retorno = ttk.Label(registro, style='Comum.TLabel', text='')

        def user_error():
            user_entry.configure(bootstyle="Danger")
            registro.after(3000,lambda: user_entry.configure(bootstyle="default"))
        def email_error():
            email_entry.configure(bootstyle="Danger")
            registro.after(3000,lambda: email_entry.configure(bootstyle="default"))
        def senha_error(same=False):
            if same == True:
                confirmar_senha_entry.configure(bootstyle="Danger")
                registro.after(3000,lambda: confirmar_senha_entry.configure(bootstyle="default"))
                senha_entry.configure(bootstyle="Danger")
                registro.after(3000,lambda: senha_entry.configure(bootstyle="default"))
            else:
                senha_entry.configure(bootstyle="Danger")
                registro.after(3000,lambda: senha_entry.configure(bootstyle="default"))
        
        
        def usuario():
            usuario = cadastro.credenciais(usuario=user_var.get())
            usuario = usuario.user()
            if usuario != True:
                retorno.configure(text=usuario)
                user_error()
                return False
            else:
                retorno.configure(text='')
                return True
        
        user_var = StringVar(value='Usuário')
        user_entry = ttk.Entry(registro,
                               textvariable=user_var,
                               style='custom.TEntry'
                               )
        user_entry.place(anchor='center', relx=0.5, rely=0.2, height=59, width=255)
        user_entry.bind('<FocusIn>',lambda event: (user_var.set(value=''),
                                                         user_entry.unbind('<FocusIn>'),
                                                         user_entry.bind('<KeyRelease>', lambda event: usuario())
                                                         ))

        def email():
            email = cadastro.credenciais(email=email_var.get())
            email = email.Email()
            if email != True:
                retorno.configure(text=email)
                email_error()
                return False
            else:
                retorno.configure(text='')
                return True
        
        
        email_var = StringVar(value='E-mail')
        email_entry = ttk.Entry(registro,
                                textvariable=email_var,
                                style='custom.TEntry')
        email_entry.place(anchor='center', relx=0.5, rely=0.33, height=59, width=255)
        email_entry.bind('<FocusIn>',lambda event: (email_var.set(value=''),
                                                         email_entry.unbind('<FocusIn>'),
                                                         email_entry.bind('<KeyRelease>', lambda event: email())
                                                         ))
        
        def senha(*args):
            senha = cadastro.credenciais(senha=senha_var.get())
            senha = senha.passw()
            if senha != True:
                retorno.configure(text=senha)
                senha_error()
                return False
            else:
                retorno.configure(text='')
                return True
        
        senha_frame = Frame(registro, height=73, width=400)
        senha_frame.place(anchor='center', relx=0.5, rely=0.455)
        senha_frame.lower()
        
        senha_var = StringVar(value='Senha')
        senha_entry = ttk.Entry(senha_frame,
                                textvariable=senha_var,
                                style='custom.TEntry')
        senha_entry.place(anchor='center', relx=0.5, rely=0.53, height=59, width=255)
        senha_entry.bind('<FocusIn>',lambda event: senha_var.set(value=''))
        senha_var.trace('w',lambda *args: esconder_senha())
        
        esconder_senha_imagem = PhotoImage(file = os.path.abspath('data/assets/hide_password.png'))
        ver_senha_imagem = PhotoImage(file = os.path.abspath('data/assets/show_password.png'))
        
        ver_senha=ttk.Button(senha_frame,padding=1, image = esconder_senha_imagem, command=lambda: esconder_senha(ver='ver',
                                                                                                                  entry=senha_entry,
                                                                                                                  entry1=confirmar_senha_entry))
        ver_senha.place(anchor='nw', relx=0.83, rely=0.13)
        
        
        def gerarsenha():
            senha_gerada = cadastro.credenciais()
            senha_gerada = senha_gerada.GerarSenha()
            senha_var.set(value=senha_gerada)
            confirmar_senha_var.set(value=senha_gerada)
            
        gerar_senha_imagem = PhotoImage(file = os.path.abspath('data/assets/generate_password.png'))
        gerar_senha = ttk.Button(senha_frame,padding=1,image = gerar_senha_imagem,command=gerarsenha)
        gerar_senha.place(anchor='nw', relx=0.83, rely=0.58)

        def confirmar_senha(*args):
            confirmar_senha = confirmar_senha_var.get()
            senha = senha_var.get()
            if confirmar_senha != senha:
                retorno.configure(text='As senhas não coincidem')
                return False
            else:
                retorno.configure(text='')
                return True
        
        
        confirmar_senha_var = StringVar(value='Confirmar Senha')
        confirmar_senha_entry = ttk.Entry(registro,
                                          textvariable=confirmar_senha_var,
                                          style='custom.TEntry')
        confirmar_senha_entry.place(anchor='center', relx=0.5, rely=0.595, height=59, width=255)
        confirmar_senha_entry.bind('<FocusIn>',lambda event: confirmar_senha_var.set(value=''),)
        
        confirmar_senha_var.trace('w',lambda *args: esconder_senha(entry=confirmar_senha_entry,
                                                                   comando=confirmar_senha))
        
        def esconder_senha(ver='esconder',entry=senha_entry,comando=senha,entry1=''):
            if ver=='esconder':
                entry.unbind('<FocusIn>'),
                entry.configure(show='*')
                entry.bind('<KeyRelease>', comando)
                ver_senha.config(image=esconder_senha_imagem)
                
            elif ver=='ver':
                entry1.configure(show='')
                entry.configure(show='')
                ver_senha.config(image=ver_senha_imagem)
            else:
                return False
        
        def cadastrar():
            if not confirmar_senha():
                retorno.configure(text='As senhas não coincidem')
                senha_error(same=True)
            elif not senha():
                retorno.configure(text='Senha inválida')
                senha_error()
            elif not email():
                retorno.configure(text='E-mail inválido')
                email_error()
            elif not usuario():
                retorno.configure(text='Usuário Inválido')
                user_error()
            else:
                cadastrar = cadastro.credenciais(user_var.get(),email_var.get(),senha_var.get())
                cadastrar = cadastrar.cadastrar()
                retorno.configure(text=cadastrar)
            
        
        confirmar = ttk.Button(registro,
                               style='Estilo1.info.TButton',
                               text='Registrar',
                               command=cadastrar)
        confirmar.place(anchor='center', relx=0.5, rely=0.8, relheight=0.1, relwidth=0.3)
        
        retorno.place(anchor='center', relx=0.5, rely=0.7)
        
        registro.mainloop()

    def esqueceu_senha(self):
        tela = ttk.Toplevel(self.login)
        tela.geometry('400x500')
        tela.resizable(False, False)
        tela.title('Esqueci minha senha')

        titulo = ttk.Label(tela, text='Resetar senha', font='Nexa 20')
        titulo.pack(pady=20)
        
        retorno = ttk.Label(tela, style='Comum.TLabel', text='')

        def user_error():
            user_entry.configure(bootstyle="Danger")
            tela.after(3000,lambda: user_entry.configure(bootstyle="default"))
        def email_error():
            email_entry.configure(bootstyle="Danger")
            tela.after(3000,lambda: email_entry.configure(bootstyle="default"))
        def senha_error(same=False):
            if same == True:
                confirmar_senha_entry.configure(bootstyle="Danger")
                tela.after(3000,lambda: confirmar_senha_entry.configure(bootstyle="default"))
                senha_entry.configure(bootstyle="Danger")
                tela.after(3000,lambda: senha_entry.configure(bootstyle="default"))
            else:
                senha_entry.configure(bootstyle="Danger")
                tela.after(3000,lambda: senha_entry.configure(bootstyle="default"))
        
        
        def usuario():
            usuario = cadastro.credenciais(usuario=user_var.get())
            usuario = usuario.user()
            if usuario == True:
                retorno.configure(text='Usuário não cadastrado')
                user_error()
                return False
            elif usuario != 'Usuário já cadastrado':
                retorno.configure(text=usuario)
                user_error()
                return False
            else:
                retorno.configure(text='')
                return True
        
        user_var = StringVar(value='Usuário')
        user_entry = ttk.Entry(tela,
                               textvariable=user_var,
                               style='custom.TEntry'
                               )
        user_entry.place(anchor='center', relx=0.5, rely=0.2, height=59, width=255 )
        user_entry.bind('<FocusIn>',lambda event: (user_var.set(value=''),
                                                         user_entry.unbind('<FocusIn>'),
                                                         user_entry.bind('<KeyRelease>', lambda event: usuario())
                                                         ))

        def email():
            email = cadastro.credenciais(email=email_var.get())
            email = email.Email()
            if email == True:
                retorno.configure(text='E-mail não cadastrado')
                email_error()
                return False
            elif email != 'E-mail já cadastrado':
                retorno.configure(text=email)
                email_error()
                return False
            else:
                retorno.configure(text='')
                return True
        
        
        email_var = StringVar(value='E-mail')
        email_entry = ttk.Entry(tela,
                                textvariable=email_var,
                                style='custom.TEntry')
        email_entry.place(anchor='center', relx=0.5, rely=0.33, height=59, width=255)
        email_entry.bind('<FocusIn>',lambda event: (email_var.set(value=''),
                                                         email_entry.unbind('<FocusIn>'),
                                                         email_entry.bind('<KeyRelease>', lambda event: email())
                                                         ))
        
        def senha(*args):
            senha = cadastro.credenciais(senha=senha_var.get())
            senha = senha.passw()
            if senha != True:
                retorno.configure(text=senha)
                senha_error()
                return False
            else:
                retorno.configure(text='')
                return True
        
        senha_frame = Frame(tela, height=73, width=400)
        senha_frame.place(anchor='center', relx=0.5, rely=0.455)
        senha_frame.lower()
        
        senha_var = StringVar(value='Senha')
        senha_entry = ttk.Entry(senha_frame,
                                textvariable=senha_var,
                                style='custom.TEntry')
        senha_entry.place(anchor='center', relx=0.5, rely=0.53, height=59, width=255)
        senha_entry.bind('<FocusIn>',lambda event: senha_var.set(value=''))
        senha_var.trace('w',lambda *args: esconder_senha())
        
        esconder_senha_imagem = PhotoImage(file = os.path.abspath('data/assets/hide_password.png'))
        ver_senha_imagem = PhotoImage(file = os.path.abspath('data/assets/show_password.png'))
        
        ver_senha=ttk.Button(senha_frame,padding=1, image = esconder_senha_imagem, command=lambda: esconder_senha(ver='ver',entry=senha_entry,entry1=confirmar_senha_entry))
        ver_senha.place(anchor='nw', relx=0.83, rely=0.13)
        
        
        def gerarsenha():
            senha_gerada = cadastro.credenciais()
            senha_gerada = senha_gerada.GerarSenha()
            senha_var.set(value=senha_gerada)
            confirmar_senha_var.set(value=senha_gerada)
            
        gerar_senha_imagem = PhotoImage(file = os.path.abspath('data/assets/generate_password.png'))
        gerar_senha = ttk.Button(senha_frame,padding=1,image = gerar_senha_imagem,command=gerarsenha)
        gerar_senha.place(anchor='nw', relx=0.83, rely=0.58)

        def confirmar_senha(*args):
            confirmar_senha = confirmar_senha_var.get()
            senha = senha_var.get()
            if confirmar_senha != senha:
                retorno.configure(text='As senhas não coincidem')
                return False
            else:
                retorno.configure(text='')
                return True
        
        
        confirmar_senha_var = StringVar(value='Confirmar Senha')
        confirmar_senha_entry = ttk.Entry(tela,
                                          textvariable=confirmar_senha_var,
                                          style='custom.TEntry')
        confirmar_senha_entry.place(anchor='center', relx=0.5, rely=0.595, height=59, width=255)
        confirmar_senha_entry.bind('<FocusIn>',lambda event: confirmar_senha_var.set(value=''))
        
        confirmar_senha_var.trace('w',lambda *args: esconder_senha(entry=confirmar_senha_entry,
                                                                   comando=confirmar_senha))
        
        def esconder_senha(ver='esconder',entry=senha_entry,comando=senha,entry1=''):
            if ver=='esconder':
                entry.unbind('<FocusIn>'),
                entry.configure(show='*')
                entry.bind('<KeyRelease>', comando)
                ver_senha.config(image=esconder_senha_imagem)
                
            elif ver=='ver':
                entry1.configure(show='')
                entry.configure(show='')
                ver_senha.config(image=ver_senha_imagem)
            else:
                return False
        
        def reset():
            if not confirmar_senha():
                retorno.configure(text='As senhas não coincidem')
                senha_error(same=True)
            elif not senha():
                retorno.configure(text='Senha inválida')
                senha_error()
            elif not email():
                retorno.configure(text='E-mail inválido')
                email_error()
            elif not usuario():
                retorno.configure(text='Usuário Inválido')
                user_error()
            else:
                cadastrar = UsuariosFunc.InserirDados(usuario=user_var.get(), email=email_var.get(),senha=senha_var.get())
                cadastrar = cadastrar.alterarSenha()
                retorno.configure(text=cadastrar)
            
        
        confirmar = ttk.Button(tela,
                               style='Estilo1.info.TButton',
                               text='Alterar Senha',
                               command=reset)
        confirmar.place(anchor='center', relx=0.5, rely=0.8, relheight=0.1, relwidth=0.3)
        
        retorno.place(anchor='center', relx=0.5, rely=0.7)
        
        tela.mainloop()