from data.auth import cadastro, verificarusuario
from data.edit_config import editUser,editSenha,editSchema
from bd import sqlite

def login(usuario,senha,secao=''):
    if len(senha) > 16:
        verificar = verificarusuario.usuario(usuario=usuario,email=usuario,senha=senha)
    else:
        credenciais = cadastro.credenciais(senha=senha)
        senha_encriptada = credenciais.EncriptarSenha()
        verificar = verificarusuario.usuario(usuario=usuario,email=usuario,senha=senha_encriptada)
    if verificar.verificarUsuario() and verificar.verificarEmail():
        return 'Usuário ou E-mail não cadastrados'
    elif not verificar.verificarSenha():
        return 'Senha incorreta'
    else:
        if secao:
            editSenha(senha_encriptada)
        editUser(usuario)
        SCHEMA = sqlite.tabela()
        SCHEMA = SCHEMA.CriarDirSchema()
        editSchema(SCHEMA)
        return 'Logado'