import sqlite3, os, sys, analise_pareto_tabela
from pandas import *
# CAMINHO_PROJETO = os.getcwd()
# sys.path.insert(0, CAMINHO_PROJETO)
from data.edit_config import *

ver_tabela = analise_pareto_tabela.pareto()
ver_tabela.sqlite()

""" AAAAAAAAAAAAAAAAAAAAAAAAAA """

