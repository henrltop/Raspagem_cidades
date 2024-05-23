from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException, TimeoutException
import csv
from tqdm import tqdm

Nome_do_Arquivo = 'Raspagem_Campo_novo.csv'
# Configurações do Selenium
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--log-level=3')
driver = webdriver.Chrome(options=options)

# Acessa a página
url = 'https://www.gp.srv.br/transparencia_camponovodoparecis/servlet/contrato_servidor_v3?1'
driver.get(url)

# Clique no botão Pesquisar
pesquisar = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="BUTTON1"]')))
pesquisar.click()

# Seleciona 150 itens por página
selecionar = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="vQTD_POR_PAGINA"]')))
select = Select(selecionar)
select.select_by_visible_text('150')

def pegar_total_registro():
    total_registros_element = driver.find_element(By.XPATH, '//*[@id="span_vTOTAL_REGISTROS"]')
    return int(total_registros_element.text)

def total_de_paginas():
    total_de_registros = pegar_total_registro()
    registro_por_pagina = 150
    num_paginas = (total_de_registros + registro_por_pagina - 1) // registro_por_pagina
    return int(num_paginas)

num_paginas = total_de_paginas()
print(num_paginas)

# Função para clicar no botão "Próximo"
def click_proximo():
    try:
        proximo = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="TB_PROXIMO_ENABLED"]/a'))
        )
        proximo.click()
        return True
    except TimeoutException:
        print("Botão 'Próximo' desativado.")
        return False

with open(Nome_do_Arquivo, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['CPF/CNPJ', 'Razão Social', 'Vigência', 'Situação', 'Valor Contrato', 'Setor'])

# Função para extrair elementos da tabela
def extrair_elementos():
    try:
        # Tenta encontrar o CPF/CNPJ
        try:
            cpf_cnpj_element = WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="span_vCONTRATO_CPF_CNPJ"]'))
            ).text
        except TimeoutException:
            try:
                cpf_cnpj_element = WebDriverWait(driver, 3).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="span_vSERV_CPF"]'))
                ).text
            except TimeoutException:
                cpf_cnpj_element = "N/A"

        # Tenta encontrar a Razão Social
        try:
            razao_social_element = WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="span_vCONTRATO_RAZAO_SOCIAL"]'))
            ).text
        except TimeoutException:
            try:
                razao_social_element = WebDriverWait(driver, 3).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="span_vSERV_NOME"]'))
                ).text
            except TimeoutException:
                razao_social_element = "N/A"

        # Tenta encontrar a Vigência
        try:
            vigencia_element = WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="TABLE6"]'))
            ).text
        except TimeoutException:
            try:
                vigencia_element = WebDriverWait(driver, 3).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="span_vDATA_DE_POSSE"]'))
                ).text
            except TimeoutException:
                vigencia_element = "N/A"

        # Tenta encontrar a Situação
        try:
            situacao_element = WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="span_vCONTRATO_SITUACAO"]'))
            ).text
        except TimeoutException:
            try:
                situacao_element = WebDriverWait(driver, 3).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="span_vSERV_SITUACAO"]'))
                ).text
            except TimeoutException:
                situacao_element = "N/A"

        # Tenta encontrar o Valor do Contrato
        try:
            valor_element = WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="span_vCONTRATO_VALOR"]'))
            ).text
        except TimeoutException:
            try:
                valor_element = WebDriverWait(driver, 3).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="span_vSERV_VALOR"]'))
                ).text
            except TimeoutException:
                valor_element = "N/A"

        # Tenta encontrar o Setor
        try:
            setor_desc_element = WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="span_vSERVIDOR_LOTACAO_DESC"]'))).text
        except TimeoutException:
            setor_desc_element = "N/A"

        with open(Nome_do_Arquivo, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow([cpf_cnpj_element, razao_social_element, vigencia_element, situacao_element, valor_element, setor_desc_element])

    except StaleElementReferenceException:
        print("Tabela não encontrada, tentando novamente...")
        extrair_elementos()

    except Exception as e:
        print(f"Erro ao extrair elementos da tabela: {e}")

# Função para clicar na lupa e obter os dados da tabela
def scrape_table():
    for i in range(1, 151):
        xpath_lupa = f'//*[@id="grid"]/tbody/tr[{i}]/td/a/i[@title="Visualizar detalhes"]'
        
        for _ in range(3):  # Tentativas para lidar com elementos obsoletos
            try:
                lupa = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath_lupa)))
                lupa.click()
                break
            except (StaleElementReferenceException, ElementClickInterceptedException):
                print("Elemento da lupa ficou obsoleto ou está sendo interceptado. Tentando novamente...")
                sleep(1)
                try:
                    lupa = driver.find_element(By.XPATH, xpath_lupa)
                    driver.execute_script("arguments[0].click();", lupa)
                except StaleElementReferenceException:
                    continue
                except Exception as e:
                    print(f"Erro ao tentar clicar na lupa com JavaScript: {e}")
                    continue
            except Exception as e:
                print(f"Erro inesperado ao clicar na lupa: {e}")
                continue

        try:
            WebDriverWait(driver, 20).until(EC.number_of_windows_to_be(2))
        except:
            continue

        driver.switch_to.window(driver.window_handles[1])
        extrair_elementos()
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

for _ in tqdm(range(num_paginas), desc="Progresso"):
    scrape_table()
    if not click_proximo():
        break

driver.quit()
