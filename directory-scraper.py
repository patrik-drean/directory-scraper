import getpass, json, time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.by import By

BASE_PATH = '/Users/patrikdrean/dev'
LOGIN_URL = "https://login.churchofjesuschrist.org/?service=200"
DIRECTORY_URL = "https://directory.churchofjesuschrist.org/2029413"
HOUSEHOLD_CSS_CLASS_NAME = "sc-gZMcBi"
CREDS_FILE_PATH = f'{BASE_PATH}/secrets/lds-creds.json'

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
  driver = webdriver.Chrome(f"{BASE_PATH}/directory-scraper/chromedriver", options=options)
  return driver

def authenticateUser(driver):
  driver.get(LOGIN_URL)

  ########## Uncoment for manual entering ##########
  # username = input('Enter username: ')
  # password = getpass.getpass('Enter password: ')

  creds = json.load(open(CREDS_FILE_PATH))
  username = creds['username']
  password = creds['password']

  WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))  
  username_input = driver.find_element_by_name("username")
  password_input = driver.find_element_by_name("password")
  submit_button = driver.find_element_by_id("sign-in")

  username_input.clear()
  password_input.clear()
  username_input.send_keys(username)
  password_input.send_keys(password)

  submit_button.click()
  time.sleep(5)

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

  f = open(f"{BASE_PATH}/directory-scraper/output/current-households.json", "w")
  f.write(json_string)
  f.close()