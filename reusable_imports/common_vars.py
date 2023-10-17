# This file defines common variables which are used in more than one files
# These values should be retrieved as soon as the user logs in from the mapping table
import io
import os
import random
import pymysql
from cachecontrol import CacheControl
from cachecontrol.caches import FileCache
import requests
import cv2
import numpy

from utils.movie_utils import get_title, get_poster, get_lang, get_pop

# This list holds id of all the movies selected by the user in the checklist page
movies = list()

# This list holds the genres selected by the user in the genre page
genres = list()

# This list holds the languages selected by the user in the genre page
languages = list()

# Retrieved as soon as user logs in. This lists holds all the movie ids in the user's playlists
playlists_metadata = {
    'shortlist': ['Shortlist', 'Cinematch Team', '12/10/2023', [615656, 872585, 677179, 385687, 1397]],
    'completed': ['Completed', 'User', '02/03/2020', [238, 12, 37165]],
    'plantowatch': ['Plan To Watch', 'User', '12/12/2023', [575264, 267805, 283995]],
    'testplay': ['Test Play', 'User', '07/06/2023', [758009, 920143, 28152, 852096, 668482, 587092, 873126]]}

# Playlist metadata will be added in this when deleted
# Then this should be uploaded to the removed playlists table
removed_playlists = dict()

# unique identifiers for playlists which will be assigned when creating the playlists frame in the library page
playlists_original = list(playlists_metadata.keys())
poster = ["playlist_posters\\one.jpg", "playlist_posters\\two.jpg", "playlist_posters\\three.jpg"]
# Append more these three are default

# random picture generator for playlist img
playlist_picture = [random.choice(poster) for i in range(len(playlists_metadata))]

# stores the output of get_movies function
playlists_display_metadata = {}


def get_movies():
    """
    get the title, poster, language of all the movies in the playlists_metadata lists and stores it in
    playlists_display_metadata
    :return: None
    """

    # Common session used to load the images of all the movies in the metadata list. The images are then cached and
    # stored so when the program is run again, images load easily.
    cache_path = f"{os.path.expanduser('~')}\\AppData\\Local\\Temp\\CinematchCache\\.main_img_cache"
    session = CacheControl(requests.Session(), cache=FileCache(cache_path))

    # SQL connection
    conn = pymysql.connect(host='localhost', user='root', password='root', database='movies')

    # Main loop to get the metadata
    for i in range(len(list(playlists_metadata.keys()))):
        playlists_display_metadata[list(playlists_metadata.keys())[i]] = []
        name = list(playlists_metadata.keys())[i]

        for j in list(playlists_metadata.values())[i][3]:
            id = int(j)
            title = get_title(int(j), connection=conn, cursor=conn.cursor())  # gets title
            poster_path = get_poster(int(j), connection=conn, cursor=conn.cursor())  # gets poster path

            if poster_path is not 'nan':
                poster_var = session.get(f"https://image.tmdb.org/t/p/original{poster_path}").content
                # gets poster image as a byte array
            else:
                poster_var = None
                # executes if the poster path is not available in the database. This link above redirects to another
                # custom poster image for nan posters in the database.

            lang = get_lang(int(j), connection=conn, cursor=conn.cursor())  # gets movie lang
            popularity = get_pop(int(j), connection=conn, cursor=conn.cursor())  # gets movie popularity
            enter = [name, title, poster_var, lang, popularity, id]

            if type(title) is str:
                playlists_display_metadata[list(playlists_metadata.keys())[i]].append(tuple(enter))


def get_playlist_movies(list_name: str):
    if list_name in playlists_original:
        return playlists_display_metadata[list_name]
    else:
        return False
