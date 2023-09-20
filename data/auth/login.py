from data.auth import cadastro, verificarusuario

def login(usuario,senha):
    credenciais = cadastro.credenciais(senha=senha)
    senha_encriptada = credenciais.EncriptarSenha()
    verificar = verificarusuario.usuario(usuario=usuario,email=usuario,senha=senha_encriptada)
    if verificar.verificarUsuario() and verificar.verificarEmail():
        return 'Usuário ou E-mail não cadastrados'
    elif not verificar.verificarSenha():
        return 'Senha incorreta'
    else:
        return 'Logado'