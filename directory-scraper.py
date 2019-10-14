import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

login_url = "https://ident.churchofjesuschrist.org/sso/UI/Login"
directory_url = "https://directory.churchofjesuschrist.org/2029413"
payload = {
    'IDToken1': 'USERNAME',
    'IDToken2': 'PASSWORD',
    'IDButton': 'Log In',
    'goto': '',
    'gotoOnFail': '',
    'SunQueryParamsString': 'c2VydmljZT1jcmVkZW50aWFscyZyZWFsbT0vY2h1cmNo',
    'encoded': 'true',
    'gx_charset': 'UTF-8'
  }

def main():
  driver = configureDriver()
  session = requests.Session() 

  authenicated_cookies = authenticateUser(driver, session)

  # driver.implicitly_wait(10) 
  driver.get(directory_url)
  [driver.add_cookie(c) for c in authenicated_cookies]
  input()
  driver.get(directory_url)
  text_file = open("Output.html", "w")
  text_file.write(driver.page_source)
  text_file.close()
  # print(driver.page_source)

  # input()

def configureDriver():
  options = webdriver.ChromeOptions()
  options.add_argument('--ignore-certificate-errors')
  options.add_argument('--incognito')
  # options.add_argument('--headless')
  driver = webdriver.Chrome("/Users/patrikdrean/dev/directory-scraper/chromedriver", chrome_options=options)
  return driver

def authenticateUser(driver, session):
  response = session.get(login_url)
  session.post(login_url, data=payload)
  response = session.get(directory_url)

  authenicated_cookies = [{'name':name, 'value':value} for name, value in session.cookies.get_dict().items()]
  return authenicated_cookies

if __name__ == "__main__":
    main()

