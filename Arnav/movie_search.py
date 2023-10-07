import pymysql
import pymysql.cursors


def phrase_former(phrase: str, sep: str):

    phrase_list = []
    split_phrase = phrase.split()

    for i in range(len(split_phrase)+1):
        phrase_list.append(' '.join(split_phrase[:i]) + sep + ' ' + ' '.join(split_phrase[i:]))

    phrase_list.pop()

    return phrase_list[1:]

def search(phrase: str, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):
    
    '''
    
    search for movies using `phrase`
    
    '''

    title_search = []
    genre_search = []
    cast_search = []
    keyword_search = []
    overview_search = []

    cursor.execute(f'select id from main where overview like "%{phrase}%" order by popularity desc')
    overview_search.extend([int(i[0]) for i in cursor.fetchall()])

    cursor.execute(f'select id from main where title like "%{phrase}%" order by popularity desc')
    title_search.extend([int(i[0]) for i in cursor.fetchall()])

    L = []
    s = ''
    for sep in [':', ';', ' -']:
        L.extend(phrase_former(phrase, sep))
    for i in L:
        s += f'"%{i}%" or title like '
    s = s[:len(s)-15]


    cursor.execute(f'select id from main where title like {s} or title sounds like "{phrase}" order by popularity desc')
    title_search.extend([int(j[0]) for j in cursor.fetchall()])

    cursor.execute(f'select id from main where genres like "%{phrase}%" order by popularity desc')
    genre_search.extend([int(i[0]) for i in cursor.fetchall()])

    cursor.execute(f'select id from recommendation where keywords like "%{phrase}%" order by popularity desc')
    keyword_search.extend([int(i[0]) for i in cursor.fetchall()])

    cursor.execute(f'select id from main where cast like "%{phrase}%" order by popularity desc')
    cast_search.extend([int(i[0]) for i in cursor.fetchall()])

    combined_search = title_search + cast_search + overview_search + keyword_search
    combined_search = list(set(combined_search))

    return combined_search

