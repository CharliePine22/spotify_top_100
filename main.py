from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import lxml

user_date_input = input(
    'What year would you like to grab the top 100 songs? Please enter in YYYY-MM-DD format(1994-11-30): ')

# Spotify API Authentication
SPOTIFY_CLIENT_ID = "3a70afa9732749a2b07262054aca5873"
SPOTIFY_CLIENT_SECRET = "25570a8cac6e4beca8d60af1a6e3b75f"
SPOTIFY_DIRECT_URL = "https://developer.spotify.com/dashboard/applications/3a70afa9732749a2b07262054aca5873"
SPOTIPY_REDIRECT_URI = "http://example.com"

# Gaining access to spotify profile
scope = 'playlist-modify-public'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI, scope=scope, show_dialog=True,
                                               cache_path='.cache'))
user_id = sp.current_user()["id"]


def grab_top_100():
    # Scrape the billboard for the top 100 songs of whatever date the user inputs
    response = requests.get(f'https://www.billboard.com/charts/hot-100/{user_date_input}')
    soup = BeautifulSoup(response.text, 'lxml')
    all_text = [x.getText() for x in
                soup.find_all(name='span', class_='chart-element__information__song text--truncate color--primary')]
    return all_text


def create_playlist():
    new_playlist = sp.user_playlist_create(user_id, name=f'{user_date_input} top 100 Songs', collaborative=False,
                                           description="A playlist containing the top 100 songs of the date the user inputs.")


def grab_playlist_id():
    playlists = sp.user_playlists(user_id, limit=1)
    return playlists['items'][0]['id']


# 1974-02-26
def add_songs():
    search_str = ''
    song_uris = []
    for song in grab_top_100():
        search_str += song
        try:
            result = sp.search(search_str)['tracks']['items'][0]["uri"]
        except IndexError:
            pass
        else:
            song_uris.append(result)
        search_str = ''

    try:
        sp.playlist_add_items(grab_playlist_id(), items=song_uris, position=None)
    except (IndexError, KeyError, AttributeError):
        pass
    else:
        print('Song Added')
    finally:
        print('Finished')

# add_songs()
