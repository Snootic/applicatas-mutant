import sqlite3

usuarios = sqlite3.connect('usuarios.db')
cursor = usuarios.cursor()

class usuario:
    usuario: str
    email: str
    senha: str
    
    def verificarUsuario(self):
        """Verifica o usuário digitado já está cadastrado

        Returns:
            'usuario_existe': usuario já está cadastrado
        """
        cursor.execute(f'SELECT COUNT(usuario) FROM credenciais WHERE usuario="{(self.usuario).lower()}"')
        verificar = cursor.fetchone()
        if verificar[0] == 1:
            return 'usuario_existe'
        else:
            pass
        
    def verificarEmail(self):
        """Verifica se o email digitado já está cadastrado
        
        Returns:
            'email_invalido': email digitado não é atende requisitos mínimos
            'email_existe': email digitado já está cadastrado
        """
        cursor.execute(f'SELECT COUNT(email) FROM credenciais WHERE usuario="{(self.email).lower()}"')
        verificar = cursor.fetchone()
        if verificar[0] == 1:
            return 'email_existe'
        else:
            pass
        
    def verificarSenha(self):
        '''Verifica se a senha digitada está correta
        
        Returns:
            'senha_inválida': Senha digitada não é igual a cadastrada
        '''
        cursor.execute(f'SELECT senha FROM credenciais WHERE senha="{self.senha}"')
        verificar = cursor.fetchone()
        if self.senha != verificar[0]:
            return 'senha_invalida'