import secrets
import string
import hashlib
from data import edit_config
from data.auth import verificarusuario
from validate_email import validate_email
from data.users import UsuariosFunc

class credenciais:
    def __init__(self, usuario='', email='', senha=''):
        self.CONFIG = edit_config.LerConfig('config')

        self.CARACTERES_ESPECIAIS = "!#$%&"

        TAMANHO_PADRAO_SENHA = 12

        self.TAMANHO_SENHA_INVALIDA = f'''
        SENHA deve conter entre 8 e 16 caracteres.
        Gerando senha automatica com o tamando de {TAMANHO_PADRAO_SENHA} caracteres.
        '''
        
        self.usuario = usuario
        self.email = email
        self.senha = senha
        
    def GerarSenha(self,tamanho=12):
        caracteres_validos = string.ascii_letters + string.digits + self.CARACTERES_ESPECIAIS
        senha_gerada = ''.join(secrets.choice(caracteres_validos) for _ in range(tamanho))
        return senha_gerada

    def EncriptarSenha(self,senha):
        '''Encriptar Senha digitada ou gerada com SHA-256'''
        senha = senha.encode('utf-8')
        senha_encriptada = hashlib.sha256(senha).hexdigest()
        return senha_encriptada
        
    def passw(self):
        for caracter in self.senha:
            if caracter not in (self.CARACTERES_ESPECIAIS + string.ascii_letters + string.digits):
                return 'Caracteres inválidos! Caracteres especiais aceitos: !#$%&'
            
        if len(self.senha) < 8 or len(self.senha) > 16:
            return 'Digite uma senha entre 8 e 16 caracteres'
        else:
            return True
    
    def user(self):
        if len(self.usuario) < 3 or len(self.usuario) > 16:
            return 'Digite um usuário entre 3 e 16 caracteres'
        
        verificar = verificarusuario.usuario(self.usuario, self.email, self.senha)
        if not verificar.verificarUsuario():
            return 'Usuário já cadastrado'
        else:
            return True
        
    def Email(self):
        if not validate_email(self.email):
            return "Digite um e-mail válido!"
        
        verificar = verificarusuario.usuario(self.usuario, self.email, self.senha)
        if not verificar.verificarEmail():
            return 'E-mail já cadastrado'
        else:
            return True
    
    def cadastrar(self):
        senha_encriptada = self.EncriptarSenha(self.senha)
        add = UsuariosFunc.InserirDados(usuario=self.usuario,email=self.email,senha=senha_encriptada)
        add = add.add()
        if add == True:
            return 'Sucesso'
        else:
            if add == 'UNIQUE constraint failed: credenciais.email':
                return 'Email já está cadastrado'
            elif add == 'UNIQUE constraint failed: credenciais.usuario':
                return 'Usuário já está cadastrado'
            return f'Um erro ocorreu: {add}'

