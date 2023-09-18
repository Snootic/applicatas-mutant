import sqlite3
import verificarusuario

usuarios = sqlite3.connect('usuarios.db')
cursor = usuarios.cursor()

def add(usuario,email,senha):
    cursor.execute(f'INSERT INTO credenciais (usuario,email,senha) VALUES({usuario},{email},{senha})')
    usuarios.commit()
    
def alterarUser(usuario):
    user = verificarusuario.usuario(usuario, '', '')
    if user != None:
        return user
    else:
        cursor.execute(f'UPDATE credenciais SET usuario="{usuario}"')
        
def alterarEmail(email):
    Email = verificarusuario.usuario(email, '', '')
    if Email != None:
        return Email
    else:
        cursor.execute(f'UPDATE credenciais SET email="{email}"')
        
def alterarSenha(senha):
    password = verificarusuario.usuario(senha, '', '')
    if password != None:
        return password
    else:
        cursor.execute(f'UPDATE credenciais SET senha="{senha}"')