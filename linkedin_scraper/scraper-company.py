from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

def scrape_linkedin_company(url):
    """Extrai nome, logo e sumário da empresa do LinkedIn."""
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless=new") # Execute sem interface gráfica (opcional)
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(url)
        # Esperar até que os elementos sejam carregados (com timeout)
        wait = WebDriverWait(driver, 10)

        try:
            name_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1.org-top-card-summary__title")))
            name = name_element.text.strip()
        except (TimeoutException, NoSuchElementException):
            name = None

        try:
            logo_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "img.org-top-card-primary-content__logo")))
            logo_url = logo_element.get_attribute("src")
        except (TimeoutException, NoSuchElementException):
            logo_url = None

        try:
            summary_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "p.org-top-card-summary__tagline")))
            summary = summary_element.text.strip()
        except (TimeoutException, NoSuchElementException):
            summary = None

        return name, logo_url, summary

    except Exception as e:
        print(f"Erro durante o scraping: {e}")
        return None, None, None
    finally:
        driver.quit()

if __name__ == "__main__":
    company_url = "https://www.linkedin.com/company/eusouagabriel/"
    name, logo_url, summary = scrape_linkedin_company(company_url)

    if name and logo_url and summary:
        print("\nInformações da empresa:")
        print(f"Nome: {name}")
        print(f"Logo URL: {logo_url}")
        print(f"Sumário: {summary}")
    else:
        print("Não foi possível extrair as informações da empresa.")