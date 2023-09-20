import sqlite3
import data.auth.verificarusuario as verificarusuario
import data.users.usuarios as usuarios
import os

class InserirDados:
    def __init__(self,usuario='',email='',senha=''):
        self.usuario = usuario
        self.email = email
        self.senha = senha
        CAMINHO_DB = os.path.join(os.getcwd(),f'data/users/usuarios.db')
        self.usuarios = sqlite3.connect(CAMINHO_DB)
        self.cursor = self.usuarios.cursor()

    def add(self):
        try:
            usuarios.user_table()
            self.cursor.execute(f"INSERT INTO credenciais (usuario,email,senha) VALUES(?,?,?)", (self.usuario, self.email, self.senha))
            self.usuarios.commit()
            return True
        except Exception as e:
            self.usuarios.rollback()
            return e
        
    def alterarUser(self):
        user = verificarusuario.usuario(usuario = self.usuario)
        if user != None:
            return user
        else:
            self.cursor.execute(f'UPDATE credenciais SET usuario="{self.usuario}"')
            self.usuarios.commit()
            
    def alterarEmail(self):
        Email = verificarusuario.usuario(email = self.email)
        if Email != None:
            return Email
        else:
            self.cursor.execute(f'UPDATE credenciais SET email="{self.email}"')
            self.usuarios.commit()
            
    def alterarSenha(self):
        password = verificarusuario.usuario(self.senha)
        if password != None:
            return password
        else:
            self.cursor.execute(f'UPDATE credenciais SET senha="{self.senha}"')
            self.usuarios.commit()