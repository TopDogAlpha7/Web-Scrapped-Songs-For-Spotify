import requests
import lxml
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

def configure():
  load_dotenv()

configure()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv("CLIENT_ID"), client_secret=os.getenv("CLIENT_SECRET"), redirect_uri=os.getenv("REDIRECT_URL"), show_dialog=True, cache_path="cache.txt", scope="playlist-modify-private"))

print("Enter the data in the format YYYY-MM-DD")

year = input("Enter year: ")
month = input("Enter month: ")
day = input("Enter day: ")
date = f"{year}-{month}-{day}"

response = requests.get(url=f"https://www.billboard.com/charts/hot-100/{date}")
txt = response.text

soup = BeautifulSoup(txt, "lxml")
title = soup.find_all(name="h3", id="title-of-a-story", class_="u-line-height-125")
all_titles = [song.getText().replace('\n\n\t\n\t\n\t\t\n\t\t\t\t\t', '').replace('\t\t\n\t\n', '') for song in title]

uri_list = []
for song in all_titles:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        uri_list.append(uri)
    except IndexError:
        pass

playlist = sp.user_playlist_create(user=os.getenv("USER_ID"), name="Web scrapped bangers", public=False)
playlist_id = playlist["id"]
sp.playlist_add_items(playlist_id=playlist_id, items=uri_list)

