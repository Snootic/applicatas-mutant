# Só de teste, apagar este arquivo mais tarde


import tabela_pareto as tabela_pareto
import adicionar_valores

nome_bd = input('Digite o nome do banco: ')

criar_tabela = tabela_pareto.criar_bd(nome_bd)
if criar_tabela == 'tabela_existe':
    print('Tabela já existe')
else:
    nome_bd = criar_tabela
    
ocorrencia = input('Digite a ocorrencia: ')
numero_ocorrencias = int(input('Digite a quantidade da ocorrencia: '))

for i in range(numero_ocorrencias):
    adicionar_valores.adicionar_valor(nome_bd, ocorrencia)