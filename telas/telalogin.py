from tkinter import *
import ttkbootstrap as ttk
from telas.app import *
from data.auth import login, cadastro
from telas import telainicial
from data.edit_config import getUser, getSenha
import os

#TODO:
# melhorar a segurança do login automatico
# mudar a cor das bordas das entry em caso de erro


class telalogin:
    def __init__(self):
        self.login = ttk.Window()
        tela = Tela(self.login, 'Peraeque - Login')
        tela.centralizarTela(600,600)
        self.login.resizable(False,False)
        
        self.estilo = Estilo()

        titulo = ttk.Label(self.login,
                           text='Applicatas Mutant',
                           style='Titulo.TLabel')
        subtitulo = ttk.Label(self.login,
                              text='Bem vindo! Faça login para continuar',
                              style='Comum.TLabel')
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
                                width=39,
                                font=self.estilo.fonte)
            self.user_entry.place(x=300,y=200,anchor='center', height=60)
            self.user_entry.bind('<FocusIn>',lambda event: (self.user_var.set(value=''),
                                                            self.user_entry.unbind('<FocusIn>')))
        def senha_entry(self):
            self.senha_var = StringVar(value='Senha')
            self.senha_entry = ttk.Entry(self.login, textvariable=self.senha_var, width=39, font=self.estilo.fonte)
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
            if log == 'Logado':
                retorno.configure(text='')
                self.senha_entry.destroy()
                self.user_entry.destroy()
                self.manter_secao_var.set(value=False)
                user_entry(self)
                senha_entry(self)
                self.login.withdraw()
                inicio = telainicial.inicio(self.login)
                
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
                                   style='Estilo1.Link.TButton')
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
             
    def registro(self):
        registro = ttk.Toplevel(self.login)
        registro.geometry('400x500')
        registro.resizable(False, False)
        registro.title('Registrar-se')

        titulo = ttk.Label(registro, text='Registrar-se', font='Nexa 20')
        titulo.pack(pady=20)
        
        retorno = ttk.Label(registro, style='Comum.TLabel', text='')

        def usuario():
            usuario = cadastro.credenciais(usuario=user_var.get())
            usuario = usuario.user()
            if usuario != True:
                retorno.configure(text=usuario)
                return False
            else:
                retorno.configure(text='')
                return True
        
        user_var = StringVar(value='Usuário')
        user_entry = ttk.Entry(registro,
                               font=self.estilo.fonte,
                               textvariable=user_var,
                               width=30,
                               )
        user_entry.pack(ipady=15,pady=5)
        user_entry.bind('<FocusIn>',lambda event: (user_var.set(value=''),
                                                         user_entry.unbind('<FocusIn>'),
                                                         user_entry.bind('<KeyRelease>', lambda event: usuario())
                                                         ))

        def email():
            email = cadastro.credenciais(email=email_var.get())
            email = email.Email()
            if email != True:
                retorno.configure(text=email)
                return False
            else:
                retorno.configure(text='')
                return True
        
        
        email_var = StringVar(value='E-mail')
        email_entry = ttk.Entry(registro,
                                font=self.estilo.fonte,
                                textvariable=email_var,
                                width=30)
        email_entry.pack(ipady=15,pady=(5,0))
        email_entry.bind('<FocusIn>',lambda event: (email_var.set(value=''),
                                                         email_entry.unbind('<FocusIn>'),
                                                         email_entry.bind('<KeyRelease>', lambda event: email())
                                                         ))
        
        def senha(*args):
            senha = cadastro.credenciais(senha=senha_var.get())
            senha = senha.passw()
            if senha != True:
                retorno.configure(text=senha)
                return False
            else:
                retorno.configure(text='')
                return True
        
        senha_frame = Frame(registro, height=73, width=400)
        senha_frame.pack()
        
        senha_var = StringVar(value='Senha')
        senha_entry = ttk.Entry(senha_frame,
                                font=self.estilo.fonte,
                                textvariable=senha_var,)
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
        confirmar_senha_entry = ttk.Entry(registro,
                                          font=self.estilo.fonte,
                                          textvariable=confirmar_senha_var,
                                          width=30)
        confirmar_senha_entry.pack(ipady=15,pady=5)
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
        
        def cadastrar():
            if not confirmar_senha():
                retorno.configure(text='As senhas não coincidem')
            elif not senha():
                retorno.configure(text='Senha inválida')
            elif not email():
                retorno.configure(text='E-mail inválido')
            elif not usuario():
                retorno.configure(text='Usuário Inválido')
            else:
                cadastrar = cadastro.credenciais(user_var.get(),email_var.get(),senha_var.get())
                cadastrar = cadastrar.cadastrar()
                retorno.configure(text=cadastrar)
            
        
        confirmar = ttk.Button(registro,
                               style='Estilo1.info.TButton',
                               width=20,
                               text='Registrar',
                               command=cadastrar)
        confirmar.pack(ipady=10,pady=5)
        
        retorno.pack(before=confirmar)
        
        registro.mainloop()
