import sqlite3

usuarios = sqlite3.connect('usuarios.db')
cursor = usuarios.cursor()

cursor.execute('''CREATE TABLE if not exists credenciais(
id INTEGER PRIMARY KEY AUTOINCREMENT,
usuario VARCHAR UNIQUE,
email VARCHAR UNIQUE,
senha VARCHAR)''')