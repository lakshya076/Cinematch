# This file defines common variables which are used in more than one files
# These values should be retrieved as soon as the user logs in from the mapping table
import os
import random
import pymysql
from cachecontrol import CacheControl
from cachecontrol.caches import FileCache
import requests

from utils.movie_utils import get_title, get_poster, get_lang, get_pop

# This list holds id of all the movies selected by the user in the checklist page
movies = list()

# This list holds the genres selected by the user in the genre page
genres = list()

# This list holds the languages selected by the user in the genre page
languages = list()

# Username
username = "User"

# Retrieved as soon as user logs in. This lists holds all the movie ids in the user's playlists
playlists_metadata = {
    'shortlist': ['Shortlist', 'Cinematch Team', '12/10/2023', [615656, 872585, 677179, 385687, 1397]],
    'test1': ['Test 1', f'{username}', '02/03/2020', [238, 12, 37165]],
    'test2': ['Test 2', f'{username}', '12/12/2023', [575264, 267805, 283995]],
    'test3': ['Test 3', f'{username}', '07/06/2023', [758009, 920143, 28152, 852096, 668482, 587092, 873126]]}

# Playlist metadata will be added in this when deleted
# Then this should be uploaded to the removed playlists table
removed_playlists = dict()

# Random movies to choose for the random page function
random_movies = [615656, 872585, 677179, 385687, 1397, 238, 12, 37165, 758009, 920143, 28152, 852096, 668482, 587092,
                 873126, 575264, 267805, 283995]

poster = ["playlist_posters\\one.jpg", "playlist_posters\\two.jpg", "playlist_posters\\three.jpg",
          "playlist_posters\\four.png"]
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
            lang = get_lang(int(j), connection=conn, cursor=conn.cursor())  # gets movie lang
            popularity = get_pop(int(j), connection=conn, cursor=conn.cursor())  # gets movie popularity
            if poster_path != 'nan':
                try:
                    poster_var = session.get(f"https://image.tmdb.org/t/p/original{poster_path}").content
                except requests.ConnectionError:  # Network Error
                    poster_var = None
                # gets poster image as a byte array
            else:
                poster_var = None
                # executes if the poster path is not available in the database.

            enter = [name, title, poster_var, lang, popularity, id]

            if type(title) is str:
                playlists_display_metadata[list(playlists_metadata.keys())[i]].append(tuple(enter))


def get_playlist_movies(list_name: str):
    if list_name in playlists_metadata.keys():
        try:
            return playlists_display_metadata[list_name]
        except KeyError:
            return False
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
