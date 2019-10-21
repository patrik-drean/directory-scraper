import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '1Ly_6nh1QfqQufMwwT69n1GUtZ72hFaynO6visbJFpRA'
RANGE = 'A1:P800'
CREDS_FILE_PATH = "../secrets/lds-creds.json"

def getSheetData(sheet_name):
  spreadsheet_service = authenticate()

  sheet = spreadsheet_service.spreadsheets()
  result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,range=f'{sheet_name}!{RANGE}').execute()
  values = result.get('values', [])

  return values

def writeDataToSheet(sheet_name, values):
  spreadsheet_service = authenticate()

  for _ in range(0, 100):
    values.append(['', '', ''])

  body = {
      'values': values
  }
  result = spreadsheet_service.spreadsheets().values().update(
      spreadsheetId=SPREADSHEET_ID, range=f'{sheet_name}!{RANGE}',
      valueInputOption='RAW', body=body).execute()

def appendDataToSheet(sheet_name, values):
  spreadsheet_service = authenticate()

  body = {
      'values': values
  }
  result = spreadsheet_service.spreadsheets().values().append(
      spreadsheetId=SPREADSHEET_ID, range=f'{sheet_name}!{RANGE}',
      valueInputOption='RAW', body=body).execute()

def authenticate():
  creds = None
  if os.path.exists('token.pickle'):
      with open('token.pickle', 'rb') as token:
          creds = pickle.load(token)

  if not creds or not creds.valid:
      if creds and creds.expired and creds.refresh_token:
          creds.refresh(Request())
      else:
          flow = InstalledAppFlow.from_client_secrets_file(CREDS_FILE_PATH, SCOPES)
          creds = flow.run_local_server(port=0)

      with open('token.pickle', 'wb') as token:
          pickle.dump(creds, token)

  return build('sheets', 'v4', credentials=creds)