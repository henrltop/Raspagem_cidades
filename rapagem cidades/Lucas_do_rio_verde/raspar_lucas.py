from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd
import time

url = 'https://transparencia.betha.cloud/#/cST4aUw2ylR2Zxh80uoChw==/consulta/28404?esconderCabecalho=S&esconderMenu=S&esconderRodape=S'

driver = webdriver.Chrome()
driver.get(url)


#------------------------------------------------------------------------------------------(Inicio da remoção do modal)
# Espera até que o modal esteja visível
WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.bth-filter.bth-filter--sidebar.bth-filter--floating.responsive-filter')))
print('Modal visível')

# Agora que o modal está visível, você pode encontrar o botão dentro dele
Botão_modal = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//button[normalize-space(text())="Filtrar (ENTER)"]')))
Botão_modal.click()


#------------------------------------------------------------------------------------------(Fim da remoção do modal)

#------------------------------------------------------------------------------------------(Localizar Botão de passar página)
selecionar = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="card-consulta"]/div/div/div/div/div[6]/div/div/div[1]/form/select')))
select = Select(selecionar)
select.select_by_visible_text('100')
#------------------------------------------------------------------------------------------


tabela = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="card-consulta"]/div/div/div/div/div[5]/div/table/tbody')))
linhas = tabela.find_elements(By.TAG_NAME, 'tr')

dados = []
for linha in linhas:
    # Encontre todas as células dentro da linha
    celulas = linha.find_elements(By.TAG_NAME, 'td')
    # Para cada linha, obtenha o texto de cada célula e adicione-o à lista de dados
    dados_linha = [celula.text for celula in celulas]
    dados.append(dados_linha)


df = pd.DataFrame(dados)

df.to_csv('teste.csv', index=False)




def click_proximo():
    try:
        proximo = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="card-consulta"]/div/div/div/div/div[6]/div/div/div[2]/div/button[7]'))
        )
        proximo.click()
        return True
    except TimeoutException:
        print("Botão 'Próximo' desativado.")
        return False
#---------------------------------------------------------------------------------------------
tabela = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="card-consulta"]/div/div/div/div/div[5]/div/table/tbody')))
print(tabela.text)
