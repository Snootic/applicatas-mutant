import sqlite3
import os

class user_table:
    def __init__(self):
        if not os.path.exists('data/users'):
            os.makedirs('data/users')
        CAMINHO_DB = os.path.join(os.getcwd(),f'data/users/usuarios.db')
        usuarios = sqlite3.connect(CAMINHO_DB)
        cursor = usuarios.cursor()

        cursor.execute('''CREATE TABLE if not exists credenciais(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario VARCHAR UNIQUE,
        email VARCHAR UNIQUE,
        senha VARCHAR)''')
        usuarios.close()
        