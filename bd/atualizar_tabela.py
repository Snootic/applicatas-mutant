import sqlite3, os, sys, analise_pareto_tabela
from pandas import *
caminnho_projeto = os.getcwd()
sys.path.insert(0, caminnho_projeto)
from data.edit_config import *

ver_tabela = analise_pareto_tabela.pareto()
ver_tabela.sqlite()

""" AAAAAAAAAAAAAAAAAAAAAAAAAA """

