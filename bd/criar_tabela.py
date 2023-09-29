from bd.tabela_sqlite import *
from data import edit_config

class sql_tabela:
    def criar_tabela(self,nome_tabela):
        tabela_sqlite = tabela(table=nome_tabela)
        criar_tabela = tabela_sqlite.CriarBD()
        return criar_tabela
        
    def adicionar_itens_tabela(self,tabela):
        tabela_sqlite = tabela(table=tabela)
        while True:
            ocorrencia = input('Digite a ocorrencia ("wq" para sair): ')
            if ocorrencia == 'wq':
                break
            else:
                self.tabela_sqlite.addValor(ocorrencia)