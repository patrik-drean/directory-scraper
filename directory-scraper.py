import time, re, csv, glob, pprint, time, getpass, json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException

login_url = "https://ident.churchofjesuschrist.org/sso/UI/Login"
directory_url = "https://directory.churchofjesuschrist.org/2029413"
household_class_name = "sc-gZMcBi"
creds_file_path = "../secrets/lds-creds.json"

json_file = open(creds_file_path)
creds = json.load(json_file)

def main():
  driver = configureDriver()

  authenticateUser(driver)
  households = getHouseholds(driver)
  outputJson(households)

def configureDriver():
  options = webdriver.ChromeOptions()
  options.add_argument('--ignore-certificate-errors')
  options.add_argument('--incognito')
  # options.add_argument('--headless')
  driver = webdriver.Chrome("/Users/patrikdrean/dev/directory-scraper/chromedriver", options=options)
  return driver

def authenticateUser(driver):
  driver.get(login_url)

  ## Uncoment for manual entering ##
  # username = input('Enter username: ')
  # password = getpass.getpass('Enter password: ')

  username = creds['username']
  password = creds['password']

  WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'IDToken1')))  
  username_input = driver.find_element_by_name("IDToken1")
  password_input = driver.find_element_by_name("IDToken2")

  username_input.clear()
  password_input.clear()
  username_input.send_keys(username)
  password_input.send_keys(password)

  username_input.submit()

def getHouseholds(driver):
  driver.get(directory_url)
  WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, household_class_name)))
  driver.find_elements_by_class_name(household_class_name)
  
  households = list(map(lambda element: element.text, driver.find_elements_by_class_name(household_class_name)))
  return households

def outputJson(households):
  json_string = '['

  for row in households: 
    json_string += f'{{ "name": "{row}"}},'
    
  json_string = json_string[:-1]
  json_string += ']'

  f = open("households.json", "w")
  f.write(json_string)
  f.close()


if __name__ == "__main__":
    main()