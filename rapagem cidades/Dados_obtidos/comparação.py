# 1 parte


#Dados alunos do IFMT 2020 a 2024
import pandas as pd

urls_alunos = [
    "https://dados.ifmt.edu.br/dataset/6b7c7c38-587a-436b-a7b2-4e3ca59d1ca8/resource/fc30244a-166d-4830-a66d-a573ebe187eb/download/aluno.csv",  # 2020
    "https://dados.ifmt.edu.br/dataset/6b7c7c38-587a-436b-a7b2-4e3ca59d1ca8/resource/d2a472aa-3a02-4d45-bc65-5852fa9be664/download/aluno.csv",  # 2021
    "https://dados.ifmt.edu.br/dataset/6b7c7c38-587a-436b-a7b2-4e3ca59d1ca8/resource/96f114e2-58f9-4f59-9c44-f59814c0b264/download/aluno.csv",  # 2022
    "https://dados.ifmt.edu.br/dataset/6b7c7c38-587a-436b-a7b2-4e3ca59d1ca8/resource/1535c8e2-f1c4-4dcf-9948-dc734522d040/download/aluno.csv",  # 2023
    "https://dados.ifmt.edu.br/dataset/6b7c7c38-587a-436b-a7b2-4e3ca59d1ca8/resource/9513092b-ad4a-4e70-a806-b65618fcd102/download/aluno.csv",  # 2024
]

# Lista para armazenar cada DataFrame
dfs = []

for url in urls_alunos:
    # Lê o arquivo .csv da URL
    df = pd.read_csv(url)

    # Altera o cabeçalho para caixa alta
    df.columns = df.columns.str.upper()

    # Adiciona o DataFrame à lista
    dfs.append(df)

# Concatena todos os DataFrames
df_concatenado = pd.concat(dfs)

# Remove as duplicatas
df_concatenado = df_concatenado.drop_duplicates()

# Escreve o DataFrame de volta para o arquivo .csv
df_concatenado.to_csv('arquivo_alunos.csv', index=False)


# 2 parte


# Comparação de arquivos de servidores dos municipios
import pandas as pd

# Lista de arquivos .csv para concatenar
arquivos = [
    "Raspagem_Dados_Alta_Floresta.csv",
    "Raspagem_Dados_Campo_Verde.csv",
    "Raspagem_Dados_Diamantino.csv"
    ]

# Cria uma lista de DataFrames
dfs = [pd.read_csv(arquivo) for arquivo in arquivos]

# Concatena os DataFrames
df_concatenado = pd.concat(dfs)

# Remove as linhas duplicadas
df_concatenado = df_concatenado.drop_duplicates()

# Escreve o DataFrame resultante em um novo arquivo .csv
df_concatenado.to_csv('arquivo_concatenado.csv', index=False)


#3 parte

import pandas as pd

# Lê os arquivos .csv
ALUNOS = pd.read_csv('arquivo_alunos.csv', sep=',')
SERVIDORES = pd.read_csv('arquivo_concatenado_sem_duplicidades.csv', sep=';')

# Imprime os nomes das colunas de cada DataFrame
print("Colunas em ALUNOS: ", ALUNOS.columns)
print("Colunas em SERVIDORES: ", SERVIDORES.columns)

# Encontra as linhas duplicadas
duplicados = pd.merge(ALUNOS, SERVIDORES, how='inner', on='NOME')
duplicados = duplicados.drop_duplicates()

# Escreve as linhas duplicadas em um novo arquivo .csv
duplicados.to_csv('servidores_alunos3.csv', index=False)




