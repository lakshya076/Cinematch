# This file defines common variables which are used in more than one files
# These values should be retrieved as soon as the user logs in from the mapping table
import datetime
import os
import random
from typing import Tuple, List, Any, Dict

import pymysql
from cachecontrol import CacheControl
from cachecontrol.caches import FileCache
import requests

from backend.Utils.movie_utils import *
from backend.Utils.user_utils import get_logged_user, is_premium
from backend.Utils.playlist_utils import *
from backend.Utils.mapping_utils import *
from reusable_imports.commons import remove_spaces

# This list holds id of all the movies selected by the user in the checklist page - works only when user registers
movies = list()

# This list holds the genres selected by the user in the genre page - works only when user registers
genres = list()

# This list holds the languages selected by the user in the genre page - works only when user registers
languages = list()

# Universal SQL connection
conn = pymysql.connect(host='localhost', user='root', password='root', database='movies')
cur = conn.cursor()

# Username
no_logged = True
username = "User"

# Premium user or not. 0 -> No; 1 -> Yes
premium = 0

# List to store ad posters
ad = ["Advertisements/ad_one.png", "Advertisements/ad_two.png"]

# This list holds all the recommendations for the user (max - 15)
recoms = list()

# This list holds all the movies user can watch again (max - 10)
watchagain = list()

# This movie holds all the language movies based on the languages user has chosen (max -15)
language = list()

# Retrieved as soon as user logs in. This lists holds all the movie ids in the user's playlists
# Stores the image as str
playlists_metadata = dict()
"""
    Structure:- 
        {playlist name, username, playlist date, [movie id in playlist], none}
"""

# Dictionary to store metadata of random, home and playlist movies. Gets populated in splash screen
movies_metadata = dict()
"""
    Structure:-
        {id: [title, overview, real_date, genre_real, lang_real, str(pop), cast, poster_var]}
"""

# Common session used to load the images. The images are then cached and stored so when the program is run again,
# images load easily.
cache_path = f"{os.path.expanduser('~')}\\AppData\\Local\\Cinematch\\Cache"
session = CacheControl(requests.Session(), cache=FileCache(cache_path))


def init_uname() -> tuple:
    """
    Checks if the user is already logged in, if true gets the information of the user. If false, startup window is
    opened
    """
    print("Checking for recurring login")
    global username
    global no_logged
    global premium

    username = get_logged_user(cur)
    no_logged = False

    if not username:
        username = "User"
        no_logged = True
    else:
        premium = is_premium(username, cur)

    return username, no_logged, premium


def init_list_metadata() -> tuple:
    """
    Gets playlist metadata of all playlists if the user is logged in
    """
    print("Initialising playlists")
    global playlists_metadata
    global removed_playlist_movies
    global recoms
    global watchagain
    global language
    if no_logged:
        playlists_metadata = {'shortlist': ['Shortlist', 'Cinematch Team', '--/--/----', []]}

    else:
        playlists_metadata = {}
        playlists_info = get_playlists_info(username, cur)
        for i in playlists_info:
            removed_playlist_movies[i[2]] = []
            playlists_metadata[remove_spaces(i[2])] = [i[2], i[0], '-'.join(i[6].split('-')[::-1]), i[3], i[5]]

    global playlist_picture
    playlist_picture = [random.choice(poster) for i in playlists_metadata.keys()]

    return playlists_metadata, playlist_picture, removed_playlist_movies


def init_mapping() -> tuple:
    """
    Initialises the mapping data for the logged-in user
    """
    global recoms, watchagain, language
    print('Init Mapping')
    if not no_logged:
        mapping_data = get_mapping_data(username, cur)
        recoms = mapping_data[6]
        random.shuffle(recoms)
        watchagain = mapping_data[3]
        language = get_language_movies(username, 30, cur)

    return recoms, watchagain, language


# Playlist metadata will be added in this when deleted
# Then this should be uploaded to the removed playlists table
removed_playlists = {}
removed_playlist_movies = {}

# Random movies to choose for the random page function
random_movies = get_random(cur, 50)

poster = ["playlist_posters\\one.jpg", "playlist_posters\\two.jpg", "playlist_posters\\three.jpg",
          "playlist_posters\\four.png"]
playlist_picture = [random.choice(poster) for i in playlists_metadata.keys()]
# random picture generator for playlist img

# Stores the specific metadata of movies that need to be shown in the list of a specific playlist
# Also stores the movie image as bytearray
playlists_display_metadata = dict()

not_found_img = bytes(open('reusable_imports/not_found.png', 'rb').read())


def get_data() -> tuple[list[list[int] | list[Any] | Any], dict[Any, Any]]:
    """
    Function to get the data of movies in recoms, watch again and languages list (the movies which will be displayed on
    home screen)
    Also gets the movie data in the random and all the playlists
    """

    # Local SQL Connection
    conn = pymysql.connect(host='localhost', user='root', password='root', database='movies')
    cur = conn.cursor()

    print("Getting movie data")

    init_mapping()
    global recoms, watchagain, language, random_movies
    movie_list = [recoms, watchagain, language, random_movies]
    for i in range(len(movie_list)):
        movies_info = get_movies_info(movie_list[i], cur)
        movie_list[i] = []
        for j in movies_info:
            title = j[1] or "Not Available"  # gets title
            overview = j[2] or "Not Available"
            date = j[3]
            gen = j[4] or "Not Available"
            lang = j[5] or "Not Available"
            pop = j[6] or "Not Available"
            cast = j[7] or "Not Available"
            poster_path = j[8]  # gets poster path

            movie_list[i].append(int(j[0]))

            genre_real = "Not Available"
            lang_real = ""

            # Formatting date
            try:
                real_date = datetime.datetime.strptime(str(date), "%Y-%m-%d").strftime("%d-%m-%Y")
            except ValueError:
                real_date = "Not Available"

            # Formatting genre
            if gen != "Not Available":
                genre_real = ", ".join(gen)

            # Formatting poster path
            if poster_path != 'nan' and poster_path:
                try:
                    poster_var = session.get(f"https://image.tmdb.org/t/p/original{poster_path}").content
                except requests.ConnectionError:  # Network Error
                    poster_var = not_found_img
                # gets poster image as a byte array
            else:
                poster_var = not_found_img
                # executes if the poster path is not available in the database.

            # Formatting language
            if lang != "Not Available":
                try:
                    lang_real = iso_639_1[lang]
                except KeyError:
                    lang_real = lang

            print(f"Movie got {j[0]}")

            metadata_enter = [title, overview, real_date, genre_real, lang_real, str(pop), cast, poster_var]

            if j[0] not in movies_metadata:
                movies_metadata[int(j[0])] = metadata_enter

        print(movie_list[i])

    recoms = movie_list[0]
    watchagain = movie_list[1]
    language = movie_list[2]
    return movie_list, movies_metadata


def get_movies() -> tuple:
    """
    get the title, poster, language of all the movies in the playlists_metadata lists and stores it in
    playlists_display_metadata
    """
    print("Getting playlists data")

    global playlists_display_metadata, movies_metadata

    # Threaded function needs its own connection
    conn = pymysql.connect(host='localhost', user='root', password='root', database='movies')
    cur = conn.cursor()

    # Main loop to get the metadata
    for i in playlists_metadata.keys():
        playlists_display_metadata[i] = []
        print(i)
        movies_info = get_movies_info(playlists_metadata[i][3], cur)

        for j in movies_info:
            id = j[0]

            title = j[1] or "Not Available"  # gets title
            overview = j[2] or "Not Available"
            date = j[3]
            gen = j[4] or "Not Available"
            lang = j[5] or "Not Available"
            pop = j[6] or "Not Available"
            cast = j[7] or "Not Available"
            poster_path = j[8]  # gets poster path

            genre_real = "Not Available"
            lang_real = ""

            # Formatting date
            try:
                real_date = datetime.datetime.strptime(str(date), "%Y-%m-%d").strftime("%d-%m-%Y")
            except ValueError:
                real_date = "Not Available"

            # Formatting genre
            if gen != "Not Available":
                genre_real = ", ".join(gen)

            # Formatting poster path
            if poster_path != 'nan' and poster_path:
                try:
                    poster_var = session.get(f"https://image.tmdb.org/t/p/original{poster_path}").content
                except requests.ConnectionError:  # Network Error
                    poster_var = not_found_img
                # gets poster image as a byte array
            else:
                poster_var = not_found_img
                # executes if the poster path is not available in the database.

            # Formatting language
            if lang != "Not Available":
                try:
                    lang_real = iso_639_1[lang]
                except KeyError:
                    lang_real = lang

            print(f"Movie got {j[0]}")

            enter = [i, title, poster_var, lang, str(pop), id]  # Add to playlist display metadata
            metadata_enter = [title, overview, real_date, genre_real, lang_real, str(pop), cast, poster_var]

            if type(title) is str:
                playlists_display_metadata[i].append(enter)

            if j[0] not in movies_metadata:
                movies_metadata[int(j[0])] = metadata_enter
            else:
                pass

    conn.close()

    print(f'Check PDM: {playlists_display_metadata.keys()}')

    return playlists_display_metadata, movies_metadata


def get_playlist_movies(list_name: str) -> list | bool:
    """
    Gets the list of movies and their metadata from the playlists_display_metadata dict given the playlist name
    """
    if list_name in playlists_metadata.keys():
        return playlists_display_metadata[list_name]
    else:
        return False


iso_639_1 = {'ab': 'Abkhaz', 'aa': 'Afar', 'af': 'Afrikaans', 'ak': 'Akan', 'sq': 'Albanian', 'am': 'Amharic',
             'ar': 'Arabic', 'an': 'Aragonese', 'hy': 'Armenian', 'as': 'Assamese', 'av': 'Avaric', 'ae': 'Avestan',
             'ay': 'Aymara', 'az': 'Azerbaijani', 'bm': 'Bambara', 'ba': 'Bashkir', 'eu': 'Basque', 'be': 'Belarusian',
             'bn': 'Bengali', 'bh': 'Bihari', 'bi': 'Bislama', 'bs': 'Bosnian', 'br': 'Breton', 'bg': 'Bulgarian',
             'my': 'Burmese', 'ca': 'Catalan', 'ch': 'Chamorro', 'ce': 'Chechen', 'ny': 'Chichewa', 'zh': 'Chinese',
             'cv': 'Chuvash', 'kw': 'Cornish', 'co': 'Corsican', 'cr': 'Cree', 'hr': 'Croatian', 'cs': 'Czech',
             'da': 'Danish', 'dv': 'Divehi;', 'nl': 'Dutch', 'dz': 'Dzongkha', 'en': 'English', 'eo': 'Esperanto',
             'et': 'Estonian', 'ee': 'Ewe', 'fo': 'Faroese', 'fj': 'Fijian', 'fi': 'Finnish', 'fr': 'French',
             'ff': 'Fula', 'gl': 'Galician', 'ka': 'Georgian', 'de': 'German', 'el': 'Greek', 'gn': 'Guaraní',
             'gu': 'Gujarati', 'ht': 'Haitian', 'ha': 'Hausa', 'he': 'Hebrew', 'hz': 'Herero', 'hi': 'Hindi',
             'ho': 'Hiri Motu', 'hu': 'Hungarian', 'ia': 'Interlingua', 'id': 'Indonesian', 'ie': 'Interlingue',
             'ga': 'Irish', 'ig': 'Igbo', 'ik': 'Inupiaq', 'io': 'Ido', 'is': 'Icelandic', 'it': 'Italian',
             'iu': 'Inuktitut', 'ja': 'Japanese', 'jv': 'Javanese', 'kl': 'Kalaallisut', 'kn': 'Kannada',
             'kr': 'Kanuri', 'ks': 'Kashmiri', 'kk': 'Kazakh', 'km': 'Khmer', 'ki': 'Kikuyu', 'rw': 'Kinyarwanda',
             'ky': 'Kirghiz, Kyrgyz', 'kv': 'Komi', 'kg': 'Kongo', 'ko': 'Korean', 'ku': 'Kurdish', 'kj': 'Kwanyama',
             'la': 'Latin', 'lb': 'Luxembourgish', 'lg': 'Luganda', 'li': 'Limburgish', 'ln': 'Lingala', 'lo': 'Lao',
             'lt': 'Lithuanian', 'lu': 'Luba-Katanga', 'lv': 'Latvian', 'gv': 'Manx', 'mk': 'Macedonian',
             'mg': 'Malagasy', 'ms': 'Malay', 'ml': 'Malayalam', 'mt': 'Maltese', 'mi': 'Māori', 'mr': 'Marathi',
             'mh': 'Marshallese', 'mn': 'Mongolian', 'na': 'Nauru', 'nv': 'Navajo, Navaho', 'nb': 'Norwegian Bokmål',
             'nd': 'North Ndebele', 'ne': 'Nepali', 'ng': 'Ndonga', 'nn': 'Norwegian Nynorsk', 'no': 'Norwegian',
             'ii': 'Nuosu', 'nr': 'South Ndebele', 'oc': 'Occitan', 'oj': 'Ojibwa', 'cu': 'Old Church Slavonic',
             'om': 'Oromo', 'or': 'Oriya', 'os': 'Ossetian', 'pa': ' Punjabi', 'pi': 'Pāli', 'fa': 'Persian',
             'pl': 'Polish', 'ps': 'Pashto', 'pt': 'Portuguese', 'qu': 'Quechua', 'rm': 'Romansh', 'rn': 'Kirundi',
             'ro': 'Romanian', 'ru': 'Russian', 'sa': 'Sanskrit', 'sc': 'Sardinian', 'sd': 'Sindhi',
             'se': 'Northern Sami', 'sm': 'Samoan', 'sg': 'Sango', 'sr': 'Serbian', 'gd': 'Scottish Gaelic',
             'sn': 'Shona', 'si': 'Sinhala', 'sk': 'Slovak', 'sl': 'Slovene', 'so': 'Somali', 'st': 'Southern Sotho',
             'es': 'Spanish', 'su': 'Sundanese', 'sw': 'Swahili', 'ss': 'Swati', 'sv': 'Swedish', 'ta': 'Tamil',
             'te': 'Telugu', 'tg': 'Tajik', 'th': 'Thai', 'ti': 'Tigrinya', 'bo': 'Tibetan', 'tk': 'Turkmen',
             'tl': 'Tagalog', 'tn': 'Tswana', 'to': 'Tonga', 'tr': 'Turkish', 'ts': 'Tsonga', 'tt': 'Tatar',
             'tw': 'Twi', 'ty': 'Tahitian', 'ug': 'Uighur', 'uk': 'Ukrainian', 'ur': 'Urdu', 'uz': 'Uzbek',
             've': 'Venda', 'vi': 'Vietnamese', 'vo': 'Volapük', 'wa': 'Walloon', 'cy': 'Welsh', 'wo': 'Wolof',
             'fy': 'Western Frisian', 'xh': 'Xhosa', 'yi': 'Yiddish', 'yo': 'Yoruba', 'za': 'Zhuang', 'zu': 'Zulu'}

iso_639_1_inv = {v: k for k, v in iso_639_1.items()}
