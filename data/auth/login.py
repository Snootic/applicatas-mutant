from data.auth import cadastro, verificarusuario
from data.edit_config import editUser,editSenha,editSchema,editSecao
from bd import sqlite

def login(usuario,senha,secao=''):
    usuario = usuario.lower()
    if len(senha) > 16:
        verificar = verificarusuario.usuario(usuario=usuario,email=usuario,senha=senha)
    else:
        credenciais = cadastro.credenciais(senha=senha)
        senha_encriptada = credenciais.EncriptarSenha()
        verificar = verificarusuario.usuario(usuario=usuario,email=usuario,senha=senha_encriptada)
    if not verificar.verificarUsuario() and not verificar.verificarEmail():
        return 'Usuário ou E-mail não cadastrados'
    elif not verificar.verificarSenha():
        return 'Senha incorreta'
    else:
        if secao:
            editSenha(senha)
            editSecao('True')
        else:
            editSecao('False')
        editUser(verificar.getUser())
        SCHEMA = sqlite.tabela()
        SCHEMA_ADICIONAL = SCHEMA.CriarDirSchema('medidas')
        SCHEMA = SCHEMA.CriarDirSchema('pareto')
        editSchema(SCHEMA)
        return 'Logado'