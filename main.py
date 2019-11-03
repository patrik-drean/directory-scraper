from datetime import datetime
directory_scraper = __import__('directory-scraper')
google_api = __import__('google-api')

ARCHIVE_RECORDS = []
UPDATED_GOOGLE_RECORDS = []
TODAY = f'{datetime.today().year}-{datetime.today().month}-{datetime.today().day}'

def main():
  current_households = directory_scraper.getCurrentHouseholds()
  google_records = google_api.getSheetData('Households')

  for record in google_records[1:]:
    household_name = record[0]

    if household_name in current_households:
      UPDATED_GOOGLE_RECORDS.append(record)
      current_households.remove(household_name)
    else:
      ARCHIVE_RECORDS.append(record)

  for new_household in current_households:
    UPDATED_GOOGLE_RECORDS.append([new_household, '-','-'])

  headers = [google_records[0]]
  headers[0][len(headers[0])-1] = TODAY

  google_output = headers + sorted(UPDATED_GOOGLE_RECORDS, key=lambda x: x[0])

  google_api.writeDataToSheet('Households', google_output)
  google_api.appendDataToSheet('Archive',ARCHIVE_RECORDS)

if __name__ == "__main__":
    main()