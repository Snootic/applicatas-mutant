import sqlite3
import os
import platform

class user_table:
    def __init__(self):
        if platform.system() == 'Windows':
            CAMINHO_DB = os.path.join(os.getcwd(),'data\\users\\usuarios.db')
        else:
            CAMINHO_DB = os.path.join(os.getcwd(),f'data/users/usuarios.db')
        usuarios = sqlite3.connect(CAMINHO_DB)
        cursor = usuarios.cursor()

        cursor.execute('''CREATE TABLE if not exists credenciais(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario VARCHAR UNIQUE,
        email VARCHAR UNIQUE,
        senha VARCHAR)''')
        usuarios.close()
        