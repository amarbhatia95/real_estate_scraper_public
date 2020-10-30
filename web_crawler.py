from bs4 import BeautifulSoup
import re as re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module='bs4')

def init_driver(file_path):
    """Direct to zillow.com and beat captcha"""
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_experimental_option('w3c', False)

    caps = DesiredCapabilities.CHROME
    caps['loggingPrefs'] = {'performance': 'ALL'}
    
    driver = webdriver.Chrome(executable_path=file_path, 
                options=options, desired_capabilities=caps)
    driver.wait = WebDriverWait(driver, 10)
    return driver

def identify_captcha(driver):
    """Check to see if the page is currently oimpon Captcha Page"""
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    if soup.find_all('div', class_='captcha-container'):
        return True
    else:
        return False

def identify_pagination(soup):
    try:
        return int(re.findall('\d+' ,soup.find_all('div', class_='search-pagination')[0].find_all('li')[-2].text)[1])
    except:
        return False

def navigate_to_page(driver, site):
    """Navigate to Any Webpage"""
    driver.get(site)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    captcha_exists = identify_captcha(driver)
    while captcha_exists: # edit this
        time.sleep(60)
        captcha_pass = 'https://www.zillow.com/homes/'
        driver.get(captcha_pass)
        captcha_exists = identify_captcha(driver)
    return driver

def navigate_to_code(driver, code):
    """Navigate to a page with Zillow Zip Code"""
    soups = {}
    site = f'https://www.zillow.com/homes/{code}_rb'
    driver.get(site)
    captcha_exists = identify_captcha(driver)
    while captcha_exists:
        time.sleep(60)
        captcha_pass = 'https://www.zillow.com/homes/'
        driver.get(captcha_pass)
        captcha_exists = identify_captcha(driver)
    soup = get_soup(driver)
    soups[code] = []
    soups[code].append(soup)
    pagination_exists = identify_pagination(soup)
    if pagination_exists:
        for i in range(2, int(soup.find_all('div', class_='search-pagination')[0].find_all('li')[-2].text[-1]) + 1):
            new_site = site + f"{i}_p"
            driver.get(f"https://www.zillow.com/homes/{code}_rb/{i}_p")
            soup = get_soup(driver)
            soups[code].append(soup)

    return soups

def get_soup(driver):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    return soup

def terminate_driver(driver):
    driver.quit()

