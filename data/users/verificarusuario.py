import sqlite3

usuarios = sqlite3.connect('usuarios.db')
cursor = usuarios.cursor()

class usuario:
    usuario: str
    email: str
    senha: str
    
    def verificarUsuario(self):
        """Verifica o usuário digitado é válido

        Returns:
            'usuario_existe': usuario já está cadastrado
            'usuario_invalido': total de caracteres de usuario < 3 OU > 16
        """
        cursor.execute(f'SELECT COUNT(*) FROM credenciais WHERE usuario="{(self.usuario).lower()}"')
        verificar = cursor.fetchone()
        if verificar[0] == 1:
            return 'usuario_existe'
        elif self.usuario == '':
            return 'usuario_invalido'
        
    def verificarEmail(self):
        """Verifica se o email digitado é valido
        
        Returns:
            'email_invalido': email digitado não é atende requisitos mínimos
            'email_existe': email digitado já está cadastrado
        """
        cursor.execute(f'SELECT COUNT(*) FROM credenciais WHERE usuario="{(self.email).lower()}"')
        verificar = cursor.fetchone()
        if verificar[0] == 1:
            return 'email_existe'
        elif self.email == '':
            return 'email_invalido'
        
    def verificarSenha(self):
        '''Verifica se a senha digitada atende os requisitos de senha
        
        Returns:
            'senha_inválida': Senha digitada não atende requisitos
        '''
        if self.senha == '':
            return 'senha_invalida'