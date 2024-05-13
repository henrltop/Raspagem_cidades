from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd

def main():
    url = 'https://transparencia.betha.cloud/#/cST4aUw2ylR2Zxh80uoChw==/consulta/28404?esconderCabecalho=S&esconderMenu=S&esconderRodape=S'
    driver = webdriver.Chrome()
    driver.get(url)

    try:
        WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.bth-filter.bth-filter--sidebar.bth-filter--floating.responsive-filter')))
        print('Modal visível')

        # Clicar no botão "Filtrar (ENTER)"
        botao_filtrar = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//button[normalize-space(text())="Filtrar (ENTER)"]')))
        botao_filtrar.click()

        # Selecionar o valor 100 no dropdown
        selector = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="card-consulta"]/div/div/div/div/div[6]/div/div/div[1]/form/select'))
        )
        select = Select(selector)
        select.select_by_visible_text('100')

        # Raspagem de dados
        dados = []
        cabecalho = ['MATRÍCULA', 'NOME DO SERVIDOR', 'DATA DE ADMISSÃO', 'CARGO', 'CARGA HORÁRIA MENSAL',
                     'VÍNCULO EMPREGATÍCIO', 'EFETIVO EM CARGO COMISSIONADO', 'ÓRGÃO', 'LOTAÇÃO', 'CEDIDO/RECEBIDO',
                     'SITUAÇÃO', 'TIPO DE MATRICULA', 'REMUNERAÇÃO', 'CONTRATUAL']
        dados.append(cabecalho)

        # Processar as páginas
        for _ in range(1, 27):
            tabela = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="card-consulta"]/div/div/div/div/div[5]/div/table/tbody'))
            )
            linhas = tabela.find_elements(By.TAG_NAME, 'tr')

            for linha in linhas:
                celulas = linha.find_elements(By.TAG_NAME, 'td')
                dados.append([celula.text for celula in celulas])

            if not click_proximo(driver):
                break

        # Exportar para CSV
        df = pd.DataFrame(dados)
        df.to_csv('Raspagem_Lucas_Rio_Verde.csv', index=False)
        print("Dados salvos no CSV.")

    except Exception as e:
        print(f"Ocorreu um erro durante a execução: {str(e)}")
    finally:
        driver.quit()

def click_proximo(driver):
    try:
        proximo = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="card-consulta"]/div/div/div/div/div[6]/div/div/div[2]/div/button[7]'))
        )
        proximo.click()
        return True
    except TimeoutException:
        print("Botão 'Próximo' desativado.")
        return False

if __name__ == '__main__':
    main()



