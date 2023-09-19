import os
import sys
from tkinter import *
import ttkbootstrap as ttk
CAMINHO_PROJETO = os.getcwd()
sys.path.insert(0, CAMINHO_PROJETO)
from app import *
from data.auth import login

#TODO: Achar uma forma de trocar cor do texto das label do TTKBOOTSTRAP


class login:
    def __init__(self):
        login = ttk.Window()
        tela = Tela(login, 'Peraeque - Login')
        tela.centralizarTela(600,600)
        login.resizable(False,False)
        
        estilo = Estilo()

        titulo = ttk.Label(login, text='Applicatas Mutant', style='Titulo.TLabel')
        subtitulo = ttk.Label(login, text='Bem vindo! Faça login para continuar', style='Comum.TLabel')
        titulo.place(relx=0.315, rely=0.08)
        subtitulo.place(relx=0.28, rely=0.14)
        
        user_var = StringVar(value='Usuário / E-mail')
        user_entry = ttk.Entry(login, textvariable=user_var, width=39, font=estilo.fonte)
        user_entry.place(relx=0.2,rely=0.3, height=60)
        user_entry.bind('<ButtonRelease>',lambda event: (user_var.set(value=''),user_entry.unbind('<ButtonRelease>')))
        
        senha_var = StringVar(value='Senha')
        senha_entry = ttk.Entry(login, textvariable=senha_var, width=39, font=estilo.fonte)
        senha_entry.place(relx=0.2,rely=0.45, height=60)
        senha_entry.bind('<ButtonRelease>',lambda event: (senha_var.set(value=''),senha_entry.unbind('<ButtonRelease>'),senha_entry.configure(show='*')))
        
        logar_var = StringVar(value='Entrar')
        logar = ttk.Button(login, width=38, textvariable=logar_var, style='Estilo1.info.TButton')
        logar.place(relx=0.2, rely=0.6, height=70)
        
        texto_secao_var = StringVar(value='Manter seção')
        manter_secao_var= BooleanVar(value=False)
        manter_secao = ttk.Checkbutton(login, var=manter_secao_var, textvariable=texto_secao_var, style='TCheckbutton', bootstyle='info')
        # manter_secao.configure(font='Nexa 11')
        manter_secao.place(relx=0.2, rely=0.76)
        
        esqueci_senha_var = StringVar(value='Esqueci minha senha')
        esqueci_senha = ttk.Button(login, textvariable=esqueci_senha_var, style='Estilo1.Link.TButton')
        esqueci_senha.place(relx=0.58, rely=0.75)
        
        registrar_label = ttk.Label(text='Não tem conta?', style='Comum.TLabel')
        registrar = ttk.Button(login, text='Registre-se aqui', style='Estilo2.Link.TButton')
        registrar_label.place(relx=0.3,rely=0.9)
        registrar.place(relx=0.495, rely=0.892)
        
        login.mainloop()
        
    def registro():
        pass