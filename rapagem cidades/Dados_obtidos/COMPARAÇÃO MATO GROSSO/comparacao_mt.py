import pandas as pd
Dados_alunos = pd.read_csv("/home/henrique/Área de Trabalho/Programação em geral/LAPES/Estado/raspagem MT/rapagem cidades/Dados_obtidos/arquivo_alunos.csv", sep=',')
# Ler o arquivo original
df = pd.read_csv('dados_mt.csv', header=None)

# Criar um novo DataFrame com a linha que você quer adicionar
nova_linha = pd.DataFrame([['MATRICULA', 'FICHA', 'SERVIDOR', 'DATA DE EXERCÍCIO', 'DATA DA VACÂNCIA', 'FOLHA', 'ÓRGÃO', 'VANTAGENS', 'DEDUÇÕES', 'PÓS DEDUÇÕES']], columns=df.columns)

# Concatenar o novo DataFrame com o original
df = pd.concat([nova_linha, df])
Dados_servidores_mt = df
