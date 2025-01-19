import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
import time

# Configuração do driver do Firefox
service = Service(GeckoDriverManager().install())
driver = webdriver.Firefox(service=service)

# Solicitar informações ao usuário
print("Configuração da pesquisa na Ad Library do Facebook")
country = input("Digite o código do país (ex: BR para Brasil): ").strip().upper()
search_keyword = input("Digite uma palavra-chave para pesquisa: ").strip()

# Construir a URL de acordo com os critérios do usuário
base_url = "https://www.facebook.com/ads/library/"
query_params = f"?active_status=active&ad_type=all&country={country}&is_targeted_country=false&media_type=all&q={search_keyword}"
url = base_url + query_params

# Acessar a URL gerada
driver.get(url)

# Esperar a página carregar
time.sleep(5)

# Aceitar cookies, se necessário
try:
    cookie_button = driver.find_element(By.XPATH, '//button[contains(text(), "Aceitar todos os cookies")]')
    cookie_button.click()
    time.sleep(2)
except Exception:
    print("Nenhum botão de cookies encontrado.")

# Rolagem da página para carregar mais anúncios
for _ in range(5):  # Ajuste o número de rolagens conforme necessário
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

# Capturar anúncios na página
ads = driver.find_elements(By.XPATH, '//div[contains(@class, "xh8yej3")]')  # Ajuste o seletor para encontrar os anúncios
if ads:
    # Salvar os resultados em um arquivo CSV
    with open('facebook_ads.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Título', 'Descrição', 'Link']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for ad in ads:
            try:
                # Extrair título (Nome da página)
                title = ad.find_element(By.XPATH, './/a[contains(@class, "xt0psk2")]/span').text
                
                # Extrair descrição do anúncio
                description = ad.find_element(By.XPATH, './/span[contains(@class, "x14vqqas")]').text
                
                # Extrair link de destino
                link = ad.find_element(By.XPATH, './/a[contains(@href, "l.php")]').get_attribute('href')
                
                # Salvar os dados no arquivo CSV
                writer.writerow({
                    'Título': title, 
                    'Descrição': description, 
                    'Link': link
                })
            except Exception as e:
                print(f"Erro ao processar anúncio: {e}")
    print("\nOs resultados foram salvos em 'facebook_ads.csv'.")
else:
    print("\nNenhum anúncio encontrado com os critérios fornecidos.")

# Fechar o navegador
driver.quit()