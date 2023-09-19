import secrets
import string
import hashlib
from data import edit_config
from data.users import verificarusuario
from validate_email import validate_email
from data.users import UsuariosFunc

CONFIG = edit_config.LerConfig('config')

CARACTERES_ESPECIAIS = "!#$%&"

TAMANHO_PADRAO_SENHA = 12

TAMANHO_SENHA_INVALIDA = f'''
SENHA deve conter entre 8 e 16 caracteres.
Gerando senha automatica com o tamando de {TAMANHO_PADRAO_SENHA} caracteres.
'''

def GerarSenha(tamanho=12):
    caracteres_validos = string.ascii_letters + string.digits + CARACTERES_ESPECIAIS
    senha_gerada = ''.join(secrets.choice(caracteres_validos) for _ in range(tamanho))
    return senha_gerada

def EncriptarSenha(senha):
    '''Encriptar Senha digitada ou gerada com SHA-256'''
    senha = senha.encode('utf-8')
    senha_encriptada = hashlib.sha256(senha).hexdigest()
    return senha_encriptada


class credenciais:
    def __init__(self, usuario, email, senha):
        self.usuario = usuario
        self.email = email
        self.senha = senha
        
    def passw(self):
        pass
    
    def user(self):
        if len(self.usuario) < 3 and len(self.usuario) > 16:
            return 'Digite um usuário entre 3 e 16 caracteres'
        
        verificar = verificarusuario(self.usuario, self.email, self.senha)
        if verificar.verificarUsuario() == 'usuario_existe':
            return verificar.verificarUsuario()
    
    def Email(self):
        if not validate_email(self.email):
            return "Digite um e-mail válido!"
        
        verificar = verificarusuario(self.usuario, self.email, self.senha)
        if verificar.verificarEmail() == 'email_existe':
            return verificar.verificarEmail()
    
    def cadastrar(self):
        try:
            UsuariosFunc.add(self.usuario,self.email,self.senha)
            return 'sucesso'
        except Exception as e:
            return f'Um erro ocorreu: {e}'

