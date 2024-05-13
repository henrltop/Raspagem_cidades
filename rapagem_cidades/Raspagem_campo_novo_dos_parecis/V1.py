from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException, TimeoutException
import csv
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from tqdm import tqdm
import os



Nome_do_Arquivo= 'Raspagem_Alta_Floresta_segundo_modelo.csv'
# Configurações do Selenium
options = webdriver.ChromeOptions()
#options.add_argument('--headless')  
options.add_argument('--log-level=3')
driver = webdriver.Chrome(options=options)


# Acessa a página
url = 'https://www.gp.srv.br/transparencia_camponovodoparecis/servlet/contrato_servidor_v3?1'
driver.get(url)


pesquisar = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="BUTTON1"]'))
)
pesquisar.click()


# Seleciona 150 itens por página
selecionar = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, '//*[@id="vQTD_POR_PAGINA"]'))
)
select = Select(selecionar)
select.select_by_visible_text('150')


def pegar_total_registro():
    total_registros_element=driver.find_element(By.XPATH, '//*[@id="span_vTOTAL_REGISTROS"]')
    return int(total_registros_element.text)


def total_de_paginas():
    total_de_registros= pegar_total_registro()
    registro_por_pagina = 150
    num_paginas = (total_de_registros + registro_por_pagina) // registro_por_pagina
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


lista=[]


with open(Nome_do_Arquivo, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')  # Especifica o separador como ','
    writer.writerow(['CPF/CNPJ', 'Razão Social', 'Vigência', 'Situação', 'Valor Contrato', 'Setor' ])


# Função para extrair os elementos específicos da tabela
def extrair_elementos():
    try:
        # Espera até que os elementos específicos da tabela sejam visíveis
        cpf_cnpj_element = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="span_vCONTRATO_CPF_CNPJ"]'))
        ).text
        razao_social_element = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="span_vCONTRATO_RAZAO_SOCIAL"]'))
        ).text
        vigencia_element = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="TABLE6"]'))
        ).text
        situacao_element = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="span_vCONTRATO_SITUACAO"]'))
        ).text
        valor_element = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="span_vCONTRATO_VALOR"]'))
        ).text
        setor_desc_element = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="span_vSERVIDOR_SETOR_DESC"]'))
        ).text


        
        lista.append([cpf_cnpj_element, razao_social_element,vigencia_element, situacao_element, valor_element, setor_desc_element])
        
        #elementos = [cpf_cnpj_element, razao_social_element, situacao_element, valor_element, setor_desc_element]
        


        with open(Nome_do_Arquivo, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')  
            writer.writerow([cpf_cnpj_element, razao_social_element, vigencia_element, situacao_element, valor_element, setor_desc_element])
    


    except TimeoutException:
        cpf_cnpj_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="span_vSERV_CPF"]'))
        ).text
        razao_social_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="span_vSERV_NOME"]'))
        ).text
        vigencia_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="span_vDATA_DE_POSSE"]'))
        ).text
        situacao_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="span_vSERV_SITUACAO"]'))
        ).text
        valor_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="span_vSERV_VALOR"]'))
        ).text
        setor_desc_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="span_vSERVIDOR_SETOR_DESC"]'))
        ).text


        
        lista.append([cpf_cnpj_element, razao_social_element,vigencia_element, situacao_element, valor_element, setor_desc_element])
        
        
        
        with open(Nome_do_Arquivo, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')  
            writer.writerow([cpf_cnpj_element, razao_social_element, vigencia_element, situacao_element, valor_element, setor_desc_element])


        
    except StaleElementReferenceException:
        print("Tabela Não encontrada , Tentando novamente...") 
             
        
           
            
    except Exception as e:
        print(f"Erro ao extrair elementos da tabela: {e}")
        


def scrape_table():
    for i in range(1, 151):
        xpath_lupa = f'//*[@id="grid"]/tbody/tr[{i}]/td/a/i[@title="Visualizar detalhes"]'
        while True:
            try:
                lupa = driver.find_element(By.XPATH, xpath_lupa)
                lupa.click()
                break
            except (StaleElementReferenceException, ElementClickInterceptedException):
                print("\nErro ao clicar na lupa. Tentando novamente...")
                sleep(1)


        try:
            WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
        except TimeoutException:
            print("Janela não encontrada")
            continue


        driver.switch_to.window(driver.window_handles[1])
        if not extrair_elementos():
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            continue


        driver.close()
        driver.switch_to.window(driver.window_handles[0])


for _ in tqdm(range(num_paginas), desc="Progresso/pagina"):
        
    scrape_table()
    #os.system('cls' if os.name == 'nt' else 'clear')
        
    if not click_proximo():
        break  


driver.quit()