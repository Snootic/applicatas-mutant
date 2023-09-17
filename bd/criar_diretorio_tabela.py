import os
def criar_diretorio_tabela(nome_tabela): 
    diretorio_script = os.path.dirname(os.path.abspath(__file__))
    caminho_pasta_bd = os.path.join(diretorio_script,'tabelas')
    
    if not os.path.exists(caminho_pasta_bd):
        os.mkdir(caminho_pasta_bd)
        
    banco_de_dados = nome_tabela+'.db'
    caminho_bd = os.path.join(caminho_pasta_bd,banco_de_dados)
    return caminho_bd
    