
from tkinter import *
import ttkbootstrap as ttk
from app import *
from data.auth import login, cadastro
from telas import telainicial

#TODO: Achar uma forma de trocar cor do texto das label do TTKBOOTSTRAP


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
        
        def logando():
            global inicio
            log = login.login(self.user_var.get(),self.senha_var.get())
            retorno.configure(text=log)
            if log == 'Logado':
                retorno.configure(text='')
                self.senha_entry.destroy()
                self.user_entry.destroy()
                user_entry(self)
                senha_entry(self)
                self.login.withdraw()
                inicio = telainicial.inicio(self.login)
        
        logar_var = StringVar(value='Entrar')
        logar = ttk.Button(self.login,
                           width=38,
                           textvariable=logar_var,
                           style='Estilo1.info.TButton',
                           command=logando)
        logar.place(x=300,y=400,anchor='center', height=70)
        
        texto_secao_var = StringVar(value='Manter seção')
        manter_secao_var= BooleanVar(value=False)
        manter_secao = ttk.Checkbutton(self.login,
                                       var=manter_secao_var,
                                       textvariable=texto_secao_var,
                                       style='TCheckbutton',
                                       bootstyle='info')
        # manter_secao.configure(font='Nexa 11')
        manter_secao.place(x=165,y=460,anchor='center')
        
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
        
        self.login.mainloop()
        
        
    def registro(self):
        registro = ttk.Toplevel(self.login)
        registro.geometry('500x500')
        registro.resizable(False, False)
        registro.title('Registrar-se')

        titulo = Label(registro, text='Registrar-se', font='Nexa 20')
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
        email_entry.pack(ipady=15,pady=5)
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
        
        senha_frame = Frame(registro)
        senha_frame.pack()
                   
        senha_var = StringVar(value='Senha')
        senha_entry = ttk.Entry(senha_frame,
                                font=self.estilo.fonte,
                                textvariable=senha_var,
                                width=30)
        senha_entry.pack(ipady=15,pady=5,padx=(0,0),side='left')
        senha_entry.bind('<FocusIn>',lambda event: senha_var.set(value=''))
        senha_var.trace('w',lambda *args: esconder_senha())
        
        ver_senha=ttk.Button(senha_frame,width=2,command=lambda: esconder_senha(ver='ver',entry=senha_entry,entry1=confirmar_senha_entry))
        ver_senha.pack(before=senha_entry,side='left',padx=(0,5))
        
        def gerarsenha():
            senha_gerada = cadastro.credenciais()
            senha_gerada = senha_gerada.GerarSenha()
            senha_var.set(value=senha_gerada)
            confirmar_senha_var.set(value=senha_gerada)
            
        
        gerar_senha = ttk.Button(senha_frame,width=2,command=gerarsenha)
        gerar_senha.pack(padx=(5,0),side='right')

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
                
            elif ver=='ver':
                entry1.configure(show='')
                entry.configure(show='')
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
