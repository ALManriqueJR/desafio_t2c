"""
Visa busca de notebooks no site da Magazine Luiza, gerando arquivo Excel e finalmente enviando por email.
"""
import os
import re
import xlsxwriter as create_excel
import send_to_email

from selenium import webdriver as wb
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def main():
    
    produtos = []
    nome = ''
    link = ''
    qtd_review = -1
    
    caminho_arquivo = os.path.join(os.getcwd(), 'Output', 'Notebooks.xlsx')
    planilha = create_excel.Workbook(caminho_arquivo)
    aba1 = planilha.add_worksheet("Piores")
    aba2 = planilha.add_worksheet("Melhores")
    
    nav = wb.Chrome()
    nav.implicitly_wait(10)
    wait = WebDriverWait(nav, 15)
    
    for i in range(1,3):
        try:
            nav.get('https://www.magazineluiza.com.br')
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="input-search"]')))
            nav.find_element(By.ID, 'input-search').send_keys('notebooks')
            nav.find_element(By.ID, 'input-search').send_keys(Keys.RETURN)
            if wait.until(EC.presence_of_element_located((By.XPATH, '//div[@data-testid="product-list"]/ul/li'))):
                break
            else:
                if (i == 3):
                    raise Exception('Falha ao carregar dentro de 3 tentativas')
                continue
            
        except Exception as e:
            print('Site fora do ar')
            nav.quit()
            planilha.close()
            exit()
    
    while True:
        items = nav.find_elements(By.XPATH,'//h2[1][@data-testid="product-title"]')
        count = len(items)
        
        for i in range(1,count):
            prod_links = nav.find_elements(By.XPATH, f'//div[@data-testid="product-list"]/ul/li[{i}]/a')
            
            if not prod_links:
                continue
            
            prod_link = prod_links[0]
            link = prod_link.get_attribute('href')
            
            
            nome = link.split('/')[3]
            lista = [palavra.upper() if len(palavra) < 4 else palavra.capitalize()
            for palavra in nome.split('-')]
            nome = ' '.join(lista)
            
            
            review_element = nav.find_elements(By.XPATH, f'//div/ul/li[{i}]/a/div/div/div[@data-testid="review"]/span')
            
            if review_element:
                review_text = review_element[0].text
                qtd_review_match = re.search(r'\((.*?)\)', review_text)
                if qtd_review_match:
                    qtd_review = int(qtd_review_match.group(1))
            
            produtos.append({"Produto": nome, "Qtd_Aval":qtd_review, "URL": link})
        
        next_button = nav.find_elements(By.XPATH, '//button[@aria-label="Go to next page"]')
        if next_button:
            next_button[0].click()
            wait.until(EC.presence_of_element_located((By.XPATH, '//div[@data-testid="product-list"]/ul/li')))         
        else:
            break
        
    aba1.write("A1","Nome")
    aba1.write("B1","Qtd. Avaliacoes")
    aba1.write("C1","URL")
    
    aba2.write("A1","Nome")
    aba2.write("B1","Qtd. Avaliacoes")
    aba2.write("C1","URL")
    
    piores_prod = [p for p in produtos if p['Qtd_Aval'] < 100]
    melhores_prod = [p for p in produtos if p['Qtd_Aval'] >= 100]
    
    for linha, dicio in enumerate(piores_prod, start=1):
        aba1.write(linha, 0, dicio['Produto'])
        aba1.write(linha, 1, dicio['Qtd_Aval'])
        aba1.write(linha, 2, dicio['URL'])
        
    for linha, dicio in enumerate(melhores_prod, start=1):
        aba2.write(linha, 0, dicio['Produto'])
        aba2.write(linha, 1, dicio['Qtd_Aval'])
        aba2.write(linha, 2, dicio['URL'])
        
    nav.quit()
    planilha.close()
    #ps.startfile(caminho_arquivo)
    
    send_to_email.enviar(caminho_arquivo)
    
if __name__ == "__main__":
    main()
