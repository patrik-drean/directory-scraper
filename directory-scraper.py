import getpass, json
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.by import By

LOGIN_URL = "https://ident.churchofjesuschrist.org/sso/UI/Login"
DIRECTORY_URL = "https://directory.churchofjesuschrist.org/2029413"
HOUSEHOLD_CSS_CLASS_NAME = "sc-gZMcBi"
CREDS_FILE_PATH = "../secrets/lds-creds.json"

def getCurrentHouseholds():
  driver = configureDriver()
  authenticateUser(driver)
  households = getHouseholds(driver)
  outputJson(households)

  return households

def configureDriver():
  options = webdriver.ChromeOptions()
  options.add_argument('--ignore-certificate-errors')
  options.add_argument('--incognito')
  options.add_argument('--headless')
  driver = webdriver.Chrome("/Users/patrikdrean/dev/directory-scraper/chromedriver", options=options)
  return driver

def authenticateUser(driver):
  driver.get(LOGIN_URL)

  ## Uncoment for manual entering ##
  # username = input('Enter username: ')
  # password = getpass.getpass('Enter password: ')

  creds = json.load(open(CREDS_FILE_PATH))
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
  driver.get(DIRECTORY_URL)
  WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, HOUSEHOLD_CSS_CLASS_NAME)))
  driver.find_elements_by_class_name(HOUSEHOLD_CSS_CLASS_NAME)
  
  households = list(map(lambda element: element.text, driver.find_elements_by_class_name(HOUSEHOLD_CSS_CLASS_NAME)))
  return households

def outputJson(households):
  json_string = '['

  for row in households: 
    json_string += f'{{ "name": "{row}"}},'
    
  json_string = json_string[:-1]
  json_string += ']'

  f = open("current-households.json", "w")
  f.write(json_string)
  f.close()