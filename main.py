import requests
from bs4 import BeautifulSoup
from datetime import datetime


def check_valid_date(splited_date):
    year = splited_date[0]
    month = splited_date[1]
    day = splited_date[2]
    try:
        year = int(year)
        month = int(month)
        day = int(day)
        if year < 1958 or year > datetime.now().year:
            print("Invalid year value")
            return False
        if month > 12  or month < 1:
            print("Invalid month value")
            return False
        if (month in [1, 3, 5, 7, 8, 10, 12] and (day > 31 or day < 1)) or \
            (month in [4, 6, 9,11] and (day > 30 or day < 1)) or \
            (month == 2 and (day> 28 or day < 1)):
            print("Invalid day value for a given month")
            return False
        return True
    except ValueError:
        print("Please enter correct date in correct format YYYY-MM-DD")
        return False


is_date_correct = False
while not is_date_correct:
    date = input("What year would you like to travel to (up to year 1958)? Please type the date in this "
                 "format YYYY-MM-DD:")
    split_date = date.split("-")
    is_date_correct = check_valid_date(split_date)

URL = "https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/"

response = requests.get(URL)
response.encoding = "utf-8"
