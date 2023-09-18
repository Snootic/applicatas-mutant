import sqlite3

usuarios = sqlite3.connect('usuarios.db')
cursor = usuarios.cursor()

class usuario:
    usuario: str
    email: str
    senha: str
    
    def verificarUsuario(self):
        cursor.execute(f'SELECT COUNT(*) FROM credenciais WHERE usuario="{(self.usuario).lower()}"')
        verificar = cursor.fetchone()
        if verificar[0] == 1:
            return 'usuario_existe'
        elif self.usuario == '':
            return 'usuario_invalido'
        
    def verificarEmail(self):
        cursor.execute(f'SELECT COUNT(*) FROM credenciais WHERE usuario="{(self.email).lower()}"')
        verificar = cursor.fetchone()
        if verificar[0] == 1:
            return 'email_existe'
        elif self.email == '':
            return 'email_invalido'
        
    def verificarSenha(self):
        if self.senha == '':
            return 'senha_invalida'