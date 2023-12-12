import sqlite3
import data.auth.verificarusuario as verificarusuario
import data.users.usuarios as usuarios
import os, hashlib

class InserirDados:
    def __init__(self,usuario='',email='',senha='', old_user='', old_email=''):
        self.usuario = usuario
        self.email = email
        self.senha = senha
        self.old_user = old_user
        self.old_email = old_email
        CAMINHO_DB = os.path.join(os.getcwd(),f'data/users/usuarios.db')
        self.usuarios = sqlite3.connect(CAMINHO_DB)
        self.cursor = self.usuarios.cursor()

    def add(self):
        try:
            usuarios.user_table()
            self.cursor.execute(f"INSERT INTO credenciais (usuario,email,senha) VALUES(?,?,?)", (self.usuario.lower(), self.email.lower(), self.senha))
            self.usuarios.commit()
            return True
        except Exception as e:
            self.usuarios.rollback()
            return e
        
    def alterarUser(self):
        user = verificarusuario.usuario(usuario = self.usuario)
        if user == None:
            return user
        else:
            self.cursor.execute(f'UPDATE credenciais SET usuario="{self.usuario}" WHERE usuario="{self.old_user}"')
            self.usuarios.commit()
            return 'Usuário alterado com sucesso'
            
    def alterarEmail(self):
        Email = verificarusuario.usuario(email = self.email)
        if Email == None:
            return Email
        else:
            self.cursor.execute(f'UPDATE credenciais SET email="{self.email}" WHERE email="{self.old_email}"')
            self.usuarios.commit()
            return 'E-mail Alterado com sucesso'
            
    def alterarSenha(self):
        senha = self.senha.encode('utf-8')
        senha = hashlib.sha256(senha).hexdigest()
        self.cursor.execute(f'UPDATE credenciais SET senha="{senha}" WHERE usuario="{self.usuario}" AND email="{self.email}"')
        self.usuarios.commit()
        return 'Senha alterada com suceso'
    
    def rename_database(self):
        old_user_path = os.path.abspath(f'data/users/sqlite_databases/{self.old_user}')
        old_user_pareto = os.path.abspath(f'data/users/sqlite_databases/{self.old_user}/{self.old_user}_pareto.db')
        old_user_medidas = os.path.abspath(f'data/users/sqlite_databases/{self.old_user}/{self.old_user}_medidas.db')
        
        new_user_path = os.path.abspath(f'data/users/sqlite_databases/{self.usuario}')
        new_user_pareto = os.path.abspath(f'data/users/sqlite_databases/{self.old_user}/{self.usuario}_pareto.db')
        new_user_medidas = os.path.abspath(f'data/users/sqlite_databases/{self.old_user}/{self.usuario}_medidas.db')
        
        try:    
            os.rename(old_user_pareto,new_user_pareto)
            os.rename(old_user_medidas,new_user_medidas)
            os.rename(old_user_path,new_user_path)
        except Exception as e:
            print(e)
            print(os.path.exists(old_user_path), os.path.exists(old_user_pareto), os.path.exists(old_user_medidas))
    
class getDados:
    def __init__(self,usuario=''):
        self.usuario = usuario
        CAMINHO_DB = os.path.join(os.getcwd(),f'data/users/usuarios.db')
        self.usuarios = sqlite3.connect(CAMINHO_DB)
        self.cursor = self.usuarios.cursor()
    
    def get_email(self):
        self.cursor.execute(f'SELECT email FROM credenciais WHERE usuario="{self.usuario}"')
        resultado = self.cursor.fetchone()
        return resultado
    
class deleteDados:
    def __init__(self,usuario=''):
        self.usuario = usuario
        CAMINHO_DB = os.path.join(os.getcwd(),f'data/users/usuarios.db')
        self.usuarios = sqlite3.connect(CAMINHO_DB)
        self.cursor = self.usuarios.cursor()
        
    def delete_user(self):
        self.cursor.execute(f'DELETE FROM credenciais WHERE usuario="{self.usuario}"')
        self.usuarios.commit()
        return 'Deletado com sucesso'
    
    def delete_databases(self):
        os.remove(os.path.abspath(f'data/users/sqlite_databases/{self.usuario}/{self.usuario}_pareto.db'))
        os.remove(os.path.abspath(f'data/users/sqlite_databases/{self.usuario}/{self.usuario}_medidas.db'))
        os.removedirs(os.path.abspath(f'data/users/sqlite_databases/{self.usuario}'))
        return 'deletado'