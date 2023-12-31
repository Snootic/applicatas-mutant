import sqlite3
import data.users.usuarios as usuarios
import os

class usuario:
    def __init__(self, usuario='', email='', senha=''):
        CAMINHO_DB = os.path.join(os.getcwd(),f'data/users/usuarios.db')
        usuarios.user_table()
        Usuarios = sqlite3.connect(CAMINHO_DB)
        self.cursor = Usuarios.cursor()
        self.usuario = usuario
        self.email = email
        self.senha = senha
    
    def verificarUsuario(self):
        """Verifica o usuário digitado já está cadastrado
        """
        self.cursor.execute(f'SELECT COUNT(usuario) FROM credenciais WHERE usuario="{(self.usuario).lower()}"')
        verificar = self.cursor.fetchone()
        if verificar[0] == 1:
            return True
        else:
            return False
        
    def verificarEmail(self):
        """Verifica se o email digitado já está cadastrado
        """
        self.cursor.execute(f'SELECT COUNT(email) FROM credenciais WHERE email="{(self.email).lower()}"')
        verificar = self.cursor.fetchone()
        if verificar[0] == 1:
            return True
        else:
            return False
        
    def verificarSenha(self):
        '''Verifica se a senha digitada está correta
        
        Returns:
            'senha inválida': Senha digitada não é igual a cadastrada
        '''
        self.cursor.execute(f'SELECT senha FROM credenciais WHERE senha="{self.senha}"')
        verificar = self.cursor.fetchone()
        if verificar == None or self.senha != verificar[0]:
            return False
        else:
            return True
        
    def getUser(self):
        ''' Retorna o usuário indicado '''
        self.cursor.execute(f'SELECT usuario FROM credenciais WHERE email="{(self.email).lower()}"')
        usuario = self.cursor.fetchone()
        if usuario != None:
            return usuario[0]
        else:
            self.cursor.execute(f'SELECT usuario FROM credenciais WHERE usuario="{(self.usuario).lower()}"')
            usuario = self.cursor.fetchone()
            return usuario[0]