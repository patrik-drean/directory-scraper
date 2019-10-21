directory_scraper = __import__('directory-scraper')


def main():
  print(directory_scraper.getCurrentHouseholds())
  

if __name__ == "__main__":
    main()