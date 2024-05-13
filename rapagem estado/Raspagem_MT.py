from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd

# Inicialize o driver
driver = webdriver.Chrome()

# Lista para armazenar os dados raspados
dados = []
url = 'https://consultas.transparencia.mt.gov.br/pessoal/servidores_ativos/resultado_1.php?pg=1&mes=1&ano=2024'
driver.get(url)
try:
    # Encontre o elemento que contém o número total de páginas
    total_paginas_element = driver.find_element(By.XPATH, '/html/body/div[1]/div[5]/div/nav/ul/li[8]/a')
    total_paginas = int(total_paginas_element.text)

    # Loop para navegar pelas páginas
    pagina_atual = 1
    while pagina_atual <= total_paginas:
        print(f'Raspando página {pagina_atual} de {total_paginas}...')

        # Encontre a tabela na página
        # Aguarde até que a tabela seja carregada
        tabela = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, 'table')))

        # Encontre todas as linhas da tabela
        linhas = tabela.find_elements(By.TAG_NAME, 'tr')

        dados = []
        for linha in linhas:
            # Encontre todas as células dentro da linha
            celulas = linha.find_elements(By.TAG_NAME, 'td')

            # Para cada linha, obtenha o texto de cada célula e adicione-o à lista de dados
            dados_linha = [celula.text for celula in celulas]
            dados.append(dados_linha)

        # Crie um DataFrame a partir da lista de dados
        df = pd.DataFrame(dados)

        # Salve o DataFrame como um arquivo CSV
        df.to_csv('dados_atualizados.csv', index=False, mode='a', header=None)

        # Encontre o botão para passar a página e clique nele
        try:
            wait = WebDriverWait(driver, 15)
            botao = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@aria-label="Next"]')))
            botao.click()
        except TimeoutException:
            print("Erro ao clicar no botão 'Próximo'.")
            continue

        pagina_atual += 1


except Exception as e:
    print(f"Erro ao raspar dados: {e}")
    df.to_csv('dados_atualizados.csv', index=False, mode='a', header=None)
    print("Os dados raspados até agora foram salvos em 'dados.csv'.")

finally:
    # Feche o driver
    driver.quit()
    



    """pagina_atual = 5
def se_der_erro():
    url = f'https://consultas.transparencia.mt.gov.br/pessoal/servidores_ativos/resultado_1.php?pg={pagina_atual}&mes=1&ano=2024'
    print(url)

se_der_erro()"""