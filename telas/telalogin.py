import os
import sys
from tkinter import *
import ttkbootstrap as ttk
CAMINHO_PROJETO = os.getcwd()
sys.path.insert(0, CAMINHO_PROJETO)
from app import *
from data.auth import login, cadastro

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
        titulo.place(relx=0.315, rely=0.08)
        subtitulo.place(relx=0.28, rely=0.14)
        
        user_var = StringVar(value='Usuário / E-mail')
        user_entry = ttk.Entry(self.login,
                               textvariable=user_var,
                               width=39,
                               font=self.estilo.fonte)
        user_entry.place(relx=0.2,rely=0.3, height=60)
        user_entry.bind('<ButtonRelease>',lambda event: (user_var.set(value=''),
                                                         user_entry.unbind('<ButtonRelease>')))
        
        senha_var = StringVar(value='Senha')
        senha_entry = ttk.Entry(self.login, textvariable=senha_var, width=39, font=self.estilo.fonte)
        senha_entry.place(relx=0.2,rely=0.45, height=60)
        senha_entry.bind('<ButtonRelease>',lambda event: (senha_var.set(value=''),
                                                          senha_entry.unbind('<ButtonRelease>'),
                                                          senha_entry.configure(show='*')))
        
        logar_var = StringVar(value='Entrar')
        logar = ttk.Button(self.login,
                           width=38,
                           textvariable=logar_var,
                           style='Estilo1.info.TButton')
        logar.place(relx=0.2, rely=0.6, height=70)
        
        texto_secao_var = StringVar(value='Manter seção')
        manter_secao_var= BooleanVar(value=False)
        manter_secao = ttk.Checkbutton(self.login,
                                       var=manter_secao_var,
                                       textvariable=texto_secao_var,
                                       style='TCheckbutton',
                                       bootstyle='info')
        # manter_secao.configure(font='Nexa 11')
        manter_secao.place(relx=0.2, rely=0.76)
        
        esqueci_senha_var = StringVar(value='Esqueci minha senha')
        esqueci_senha = ttk.Button(self.login,
                                   textvariable=esqueci_senha_var,
                                   style='Estilo1.Link.TButton')
        esqueci_senha.place(relx=0.58, rely=0.75)
        
        registrar_label = ttk.Label(text='Não tem conta?',
                                    style='Comum.TLabel')
        registrar = ttk.Button(self.login, text='Registre-se aqui',
                               style='Estilo2.Link.TButton',
                               command=self.registro)
        registrar_label.place(relx=0.3,rely=0.9)
        registrar.place(relx=0.495, rely=0.892)
        
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
            else:
                retorno.configure(text='')
        
        user_var = StringVar(value='Usuário')
        user_entry = ttk.Entry(registro,
                               font=self.estilo.fonte,
                               textvariable=user_var,
                               width=39,
                               )
        user_entry.pack(ipady=15,pady=5)
        user_entry.bind('<ButtonRelease>',lambda event: (user_var.set(value=''),
                                                         user_entry.unbind('<ButtonRelease>'),
                                                         user_entry.bind('<KeyRelease>', lambda event: usuario())
                                                         ))

        def email():
            email = cadastro.credenciais(email=email_var.get())
            email = email.Email()
            if email != True:
                retorno.configure(text=email)
            else:
                retorno.configure(text='')
        
        
        email_var = StringVar(value='E-mail')
        email_entry = ttk.Entry(registro,
                                font=self.estilo.fonte,
                                textvariable=email_var,
                                width=39)
        email_entry.pack(ipady=15,pady=5)
        email_entry.bind('<ButtonRelease>',lambda event: (email_var.set(value=''),
                                                         email_entry.unbind('<ButtonRelease>'),
                                                         email_entry.bind('<KeyRelease>', lambda event: email())
                                                         ))
        
        def senha():
            senha = cadastro.credenciais(senha=senha_var.get())
            senha = senha.passw()
            if senha != True:
                retorno.configure(text=senha)
            else:
                retorno.configure(text='')
        
        
        senha_var = StringVar(value='Senha')
        senha_entry = ttk.Entry(registro,
                                font=self.estilo.fonte,
                                textvariable=senha_var,
                                width=39)
        senha_entry.pack(ipady=15,pady=5)
        senha_entry.bind('<ButtonRelease>',lambda event: (senha_var.set(value=''),
                                                          senha_entry.unbind('<ButtonRelease>'),
                                                          senha_entry.configure(show='*'),
                                                          senha_entry.bind('<KeyRelease>', lambda event: senha())
                                                          ))

        confirmar_senha_var = StringVar(value='Confirmar Senha')
        confirmar_senha_entry = ttk.Entry(registro,
                                          font=self.estilo.fonte,
                                          textvariable=confirmar_senha_var,
                                          width=39)
        confirmar_senha_entry.pack(ipady=15,pady=5)
        confirmar_senha_entry.bind('<ButtonRelease>',lambda event: (confirmar_senha_var.set(value=''),
                                                                    confirmar_senha_entry.unbind('<ButtonRelease>'),
                                                                    confirmar_senha_entry.configure(show='*')
                                                                    ))
        
        def cadastrar():
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
