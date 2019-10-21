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
  # driver = configureDriver()
  # authenticateUser(driver)
  # households = getHouseholds(driver)
  # outputJson(households)

  households = ['Adams, Sunny', 'Anderson, Jakob & Elizabeth', 'Anderson, Rich & Heather', 'Anderson, Richard & Susan', 'Araujo, Bruno Amon Santos Porto de & Letícia Mottola de Oliveira', 'Arsenault, Dennis & Becky', 'Barnes, Janice', 'Baxter, Carl & Michelle', 'Bearstops, Jace', 'Benson, LaDonna', 'Biggs, Emily', 'Bigler, Kyler & Laurana Joy', 'Binger, Christopher Steven & Randi Michelle', 'Bird, Jared & Lauren', 'Blair, Nathan Carl & Candace', 'Block, Codi', 'Blomquist, Raymond John & Echo', 'Bowen, Chance & Nicole', 'Broderdorf, Josh', 'Brooks, Paula', 'Brown, Dustin James & Lesle Dian', 'Caler, Ben & Laura', 'Cambridge, Erik Lee & Kristen', 'Carbine, Kyle & Lara Colleen', 'Chapman, Kelly', 'Christiansen, Chandler & Alejandra Sydni', 'Clark, Matthew & Carrie', 'Coberly, Casey & Jenny', "D'Avila, Juliana Scatulino", 'Davis, Chris', 'Davis, Daren', 'Dawson, Kolt & Stephanie', 'Denning, Richard Telford & Leann', 'Dennis, Ryan Charles', 'Devine, Rich', 'Douglas, Wesley & Penny', 'Drean, Patrik & Rachel Rose', 'Edwards, Jordan & Brittney Lee', 'Edwards, Trent', 'Evans, Amy', 'Ewing, Terry', 'Familia, Craig & Shirley', 'Fawson, Jordan & Solana Rynay', 'Forbes, Ryan & Cherelle', 'Francom, Michael', 'Frome, Nathaniel Mark', 'Gage, David & Lindsey Michelle', 'Giang, Jason', 'Golladay, Kenneth A & Anne Elizabeth', 'Gonzalez Borjas, Israel A & Lucia Nieri', 'Grant, John & Katrina', 'Grant, Valerie Lyn', 'Ham, Cameron & Danielle Jenica', 'Hansen, Jacob & Andrea Marie', 'Hardy, Cameron', 'Hardy, Darreld & Susan', 'Harvey, Jason & Ashlee Marie', 'Harward, Court & Cynthia', 'Haupt, Julie', 'Higgins, Clinton & Anna', 'Hill, Kristi', 'Hill, Suellen', 'Hooley, Chase & Jessica', 'Hutchings, Duane & Isabel', 'Irish, Chad', 'Ivie, Amber', 'Jensen, Josh & Kailee Shae', 'Jensen, Kyle & Alicia', 'Jimenez, Jennifer', 'Johanson, Mindy', 'Johnson, Amethyst', 'Jolley, Bonnie', 'Jones, Adam & Molly', 'Jones, Amber', 'Jones, Tryson', 'Kay, Natalie', 'Keeler, Gail', 'Kirby, Nicole', 'Labrum, Dallan & Kayla', 'Larsen, Charles & Patty', 'Law, Mark Arthur & Marnia Lea', 'Lebaron, Lisa', 'Lehmitz, David Cole Matheny & Adrianna Louise', 'Lobendahn, Adriu', 'Lopez, Emily', 'Lundgren, Spencer & Ashton Leigh', 'Lyman, Brett & Emily', 'Mackay, Michael & Miriam Elaine', 'Manzanares, Aaron', 'Maxfield, Dallin & Lindsay', 'Maxfield, Mark & Elaine', 'McKell, Scott & Lisa', 'Meixel, Mr & Kansas Diane', 'Miller, Mitch', 'Mitchell, Jaden & Rhiannon Dee', 'Morgan, Stacey Christine', 'Moser, Jarod & Sheryl René', 'Nelson, Geoffrey & Jaimie', 'Newman, Danielle', 'Nielson, Mark Gerber & Camilla May', 'Nuttall, Landon & Stephanie', 'Orrick, Trudy Gay', 'Owens, Sarah Young', 'Pagaduan, Jayson & Elizabeth', 'Parker, Michael & Christine', 'Patrick, Josh & Kristina', 'Patterson, Nicole', 'Pehrson, Cleve', 'Perez, Fiona', 'Perkins, Mark', 'Perkinson, Andrew John & Demi Deann', 'Peterson, Chris & Lindsay', 'Poole, Travis & Lisa', 'Porenta, Mike & Sami', 'Porter, Andrew', 'Preisendorf, Craig & Kathryn Marie', 'Pymm, Tracy & Jessica', 'Radulovich, Michael & Lisa', 'Rasmussen, Alicia', 'Rasmussen, Dave & Shauna', 'Rogers, Jeffrey D & Melissa Lynn', 'Rumsey, Tristan', 'Rymer, Tyler', 'Schumann, Scott & Tiffany Diane', 'Shelley, Bryce & Merriam', 'Smith, Aaron & Rusty Michelle', 'Smith, AJ', 'Smith, Heather', 'Smith, Richard & Susie', 'Smith, Robert & Natasha Elizabeth', 'Smith, Ryan & Emily', 'Spier, Pam', 'Stevenett, Joel & Natalie Michelle', 'Stone, TJ & Annaliese', 'Swensen, Marie', 'Thomas, Tracey', 'Thorne, Alison', 'Thueson, Dan', 'Tullis, Timothy John & Holly', 'Turner, Bob', 'Turner, Glenna', 'Valencia Cervantes, Mario & Shannon McDonald', 'Van Cott, Mark & Mary Anne', 'Viray, Jonathan & Vanesa', 'Walker, Julie Mandeline', 'Walker, Lindsay', 'Weir, Nathan Charles & Amanda Rae', 'West, Brady & Jodi', 'Wiese, Todd & Becky', 'Williams, Trevor', 'Wombacher, Brooklyn', 'Workman, Casey & Gloria Alicia', 'Workman, Ty & Meili', 'Wright, Christopher Kyle & Jillisa', 'Wynder, Darin', 'Young, Jim & Cassie']

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

  f = open("output/current-households.json", "w")
  f.write(json_string)
  f.close()