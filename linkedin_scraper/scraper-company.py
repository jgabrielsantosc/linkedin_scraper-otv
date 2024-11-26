import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import os

# Caminho para o arquivo de cookies
COOKIES_PATH = "cookies.json"

def login(driver, email, password):
    """Realiza o login no LinkedIn."""
    driver.get("https://www.linkedin.com/uas/login")
    driver.find_element(By.ID, "username").send_keys(email)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

def save_cookies(driver, path):
    """Salva os cookies em um arquivo JSON."""
    with open(path, "w") as f:
        json.dump(driver.get_cookies(), f, indent=4)

def load_cookies(driver, path):
    """Carrega os cookies de um arquivo JSON."""
    with open(path, "r") as f:
        cookies = json.load(f)
        for cookie in cookies:
            driver.add_cookie(cookie)

def scrape_linkedin_company(url, email, password):
    """Extrai nome, logo e sumário da empresa do LinkedIn, com login."""
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless=new") # Execute sem interface gráfica (opcional)
    driver = webdriver.Chrome(options=options)
    try:
        if os.path.exists(COOKIES_PATH):
            load_cookies(driver, COOKIES_PATH)
            driver.get(url)
        else:
            login(driver, email, password)
            save_cookies(driver, COOKIES_PATH)
            driver.get(url)

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
    email = os.environ.get("LINKEDIN_EMAIL") # Substitua por sua variável de ambiente
    password = os.environ.get("LINKEDIN_PASSWORD") # Substitua por sua variável de ambiente
    name, logo_url, summary = scrape_linkedin_company(company_url, email, password)

    if name and logo_url and summary:
        print("\nInformações da empresa:")
        print(f"Nome: {name}")
        print(f"Logo URL: {logo_url}")
        print(f"Sumário: {summary}")
    else:
        print("Não foi possível extrair as informações da empresa.")