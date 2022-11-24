from pathlib import Path
from os import chdir
from os import listdir
from time import sleep
import requests
import streamrip

from wavedemon import login

class Download():
    """
    Wrapper for both libraries to simplify downloading
    General idea is to just pass an ID to download and this class figures out the rest

    """

    def __init__(self): # Setup to login and set class level variables with login info, favorites, and dl client
        self.item_id = None

    def download(self, item_id):
        """
        Download abstractor method

        Keyword arguments:
        item_id - ID of item to download

        """

    def correct_metadata(self):
        """
        Add later but setup Musicbrainz to scan and correct metadata of
        downloaded media

        """


    def _playlist(self):
        """
        Download playlist

        """

session = login.tidalapi_login()
favorites = session.user.Favorites()
tidal_client = login.tidaldl_login(session)

def download_playlists():
    playlists = favorites.playlists()
    p_path = Path("Playlists")

    if not p_path.exists() or not p_path.is_dir():
        p_path.mkdir()
    chdir(p_path)

    playlist_ids = []
    for p in playlists:
        playlist_ids.append(p.id)
    
    streamrip_client_playlist_objects = []
    for p_id in playlist_ids:
        try:
            p = streamrip.media.Playlist(client=tidal_client, id=p_id)
            p.load_meta()
            streamrip_client_playlist_objects.append(p)
        except:
            continue 

    for p in streamrip_client_playlist_objects:
        try:
            p.download(parent_folder=p.name)
            create_m3u(p.name)
        except:
            create_m3u(p.name)
            continue
    chdir(Path().resolve().parent)
    
def download_albums():
    tidalapi_album_objects = favorites.albums()
    a_path = Path("Albums")

    if not a_path.exists() or not a_path.is_dir():
        a_path.mkdir()
    chdir(a_path) 

    albums = {}
    for album in tidalapi_album_objects:
        albums.update({album.id: album.name})
    
    streamrip_client_album_objects = {}
    for album_id, album_name in albums.items():
        try:
            streamrip_album_object = streamrip.media.Album(client=tidal_client, id=album_id)
            print(f"Retrieving metadata for {album_name}") 
            #Consider backing up metadata to database to prevent reloading every time
            #Also add a check for existing albums to prevent crashing the download function
            streamrip_album_object.load_meta()
            streamrip_client_album_objects.update({album_name: streamrip_album_object})
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                print("Mmmmm slow down chief")
                break
            else:
                raise e
        except:
            continue
    
    for album_name, a in streamrip_client_album_objects.items():
        try:
            a.download(parent_folder=album_name, quality=4)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                print("2 minute cooldown bc we angered the api gods")
                sleep(120)
                continue
        except:
            continue
    chdir(Path().resolve().parent)

download_playlists()
download_albums()
