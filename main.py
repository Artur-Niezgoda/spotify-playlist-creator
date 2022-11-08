import requests
from bs4 import BeautifulSoup
from datetime import datetime
from environs import Env
import spotipy
from spotipy.oauth2 import SpotifyOAuth


def check_valid_date(split_date):
    year = split_date[0]
    month = split_date[1]
    day = split_date[2]
    try:
        year = int(year)
        month = int(month)
        day = int(day)
        if year < 1958 or year > datetime.now().year:
            print("Invalid year value")
            return False
        if month > 12 or month < 1:
            print("Invalid month value")
            return False
        if (month in [1, 3, 5, 7, 8, 10, 12] and (day > 31 or day < 1)) or \
                (month in [4, 6, 9, 11] and (day > 30 or day < 1)) or \
                (month == 2 and (day > 28 or day < 1)):
            print("Invalid day value for a given month")
            return False
        return True
    except ValueError:
        print("Please enter correct date in correct format YYYY-MM-DD")
        return False


# Read environment variables from env file
env = Env()
env.read_env()
spotipy_client_id = env("SPOTIPY_CLIENT_ID")
spotipy_client_secret = env("SPOTIPY_CLIENT_SECRET")
redirect_uri = env("SPOTIPY_REDIRECT_URI")

date = "1958-01-01"
is_date_correct = False
while not is_date_correct:
    date = input("What year would you like to travel to (up to year 1958)? Please type the date in this "
                 "format YYYY-MM-DD:")
    is_date_correct = check_valid_date(date.split("-"))

# Get the Website
URL = f"https://www.billboard.com/charts/hot-100/{date}"
response = requests.get(URL)
response.encoding = "utf-8"

# Scrape
soup = BeautifulSoup(response.text, 'html.parser')

songs = soup.find_all("h3", class_="a-no-trucate")
artists = soup.find_all("span", class_="a-no-trucate")

# Initialize authentication
spotify = spotipy.Spotify(
    auth_manager=SpotifyOAuth(client_id=spotipy_client_id,
                              client_secret=spotipy_client_secret,
                              scope="playlist-modify-private",
                              redirect_uri=redirect_uri,
                              show_dialog=True,
                              cache_path="token.txt"))

user_id = spotify.current_user()["id"]

# Create a playlist
playlist = spotify.user_playlist_create(user=user_id,
                                        name=f"Pythonista playlist ({date})",
                                        public=False,
                                        description="playlist created by python code")

# Initialize query
item_list = []
for index in range(len(artists)):
    song = songs[index].getText()
    artist = artists[index].getText()

    query = spotify.search(q=f"track:{song} artist:{artist}", type="track", limit=1, market="US")
    try:
        song_uri = query["tracks"]["items"][0]["uri"]
    except IndexError:
        print(f"track not found")
        continue
    else:
        item_list.append(song_uri)

spotify.playlist_add_items(playlist_id=playlist["id"], items=item_list) # add all found songs to the playlist
