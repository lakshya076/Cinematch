# This file defines common variables which are used in more than one files
# These values should be retrieved as soon as the user logs in from the mapping table
import os
import random
import pymysql
from cachecontrol import CacheControl
from cachecontrol.caches import FileCache
import requests

from backend.Utils.movie_utils import *
from backend.Utils.user_utils import get_logged_user
from backend.Utils.playlist_utils import *
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

# This list holds all the recommendations for the user (max - 15)
recoms = [615656, 872585, 677179, 385687, 1397]

# This list holds all the movies user can watch again (max - 10)
watchagain = [677179, 385687, 1397, 238, 12, 37165]

# This movie holds all the language movies based on the languages user has chosen (max -15)
language = [615656, 872585, 677179, 385687, 1397]

# Retrieved as soon as user logs in. This lists holds all the movie ids in the user's playlists
playlists_metadata = {}

# Common session used to load the images. The images are then cached and stored so when the program is run again,
# images load easily.
cache_path = f"{os.path.expanduser('~')}\\AppData\\Local\\Temp\\CinematchCache\\.main_img_cache"
session = CacheControl(requests.Session(), cache=FileCache(cache_path))


def init_uname():
    global username
    global no_logged

    username = get_logged_user(cur)
    no_logged = False

    if not username:
        username = "User"
        no_logged = True

    return username, no_logged


def init_list_metadata():
    global playlists_metadata
    global removed_playlist_movies
    if no_logged:
        playlists_metadata = {
            'shortlist': ['Shortlist', 'Cinematch Team', '12/10/2023', [615656, 872585, 677179, 385687, 1397]],
            'test1': ['Test 1', f'{username}', '02/03/2020', [238, 12, 37165]],
            'test2': ['Test 2', f'{username}', '12/12/2023', [575264, 267805, 283995]],
            'test3': ['Test 3', f'{username}', '07/06/2023', [758009, 920143, 28152, 852096, 668482, 587092, 873126]]}
    else:
        playlists_metadata = {}
        playlists_info = get_playlists_info(username, cur)
        for i in playlists_info:
            print(i)
            removed_playlist_movies[i[2]] = []
            playlists_metadata[remove_spaces(i[2])] = [i[2], i[0], '-'.join(i[6].split('-')[::-1]), i[3], i[5]]

    global playlist_picture
    playlist_picture = [random.choice(poster) for i in playlists_metadata.keys()]

    return playlists_metadata, playlist_picture


# Playlist metadata will be added in this when deleted
# Then this should be uploaded to the removed playlists table
removed_playlists = {}
removed_playlist_movies = {}

# Random movies to choose for the random page function
random_movies = get_random(cur, 20)

poster = ["playlist_posters\\one.jpg", "playlist_posters\\two.jpg", "playlist_posters\\three.jpg",
          "playlist_posters\\four.png"]
# Append more these three are default

# random picture generator for playlist img
playlist_picture = [random.choice(poster) for i in playlists_metadata.keys()]

# stores the output of get_movies function
playlists_display_metadata = {}

not_found_img = bytes(open('reusable_imports/not_found.png', 'rb').read())

movie_data = {"recoms": [], "watchagain": [], "language": []}


def get_data():
    """
    Function to get the data of movies in recoms, watch again and languages list (the movies which will be displayed on
    home screen)
    """
    # Common session used to load the images of all the movies in the metadata list. The images are then cached and
    # stored so when the program is run again, images load easily.
    cache_path = f"{os.path.expanduser('~')}\\AppData\\Local\\Temp\\CinematchCache\\.main_img_cache"
    session = CacheControl(requests.Session(), cache=FileCache(cache_path))

    # Local SQL Connection
    conn = pymysql.connect(host='localhost', user='root', password='root', database='movies')
    cur = conn.cursor()

    print("Getting data for home screen")

    movie_list = [recoms, watchagain, language]
    for i in range(len(movie_list)):

        movies_info = get_movies_info(movie_list[i], cur)
        for j in movies_info:
            title = j[1]  # gets title
            poster_path = j[-1]  # gets poster path
            print("ok")

            if poster_path != 'nan' and poster_path:
                try:
                    poster_var = session.get(f"https://image.tmdb.org/t/p/original{poster_path}").content
                except requests.ConnectionError:  # Network Error
                    poster_var = not_found_img
                # gets poster image as a byte array
            else:
                poster_var = not_found_img
                # executes if the poster path is not available in the database.

            enter = [list(movie_data.keys())[i], title, poster_var, j]

            movie_data[list(movie_data.keys())[i]].append(tuple(enter))


def get_movies():
    """
    get the title, poster, language of all the movies in the playlists_metadata lists and stores it in
    playlists_display_metadata
    :return: None
    """
    print("Getting playlists data")

    # Threaded function needs its own connection
    conn = pymysql.connect(host='localhost', user='root', password='root', database='movies')
    cur = conn.cursor()

    # Main loop to get the metadata
    for i in playlists_metadata.keys():
        playlists_display_metadata[i] = []
        movies_info = get_movies_info(playlists_metadata[i][3], cur)

        for j in movies_info:
            id = j[0]

            title = j[1]
            poster_path = j[8]
            lang = j[5]
            popularity = j[6]

            # title = get_title(int(j), cursor=conn.cursor())  # gets title
            # poster_path = get_poster(int(j), cursor=conn.cursor())  # gets poster path
            # lang = get_lang(int(j), cursor=conn.cursor())  # gets movie lang
            # popularity = get_pop(int(j), cursor=conn.cursor())  # gets movie popularity

            if poster_path != 'nan' and poster_path:
                try:
                    poster_var = session.get(f"https://image.tmdb.org/t/p/original{poster_path}").content
                except requests.ConnectionError:  # Network Error
                    poster_var = not_found_img
                # gets poster image as a byte array
            else:
                poster_var = not_found_img
                # executes if the poster path is not available in the database.

            enter = [i, title, poster_var, lang, popularity, id]

            if type(title) is str:
                playlists_display_metadata[i].append(tuple(enter))

    conn.close()

    return playlists_display_metadata


def get_playlist_movies(list_name: str):
    if list_name in playlists_metadata.keys():
        return playlists_display_metadata[list_name]
    else:
        return False


iso_639_1 = {'ab': 'Abkhaz', 'aa': 'Afar', 'af': 'Afrikaans', 'ak': 'Akan', 'sq': 'Albanian', 'am': 'Amharic',
             'ar': 'Arabic', 'an': 'Aragonese', 'hy': 'Armenian', 'as': 'Assamese', 'av': 'Avaric',
             'ae': 'Avestan', 'ay': 'Aymara', 'az': 'Azerbaijani', 'bm': 'Bambara', 'ba': 'Bashkir',
             'eu': 'Basque', 'be': 'Belarusian', 'bn': 'Bengali', 'bh': 'Bihari', 'bi': 'Bislama', 'bs': 'Bosnian',
             'br': 'Breton', 'bg': 'Bulgarian', 'my': 'Burmese', 'ca': 'Catalan; Valencian', 'ch': 'Chamorro',
             'ce': 'Chechen', 'ny': 'Chichewa; Chewa; Nyanja', 'zh': 'Chinese', 'cv': 'Chuvash', 'kw': 'Cornish',
             'co': 'Corsican', 'cr': 'Cree', 'hr': 'Croatian', 'cs': 'Czech', 'da': 'Danish',
             'dv': 'Divehi; Maldivian;', 'nl': 'Dutch', 'dz': 'Dzongkha', 'en': 'English', 'eo': 'Esperanto',
             'et': 'Estonian', 'ee': 'Ewe', 'fo': 'Faroese', 'fj': 'Fijian', 'fi': 'Finnish', 'fr': 'French',
             'ff': 'Fula', 'gl': 'Galician', 'ka': 'Georgian', 'de': 'German', 'el': 'Greek, Modern',
             'gn': 'Guaraní', 'gu': 'Gujarati', 'ht': 'Haitian', 'ha': 'Hausa', 'he': 'Hebrew (modern)',
             'hz': 'Herero', 'hi': 'Hindi', 'ho': 'Hiri Motu', 'hu': 'Hungarian', 'ia': 'Interlingua',
             'id': 'Indonesian', 'ie': 'Interlingue', 'ga': 'Irish', 'ig': 'Igbo', 'ik': 'Inupiaq', 'io': 'Ido',
             'is': 'Icelandic', 'it': 'Italian', 'iu': 'Inuktitut', 'ja': 'Japanese', 'jv': 'Javanese',
             'kl': 'Kalaallisut', 'kn': 'Kannada', 'kr': 'Kanuri', 'ks': 'Kashmiri', 'kk': 'Kazakh', 'km': 'Khmer',
             'ki': 'Kikuyu, Gikuyu', 'rw': 'Kinyarwanda', 'ky': 'Kirghiz, Kyrgyz', 'kv': 'Komi', 'kg': 'Kongo',
             'ko': 'Korean', 'ku': 'Kurdish', 'kj': 'Kwanyama, Kuanyama', 'la': 'Latin', 'lb': 'Luxembourgish',
             'lg': 'Luganda', 'li': 'Limburgish', 'ln': 'Lingala', 'lo': 'Lao', 'lt': 'Lithuanian',
             'lu': 'Luba-Katanga', 'lv': 'Latvian', 'gv': 'Manx', 'mk': 'Macedonian', 'mg': 'Malagasy',
             'ms': 'Malay', 'ml': 'Malayalam', 'mt': 'Maltese', 'mi': 'Māori', 'mr': 'Marathi (Marāṭhī)',
             'mh': 'Marshallese', 'mn': 'Mongolian', 'na': 'Nauru', 'nv': 'Navajo, Navaho',
             'nb': 'Norwegian Bokmål', 'nd': 'North Ndebele', 'ne': 'Nepali', 'ng': 'Ndonga',
             'nn': 'Norwegian Nynorsk', 'no': 'Norwegian', 'ii': 'Nuosu', 'nr': 'South Ndebele', 'oc': 'Occitan',
             'oj': 'Ojibwe, Ojibwa', 'cu': 'Old Church Slavonic', 'om': 'Oromo', 'or': 'Oriya',
             'os': 'Ossetian, Ossetic', 'pa': 'Panjabi, Punjabi', 'pi': 'Pāli', 'fa': 'Persian', 'pl': 'Polish',
             'ps': 'Pashto, Pushto', 'pt': 'Portuguese', 'qu': 'Quechua', 'rm': 'Romansh', 'rn': 'Kirundi',
             'ro': 'Romanian, Moldavan', 'ru': 'Russian', 'sa': 'Sanskrit (Saṁskṛta)', 'sc': 'Sardinian',
             'sd': 'Sindhi', 'se': 'Northern Sami', 'sm': 'Samoan', 'sg': 'Sango', 'sr': 'Serbian',
             'gd': 'Scottish Gaelic', 'sn': 'Shona', 'si': 'Sinhala, Sinhalese', 'sk': 'Slovak', 'sl': 'Slovene',
             'so': 'Somali', 'st': 'Southern Sotho', 'es': 'Spanish; Castilian', 'su': 'Sundanese',
             'sw': 'Swahili', 'ss': 'Swati', 'sv': 'Swedish', 'ta': 'Tamil', 'te': 'Telugu', 'tg': 'Tajik',
             'th': 'Thai', 'ti': 'Tigrinya', 'bo': 'Tibetan', 'tk': 'Turkmen', 'tl': 'Tagalog', 'tn': 'Tswana',
             'to': 'Tonga', 'tr': 'Turkish', 'ts': 'Tsonga', 'tt': 'Tatar', 'tw': 'Twi', 'ty': 'Tahitian',
             'ug': 'Uighur, Uyghur', 'uk': 'Ukrainian', 'ur': 'Urdu', 'uz': 'Uzbek', 've': 'Venda',
             'vi': 'Vietnamese', 'vo': 'Volapük', 'wa': 'Walloon', 'cy': 'Welsh', 'wo': 'Wolof',
             'fy': 'Western Frisian', 'xh': 'Xhosa', 'yi': 'Yiddish', 'yo': 'Yoruba', 'za': 'Zhuang, Chuang',
             'zu': 'Zulu'}
